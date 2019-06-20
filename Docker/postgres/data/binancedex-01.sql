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
