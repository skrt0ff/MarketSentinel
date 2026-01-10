import requests
import pandas as pd


def get_access_token(refresh_token: str) -> str:
    url = "https://be.broker.ru/trade-api-keycloak/realms/tradeapi/protocol/openid-connect/token"

    payload = {
        'client_id': 'trade-api-read',
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()['access_token']


def get_portfolio_df(access_token: str, term_filter: str = 'T365') -> pd.DataFrame:
    url = "https://be.broker.ru/trade-api-bff-portfolio/api/v1/portfolio"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    df = df[df['term'] == term_filter]

    exclude_cols = [
        'subAccountId','agreementId','baseAssetTicker','term','locked',
        'dailyPL','dailyPercentPL','portfolioShare','scale','minimumStep',
        'board','priceUnit','faceValue','accruedIncome','isBlocked',
        'lockedForFutures','ratioQuantity','expireDate','logoLink'
    ]

    df = df.drop(columns=[c for c in exclude_cols if c in df.columns])

    df = df.groupby(list(df.columns), as_index=False).count()

    return df