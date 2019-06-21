#! /bin/bash

docker exec binancedex /usr/local/bin/python -m binancedex.cli report

rm /home/ubuntu/src/ui/leaderboard.html
rm /home/ubuntu/src/ui/style.css

docker cp binancedex:/reports/leaderboard.html /home/ubuntu/src/ui/leaderboard.html
docker cp binancedex:/reports/stylesheet.css /home/ubuntu/src/ui/stylesheet.css
