#!/bin/bash
app="sourcerer.io"
docker build -t ${app} .
docker run --rm -d -p 127.0.0.1:3000:3000 --name=${app} ${app}