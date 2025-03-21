from datetime import datetime
import pandas as pd
import numpy as np

def calculate_loss(
    accident_date: str,
    calculation_date: str,
    annual_earnings: float,
    birth_date: str,
    retirement_age: int = 65,
    ceiling_earnings: float = 100205,
    ceiling_end_date: str = "2039-02-18",
    growth_type: str = "linear",
    discount_rate: float = 0.04,
    contingency: float = 0.15
) -> dict:
    """
    Calculate loss of support (past + future) based on South African actuarial rules.
    """
    accident_dt = datetime.strptime(accident_date, "%Y-%m-%d")
    calc_dt = datetime.strptime(calculation_date, "%Y-%m-%d")
    birth_dt = datetime.strptime(birth_date, "%Y-%m-%d")
    ceiling_end_dt = datetime.strptime(ceiling_end_date, "%Y-%m-%d")

    current_age = (calc_dt - birth_dt).days / 365.25
    retirement_dt = birth_dt.replace(year=birth_dt.year + retirement_age)

    # --- Past Loss ---
    past_years = (calc_dt - accident_dt).days / 365.25
    past_loss = annual_earnings * past_years
    discounted_past_loss = past_loss / ((1 + discount_rate) ** past_years)

    # --- Future Loss ---
    future_years = (retirement_dt - calc_dt).days / 365.25
    if growth_type == "linear":
        earnings_diff = ceiling_earnings - annual_earnings
        annual_growth = earnings_diff / max((ceiling_end_dt - accident_dt).days / 365.25, 1)
        future_loss = 0
        earnings = annual_earnings
        for year in range(int(np.floor(future_years))):
            earnings += annual_growth
            future_loss += earnings / ((1 + discount_rate) ** (year + 1))
    else:
        # No growth
        future_loss = sum([
            annual_earnings / ((1 + discount_rate) ** year)
            for year in range(1, int(np.floor(future_years)) + 1)
        ])

    total_loss = discounted_past_loss + future_loss
    total_loss_after_contingency = total_loss * (1 - contingency)

    return {
        "current_age": round(current_age, 2),
        "past_loss": round(discounted_past_loss, 2),
        "future_loss": round(future_loss, 2),
        "total_loss": round(total_loss, 2),
        "contingency_applied": f"{int(contingency * 100)}%",
        "net_loss": round(total_loss_after_contingency, 2),
    }

def generate_summary(loss_data: dict) -> str:
    return (
        f"At the time of calculation, the claimant is approximately {loss_data['current_age']} years old. "
        f"The past loss of support is estimated at R{loss_data['past_loss']:,}, while the future loss of support "
        f"up to retirement is R{loss_data['future_loss']:,}. This totals to R{loss_data['total_loss']:,}, "
        f"which after applying a {loss_data['contingency_applied']} contingency deduction results in a net loss of R{loss_data['net_loss']:,}."
    )
