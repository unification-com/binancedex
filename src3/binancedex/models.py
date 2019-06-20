from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Column, MetaData
from sqlalchemy.types import Integer, String, Float, DateTime

engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')

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
        self.cumulate_quantity = float(cumulateQuantity)
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
