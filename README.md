![Unification](https://raw.githubusercontent.com/unification-com/mainchain/master/unification_logoblack.png "Unification")

## BinanceDEX Trade Statistics

The calculation of trade statistics for UND on the BinanceDEX displayed at 
https://leaderboard.unification.io can be found here.

Trade statistics for traders of UND is calculated by polling the dex.binance.org
api and storing data locally on a Postgres instance.

Helper scripts are available to generate a Jinja2 based static site with the
leaderboard.

It's hard to tell how Binance calculates their 24H volume calculation. This 
implementation assumes that fees are included in that calculation, however
there is still a 2% variation between the amount reported and the amount
calculated.

## Running

Type `make` to build and start the Docker composition.

Type `make fetch` to fetch all the trades from the BinanceDEX. This will fetch all the trades since UND has been listed.

Once the initial fetch is complete, type `make generate` to generate the latest trade statistics.

The leaderboard.html and stylesheet.css can then be downloaded:
```
docker cp binancedex:/reports/leaderboard.html leaderboard.html
docker cp binancedex:/reports/stylesheet.css stylesheet.css
```

Finally, the composition can be brought down with `make down`.