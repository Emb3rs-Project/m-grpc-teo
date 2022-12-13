ARG BASE_TAG=latest

FROM ghcr.io/emb3rs-project/embers-base:${BASE_TAG} as build

# creating the environment
COPY environment-py39.yml .
RUN --mount=type=cache,target=/opt/conda/pkgs mamba env create -f environment-py39.yml

# Installing Conda Pack
RUN --mount=type=cache,target=/opt/conda/pkgs conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n teo-grpc-module -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar

ARG HIGHS_VERSION=1.3.0

# Add HiGHS Executable
ENV HIGHS_VERSION=${HIGHS_VERSION}
ENV JULIA_BINARY_PATH="https://github.com/JuliaBinaryWrappers/HiGHSstatic_jll.jl/releases/download"
ENV HIGHS_BINARY="HiGHSstatic-v$HIGHS_VERSION%2B0/HiGHSstatic.v${HIGHS_VERSION}.x86_64-linux-gnu-cxx11.tar.gz"
ENV HIGHS_URL="$JULIA_BINARY_PATH/$HIGHS_BINARY"

RUN wget -c $HIGHS_URL -O - | tar -xz -C /venv/.

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

FROM python:3.10-slim as runtime

ARG COPT_KEY

# setup config
ENV GROUP_ID=1000 \
    USER_ID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

# Copy dependencies
COPY --from=build /venv /venv

# Copy COPT
COPY --from=build /opt/copt60 /opt/copt60

# Configuring app
WORKDIR /app
COPY . .

# Submodules config
ENV PYTHONPATH=ms-grpc/plibs:module

# Gurobi config
ENV GRB_LICENSE_FILE=gurobi.lic

# COPT config
ENV COPT_HOME=/opt/copt60
ENV COPT_LICENSE_FILE=copt.lic \
    COPT_LICENSE_DIR=/opt/copt60 \
    PATH=$COPT_HOME/bin:$PATH \
    LD_LIBRARY_PATH=$COPT_HOME/lib:$LD_LIBRARY_PATH \
    PYTHONPATH=$PYTHONPATH:$COPT_HOME/lib/pulp

RUN test ! -z "$COPT_KEY" && copt_licgen -key $COPT_KEY || copt_licgen -file $COPT_LICENSE_FILE
COPY ./license.* .

# Expose PORT and activate venv
EXPOSE 50053

SHELL [ "/bin/bash", "-c" ]
RUN echo 'source /venv/bin/activate' >> ~/.bashrc && source ~/.bashrc

ENTRYPOINT source /venv/bin/activate && \
    python -u server.py