#! /bin/bash

docker exec binancedex /usr/local/bin/python -m binancedex.cli report

docker cp binancedex:/reports/leaderboard.html /www/leaderboard.html
docker cp binancedex:/reports/stylesheet.css /www/stylesheet.css
