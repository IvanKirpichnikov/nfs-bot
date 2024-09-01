profile-menu =
    <b>Профиль</b>

    Имя: <b>{ $name }</b>
    Выбранная валюта: <b>{ $currency }</b>
    Общая сумма NFT коллекции: { $currency_type ->
        [rub] <b>{NUMBER($total_price, style: "currency", currency: "RUB" )}</b>
        [usd] <b>{NUMBER($total_price, style: "currency", currency: "USD" )}</b>
        *[other] Неизвестная валюта <b>{ $currency_type }</b>
    }
