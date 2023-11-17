#!/bin/bash

docker build -t etctest-xkxx:latest .

docker tag etctest-xkxx:latest milktjj/etctest-xkxx:latest

docker push milktjj/etctest-xkxx:latest
