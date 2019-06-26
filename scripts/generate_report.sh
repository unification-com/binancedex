#! /bin/bash

docker exec binancedex /usr/local/bin/python -m binancedex.cli report

rm -f /home/deploy/src/ui/leaderboard.html
rm -f /home/deploy/src/ui/style.css

docker cp binancedex:/reports/leaderboard.html /home/deploy/src/ui/leaderboard.html
docker cp binancedex:/reports/stylesheet.css /home/deploy/src/ui/stylesheet.css
