#!/bin/bash

python -m SimpleHTTPServer 7777 &
python reply.py &
node server.js
