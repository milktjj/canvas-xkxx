#!/bin/bash

docker build -t etctest-xkxx:latest .

docker tag etctest-xkxx:latest etc.default.harbor:8888/library/etctest-xkxx:latest

docker push etc.default.harbor:8888/library/etctest-xkxx:latest
