import pandas as pd


def analyze_portfolio(df: pd.DataFrame, top_n=3) -> dict:
    total_balance = df['balanceValueRub'].sum()
    total_current = df['currentValueRub'].sum()
    total_pl = df['unrealizedPL'].sum()

    total_return_pct = (total_pl / total_balance * 100) if total_balance else 0

    summary = {
        "total_balance_rub": round(total_balance, 2),
        "total_current_rub": round(total_current, 2),
        "total_pl_rub": round(total_pl, 2),
        "total_return_pct": round(total_return_pct, 2)
    }

    alloc_instr = df[['ticker','displayName','currentValueRub']].copy()
    alloc_instr['share_pct'] = (
        alloc_instr['currentValueRub'] / alloc_instr['currentValueRub'].sum() * 100
    ).round(2)

    alloc_currency = (
        df.groupby('currency')['currentValueRub']
        .sum()
        .reset_index()
    )

    worst = df.sort_values('unrealizedPL').head(top_n)
    best = df.sort_values('unrealizedPL', ascending=False).head(top_n)

    return {
        "summary": summary,
        "allocation_by_instrument": alloc_instr.to_dict(orient="records"),
        "allocation_by_currency": alloc_currency.to_dict(orient="records"),
        "top_positions": {
            "best": best[['ticker','displayName','unrealizedPL','unrealizedPercentPL']].to_dict(orient="records"),
            "worst": worst[['ticker','displayName','unrealizedPL','unrealizedPercentPL']].to_dict(orient="records")
        }
    }