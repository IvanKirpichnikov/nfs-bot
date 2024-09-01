CREATE TYPE PROFILE_CURRENCY_TYPE AS ENUM('usd', 'rub');
CREATE TABLE IF NOT EXISTS profile(
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(25) NOT NULL,
    tg_user_id BIGINT NOT NULL,
    tg_chat_id BIGINT NOT NULL,
    currency_type PROFILE_CURRENCY_TYPE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TYPE NFT_CURRENCY_TYPE AS ENUM('usd', 'rub');
CREATE TYPE NFT_CRYPTO_CURRENCY_TYPE AS ENUM('tron', 'sol', 'eth');
CREATE TABLE IF NOT EXISTS nft(
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    profile_id INTEGER NOT NULL,
    name VARCHAR(25) NOT NULL,
    price NUMERIC NOT NULL,
    description VARCHAR(400),
    currency NFT_CURRENCY_TYPE NOT NULL,
    crypto_currency NFT_CRYPTO_CURRENCY_TYPE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

