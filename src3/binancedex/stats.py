import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jinja2 import FileSystemLoader, Environment

from sqlalchemy import or_

from binancedex.api import get_trades
from binancedex.models import Session, Address, Trade
from binancedex.utils import reports_store

log = logging.getLogger(__name__)

BASE_ASSET = 'UND-EBC'
ONE_DAY = 60 * 60 * 24 * 1000


def render():
    """
    Generate the static site

    :return:
    """
    current_script = Path(os.path.abspath(__file__))
    source = current_script.parent / 'templates'

    local_store = reports_store()
    dest = local_store / f'leaderboard.html'
    if dest.exists():
        dest.unlink()

    loader = FileSystemLoader(str(source))
    environment = Environment(loader=loader)

    template = environment.get_template('leaderboard.html')
    context = process_trades()
    dest.write_text(template.render(context))

    orig_style = source / 'stylesheet.css'
    target_css_style = local_store / 'stylesheet.css'
    if target_css_style.exists():
        target_css_style.unlink()

    target_css_style.write_text(orig_style.read_text())


def get_fees(trade):
    buyer_currency, buyer_amount = trade.buyer_fee[0:-1].split(':')
    seller_currency, seller_amount = trade.seller_fee[0:-1].split(':')

    if buyer_currency == 'BNB' and seller_currency == 'BNB':
        return float(buyer_amount), float(seller_amount)
    else:
        # TODO: Fix this slippage
        return 0, 0


def trade_groups_for_address(trader_address):
    f = or_(
        Trade.buyer_id == trader_address,
        Trade.seller_id == trader_address)

    trades = Session.query(Trade).filter(f).order_by(
        Trade.time.desc()).all()

    d = defaultdict(list)
    for trade in trades:
        dt = datetime.utcfromtimestamp(trade.time / 1000)
        d[dt.strftime("%d-%m-%Y")].append(trade)
    return d


def process_trades():
    symbol = f'{BASE_ASSET}_BNB'

    for trade in get_trades(symbol):
        exists = Session.query(Trade).filter_by(
            trade_id=trade['tradeId']).first()
        if not exists:
            trade_obj = Trade.from_trade(trade)
            Session.add(trade_obj)
    Session.commit()

    trade_hist = defaultdict(set)
    total_hist = {}

    all_trades = Session.query(Trade).order_by(Trade.time.desc()).all()

    volume_total = 0
    volume_total_24 = 0
    fee_total = 0

    day_ago = all_trades[0].time - ONE_DAY

    for trade in all_trades:
        if trade.quote_asset != 'BNB':
            raise Exception(f'An unexpected Quote Asset {trade.quote_asset}')

        buyer_address = Address(trade.buyer_id, symbol)
        seller_address = Address(trade.seller_id, symbol)

        exists = Session.query(Address).filter_by(
            address=buyer_address.address).first()
        if not exists:
            Session.add(buyer_address)

        exists = Session.query(Address).filter_by(
            address=seller_address.address).first()
        if not exists:
            Session.add(seller_address)

        buyer_fee, seller_fee = get_fees(trade)
        total = (trade.price * trade.quantity) - (buyer_fee + seller_fee)

        trade_hist[trade.buyer_id].add(trade)
        trade_hist[trade.seller_id].add(trade)

        volume_total = volume_total + total
        fee_total = fee_total + (buyer_fee + seller_fee)
        if trade.time >= day_ago:
            volume_total_24 = volume_total_24 + total

    Session.commit()

    for address, trades in trade_hist.items():
        running_total = 0
        for trade in trades:
            total = trade.price * trade.quantity
            running_total = running_total + total
        total_hist[address] = running_total

    traders = []
    for address, total in total_hist.items():
        traders.append((address, total))
    traders = sorted(traders, key=lambda x: x[1], reverse=True)

    trader_stats = []
    for address, total in traders:
        trader_stats.append({
            'address': address,
            'trade_total': total
        })

    d = {
        'num_trades': len(all_trades),
        'total_volume': volume_total,
        'total_volume_24': volume_total_24,
        'number_of_trades': len(traders),
        'traders': trader_stats,
        'generated_at': datetime.utcnow(),
        'first_trade': datetime.utcfromtimestamp(all_trades[-1].time / 1000),
        'last_trade': datetime.utcfromtimestamp(all_trades[0].time / 1000)
    }
    return d
