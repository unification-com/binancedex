import time

import requests as req

import logging

from binancedex.stats import BASE_ASSET

log = logging.getLogger(__name__)

LISTING_START = '1560988800000'


def address_set():
    url = 'https://explorer.binance.org/api/v1/asset-holders?page=1&rows=5&' \
          'asset=' + BASE_ASSET
    log.debug(url)
    addressData = req.get(url).json()

    totelCount = addressData['totalNum']
    url = 'https://explorer.binance.org/api/v1/asset-holders?page=1&rows=' + \
          str(totelCount) + '&asset=' + BASE_ASSET
    log.debug(url)
    addressData = req.get(url).json()
    assetsHolders = addressData['addressHolders']
    addressSet = set()
    for d in assetsHolders:
        addressSet.add(d['address'])
    return addressSet


def transaction_set(symbol, add):
    """
    I didn't write the function that only consider n minutes before now

    """
    millis = int(round(time.time() * 1000) - (8 * 60 * 60 * 1000))

    url = f'https://dex-atlantic.binance.org/api/v1/orders/closed?address=' \
        f'{add}&start={millis}&symbol={symbol}&limit=500'
    log.debug(url)
    ordersDataBuy = req.get(url).json()
    orders = ordersDataBuy['order']
    return orders


def get_trades(symbol, stop_ts, offset=0):
    """
    I wrote this one

    """
    url = f'https://dex-atlantic.binance.org/api/v1/trades?symbol={symbol}&' \
        f'start={LISTING_START}&stop={stop_ts}&limit=1000&' \
        f'offset={offset}'
    log.debug(url)
    r = req.get(url)
    items = r.json()['trade']
    return items


def get_orders(address):
    """
    And this one

    """
    url = f'https://dex-atlantic.binance.org/api/v1/orders/closed?address=' \
        f'{address}&start={LISTING_START}&symbol=UND-EBC_BNB&limit=500'
    log.info(url)
    r = req.get(url)
    return r.json()['order']
