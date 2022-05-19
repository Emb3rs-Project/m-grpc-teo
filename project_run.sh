LIBSPATH=ms-grpc/plibs

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, Need Path to python.file"
    exit
fi

export PYTHONPATH=ms_grpc/plibs 

python $1