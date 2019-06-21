#! /bin/bash

docker exec binancedex /usr/local/bin/python -m binancedex.cli fetch-all-trades
