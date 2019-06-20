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
    cumulateQuantity DOUBLE PRECISION NOT NULL,
    fee TEXT NOT NULL,
    orderCreateTime TIMESTAMP WITH TIME ZONE,
    transactionTime TIMESTAMP WITH TIME ZONE,
    status TEXT NOT NULL,
    timeInForce SMALLINT NOT NULL,
    side SMALLINT NOT NULL,
    transactionType SMALLINT NOT NULL,
    tradeId TEXT NOT NULL,
    lastExecutedPrice DOUBLE PRECISION NOT NULL,
    lastExecutedQuantity DOUBLE PRECISION NOT NULL,
    transaction_hash TEXT NOT NULL

    PRIMARY KEY (id),
    UNIQUE (transaction_hash)
)

;
