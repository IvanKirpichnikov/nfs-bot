my-nft = Мои NFT
nft-created = NFT создано
add-nft = Добавить NFT
pagination-nft = Выбери свое NFT
nft-name-invalid-length =
    Длина(<b>{ $length }</b>) имени NFT должна быть меньше <b>25 символов</b>.
nft-price-invalid-value =
    Цена была отправлена не в правильном формате.
    Отправь цену в следующем формате. <b>100</b> или <b>100.15</b>.
nft-price-invalid-length =
    Цена NFT должна быть меньше <b>1000000</b> или больше <b>1</b>
nft-description-invalid-length = Длина(<b>{ $length }</b>) описания NFT должна быть меньше <b>400 символов</b>.

add-nft-menu =
    Название: <b>{ $name }</b>
    Цена: { $currency_type ->
        [rub] <b>{ NUMBER($price, style: "currency", currency: "RUB" ) }</b>
        [usd] <b>{ NUMBER($price, style: "currency", currency: "USD" ) }</b>
        [None] <b>{ $price }</b>
        *[other] Неизвестная валюта <b>{ $currency_type }</b>
    } { $crypto_currency ->
        [None] {""}
        *[other] (<b>{ $crypto_price } { $crypto_currency }</b>)
    }
    Блокчейн: <b>{ $crypto_currency_type }</b>
    Описание: { $description }

edit-nft-menu =
    Название: <b>{ $name }</b>
    Цена: { $currency_type ->
        [rub] <b>{ NUMBER($price, style: "currency", currency: "RUB" ) }</b>
        [usd] <b>{ NUMBER($price, style: "currency", currency: "USD" ) }</b>
        [None] <b>{ $price }</b>
        *[other] Неизвестная валюта <b>{ $currency_type }</b>
    }(<b>{ $crypto_price } { $crypto_currency_type }</b>)
    Блокчейн: <b>{ $crypto_currency_type }</b>
    Отправь новое описание, чтобы изменить его.
    Описание: { $description }

