CREATE TABLE binance.address (
    id SERIAL NOT NULL,
    address TEXT NOT NULL,
    token TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (address)
)

;

CREATE TABLE binance.transaction (
    id SERIAL NOT NULL,
    order_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    cumulate_quantity DOUBLE PRECISION NOT NULL,
    fee TEXT NOT NULL,
    order_create_time TIMESTAMP WITH TIME ZONE,
    transaction_time TIMESTAMP WITH TIME ZONE,
    status TEXT NOT NULL,
    time_in_force SMALLINT NOT NULL,
    side SMALLINT NOT NULL,
    transaction_type SMALLINT NOT NULL,
    trade_id TEXT NOT NULL,
    last_executed_price DOUBLE PRECISION NOT NULL,
    last_executed_quantity DOUBLE PRECISION NOT NULL,
    transaction_hash TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (transaction_hash)
)

;


CREATE TABLE binance.trades (
    id SERIAL NOT NULL,
    trade_id TEXT NOT NULL,
    block_height INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    buyer_order_id TEXT NOT NULL,
    seller_order_id TEXT NOT NULL,
    buyer_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    buyer_fee TEXT NOT NULL,
    seller_fee TEXT NOT NULL,
    base_asset TEXT NOT NULL,
    quote_asset TEXT NOT NULL,
    time BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (trade_id)
)

;

CREATE INDEX ix_binance_trades_buyer_id ON binance.trades (buyer_id);
CREATE INDEX ix_binance_trades_seller_id ON binance.trades (seller_id);
CREATE INDEX ix_binance_address_address ON binance.address (address);
