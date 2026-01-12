from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bcs import get_access_token, get_portfolio_df
from analytics import analyze_portfolio


app = FastAPI(title="MarketSentinel Backend")


class PortfolioRequest(BaseModel):
    refresh_token: str


@app.post("/portfolio/analyze")
def analyze_portfolio_api(req: PortfolioRequest):
    try:
        access_token = get_access_token(req.refresh_token)
        df = get_portfolio_df(access_token)

        if df.empty:
            return {"message": "Портфель пуст"}

        return analyze_portfolio(df)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))