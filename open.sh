 #!/usr/bin/env bash

TEMPLATEPATH='/PATH/templates/template.cpp'

if [ "$#" -ne 2 ]; then
    echo [1m[31m'Error usage: ./open.sh contest problem'[0m
    exit
fi

mkdir -p $1
cp -n $TEMPLATEPATH $1/$2.cpp
