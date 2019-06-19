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
    transaction_hash TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side BOOLEAN NOT NULL,
    total DOUBLE PRECISION NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    orderCreateTime TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY (id),
    UNIQUE (transaction_hash)
)

;
