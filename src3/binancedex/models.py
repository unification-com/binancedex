from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Column, MetaData
from sqlalchemy.types import Integer, String, Float, DateTime, BigInteger

from binancedex.utils import get_enum, Environment

environ = get_enum()
if environ == Environment.LAPTOP:
    engine = create_engine(
        'postgresql://postgres:password@localhost:8432/postgres')
if environ == Environment.DOCKER:
    engine = create_engine(
        'postgresql://postgres:password@postgres:5432/postgres')

SCHEMA_NAME = 'binance'

Base = declarative_base(bind=engine, metadata=MetaData(schema=SCHEMA_NAME))
Session = scoped_session(sessionmaker(engine))


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    token = Column(String)

    def __init__(self, address, token):
        self.address = address
        self.token = token


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    trade_id = Column(String)
    block_height = Column(Integer)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    buyer_order_id = Column(String)
    seller_order_id = Column(String)
    buyer_id = Column(String)
    seller_id = Column(String)
    buyer_fee = Column(String)
    seller_fee = Column(String)
    base_asset = Column(String)
    quote_asset = Column(String)
    time = Column(BigInteger)

    def __init__(self, trade_id, block_height, symbol, price, quantity,
                 buyer_order_id,
                 seller_order_id, buyer_id, seller_id, buyer_fee, seller_fee,
                 base_asset, quote_asset, time):
        self.block_height = block_height
        self.seller_order_id = seller_order_id
        self.buyer_order_id = buyer_order_id
        self.quantity = quantity
        self.price = price
        self.symbol = symbol
        self.trade_id = trade_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.buyer_fee = buyer_fee
        self.seller_fee = seller_fee
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.time = time

    @staticmethod
    def from_trade(t):
        trade = Trade(t['tradeId'], t['blockHeight'], t['symbol'], t['price'],
                      t['quantity'], t['buyerOrderId'], t['sellerOrderId'],
                      t['buyerId'], t['sellerId'], t['buyFee'], t['sellFee'],
                      t['baseAsset'], t['quoteAsset'], t['time'])
        return trade


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    order_id = Column(String)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    cumulate_quantity = Column(Float)
    fee = Column(String)
    order_create_time = Column(DateTime)
    transaction_time = Column(DateTime)
    status = Column(String)
    time_in_force = Column(Integer)
    side = Column(Integer)
    transaction_type = Column(Integer)
    trade_id = Column(String)
    last_executed_price = Column(Float)
    last_executed_quantity = Column(Float)
    transaction_hash = Column(String)

    def __init__(self, orderId, symbol, price, quantity, cumulateQuantity, fee,
                 orderCreateTime, transactionTime, status, timeInForce, side,
                 transactionType, tradeId, lastExecutedPrice,
                 lastExecutedQuantity, transactionHash):
        self.order_id = orderId
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.cumulate_quantity = cumulateQuantity
        self.fee = fee
        self.order_create_time = orderCreateTime
        self.transaction_time = transactionTime
        self.status = status
        self.time_in_force = timeInForce
        self.side = side
        self.transaction_type = transactionType
        self.trade_id = tradeId
        self.last_executed_price = lastExecutedPrice
        self.last_executed_quantity = lastExecutedQuantity
        self.transaction_hash = transactionHash

    @staticmethod
    def from_order(o):
        transaction = Transaction(o['orderId'], o['symbol'], o['price'],
                                  o['quantity'],
                                  o['cumulateQuantity'], o['fee'],
                                  o['orderCreateTime'],
                                  o['transactionTime'], o['status'],
                                  o['timeInForce'],
                                  o['side'], o['type'], o['tradeId'],
                                  o['lastExecutedPrice'],
                                  o['lastExecutedQuantity'],
                                  o['transactionHash'])
        return transaction
