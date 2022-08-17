# Module gRPC - TEO 
Platform gRPC Integration Module to communicate with TEO Module.

## Git
Clone this repository:
```shell
git clone https://github.com/Emb3rs-Project/m-grpc-teo.git
```

Load submodules:
```shell
git submodule init
git submodule update
```

## Setup Local Environment
Create Conda environment and install packages:
```shell
conda env create -n teo-grpc-module -f environment-py39.yml
conda activate teo-grpc-module
```

Create environment variables config file:
```shell
cp .env.example .env
```

Run grpc server:
```shell
PYTHONPATH=$PYTHONPATH:ms-grpc/plibs:module python server.py
```

## Setup Docker Environment
Create environment variables config file:
```shell
cp .env.example .env
```

Build docker image:
```shell
DOCKER_BUILDKIT=1 docker build -t m-grpc-teo .
```

Run docker image:
```shell
docker run -p 50053:50053 --name m-grpc-teo --rm m-grpc-teo
```

**NOTE**: *If you've run docker-dev from the Emb3rs-project repository before, I advise use the embers network 
in docker run to access PGSQL and change the database settings inside .env to Platform DB.*  

Run docker image with embers network:
```shell
docker run -p 50053:50053 --network dev_embers|platform_embers --name m-grpc-teo --rm m-grpc-teo
```