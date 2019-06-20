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
    orderId = Column(String)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    cumulateQuantity = Column(Float)
    fee = Column(String)
    orderCreateTime = Column(DateTime)
    transactionTime = Column(DateTime)
    status = Column(String)
    timeInForce = Column(Integer)
    side = Column(Integer)
    transactionType = Column(Integer)
    tradeId = Column(String)
    lastExecutedPrice = Column(Float)
    lastExecutedQuantity = Column(Float)
    transactionHash = Column(String)

    def __init__(self, orderId, symbol, price, quantity, cumulateQuantity, fee,
                 orderCreateTime, transactionTime, status, timeInForce, side,
                 transactionType, tradeId, lastExecutedPrice,
                 lastExecutedQuantity, transactionHash):
        self.orderId = orderId
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.cumulateQuantity = cumulateQuantity
        self.fee = fee
        self.orderCreateTime = orderCreateTime
        self.transactionTime = transactionTime
        self.status = status
        self.timeInForce = timeInForce
        self.side = side
        self.transactionType = transactionType
        self.tradeId = tradeId
        self.lastExecutedPrice = lastExecutedPrice
        self.lastExecutedQuantity = lastExecutedQuantity
        self.transactionHash = transactionHash

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
