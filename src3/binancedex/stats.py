import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from time import time


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
    """
    Fees can be a little bit complicated:

    These are probably fees for cancelled trades
    #Cxl:1;BNB:0.00010432;

    :return:
    """
    try:
        if trade.buyer_fee[:7] == '#Cxl:1;' or \
                trade.buyer_fee[:7] == '#Cxl:2;':
            buyer_fee = trade.buyer_fee[7:]
        else:
            buyer_fee = trade.buyer_fee

        if trade.seller_fee[:7] == '#Cxl:1;' or \
                trade.seller_fee[:7] == '#Cxl:2;':
            seller_fee = trade.seller_fee[7:]
        else:
            seller_fee = trade.seller_fee

        buyer_currency, buyer_amount = buyer_fee[0:-1].split(':')
        seller_currency, seller_amount = seller_fee[0:-1].split(':')

        slippage = 0
        if buyer_currency == 'BNB':
            buyer_ret = float(buyer_amount)
        else:
            if buyer_currency != 'UND-EBC':
                raise Exception('Unhandled currency')
            slippage = slippage + float(buyer_amount)
            buyer_ret = 0

        if seller_currency == 'BNB':
            seller_ret = float(buyer_amount)
        else:
            if seller_currency != 'UND-EBC':
                raise Exception('Unhandled currency')
            slippage = slippage + float(buyer_amount)
            seller_ret = 0

        return buyer_ret, seller_ret, slippage
    except Exception as e:
        # Don't crash while trying to calculate fees that we don't use
        log.error(e)
        return 0, 0, 0


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

    return {
        'days': d,
        'address': trader_address
    }


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
    total_fees = 0
    total_fee_slippage = 0

    now = int(time() * 1000)
    day_ago = now - ONE_DAY

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

        buyer_fee, seller_fee, slippage = get_fees(trade)
        total_fee_slippage = total_fee_slippage + slippage
        total_fees = total_fees + (buyer_fee + seller_fee)
        total = (trade.price * trade.quantity)

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
        'total_fees': total_fees,
        'total_slippage': total_fee_slippage,
        'traders': trader_stats,
        'generated_at': datetime.utcnow(),
        'first_trade': datetime.utcfromtimestamp(all_trades[-1].time / 1000),
        'last_trade': datetime.utcfromtimestamp(all_trades[0].time / 1000)
    }
    return d
