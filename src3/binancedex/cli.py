import logging
import os
from time import sleep, time

import click

from binancedex.api import get_trades
from binancedex.models import Session, Trade
from binancedex.stats import BASE_ASSET, render

log = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@main.command()
def report():
    """
    Generate a static report

    """
    render()


@main.command()
def fetch_all_trades():
    """
    Exhaustively fetches all the trades
    """

    symbol = f'{BASE_ASSET}_BNB'
    now = int(time() * 1000)

    items = 1000
    offset = 0
    while items == 1000:
        fetch_trades = get_trades(symbol, now, offset=offset)
        for trade in fetch_trades:
            exists = Session.query(Trade).filter_by(
                trade_id=trade['tradeId']).first()
            if not exists:
                trade_obj = Trade.from_trade(trade)
                Session.add(trade_obj)
        Session.commit()

        items = len(fetch_trades)
        offset = offset + items

        sleep(1)


@main.command()
def fetch_latest_trades():
    """
    This one is to be wired into a cron job

    :return:
    """
    symbol = f'{BASE_ASSET}_BNB'
    now = int(time() * 1000)
    fetch_trades = get_trades(symbol, now)

    for trade in fetch_trades:
        exists = Session.query(Trade).filter_by(
            trade_id=trade['tradeId']).first()
        if not exists:
            trade_obj = Trade.from_trade(trade)
            Session.add(trade_obj)
    Session.commit()


if __name__ == "__main__":
    main()
