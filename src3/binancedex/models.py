from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Column, MetaData
from sqlalchemy.types import Integer, String

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
