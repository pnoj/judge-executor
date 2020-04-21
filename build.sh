#!/bin/bash
if [ -z "$1" ]
then
    echo "No argument supplied"
    exit 0
fi
cp files/* runtimes/$1/
docker build --tag=executor-$1:sha-$(git rev-parse --short=7 HEAD) runtimes/$1/
for file in files/*
do
    rm runtimes/$1/$(basename $file)
done
