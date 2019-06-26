.DEFAULT_GOAL := all

.PHONY: all, fetch, generate

all:
	 docker-compose --file Docker/docker-compose.yml up --build

fetch:
	docker exec binancedex /usr/local/bin/python -m binancedex.cli fetch-all-trades

generate:
	docker exec binancedex /usr/local/bin/python -m binancedex.cli report

