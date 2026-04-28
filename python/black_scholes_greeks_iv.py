import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq
from pathlib import Path


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# ------------------------------------------------------------
# 1. Black-Scholes price
# ------------------------------------------------------------

def black_scholes_price(S0, K, T, r, sigma, option_type="call"):
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive.")

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    if option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    raise ValueError("option_type must be 'call' or 'put'.")


# ------------------------------------------------------------
# 2. Black-Scholes Greeks
# ------------------------------------------------------------

def black_scholes_greeks(S0, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    pdf_d1 = norm.pdf(d1)

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (
            -(S0 * pdf_d1 * sigma) / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        )
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)

    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (
            -(S0 * pdf_d1 * sigma) / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        )
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    gamma = pdf_d1 / (S0 * sigma * np.sqrt(T))
    vega = S0 * pdf_d1 * np.sqrt(T)

    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega / 100,      # per 1% volatility move
        "Theta": theta / 365,    # per day
        "Rho": rho / 100         # per 1% rate move
    }


# ------------------------------------------------------------
# 3. Implied volatility solver
# ------------------------------------------------------------

def implied_volatility(market_price, S0, K, T, r, option_type="call"):
    """
    Solve for the volatility that makes Black-Scholes price equal market price.
    """

    def objective(sigma):
        return black_scholes_price(S0, K, T, r, sigma, option_type) - market_price

    try:
        return brentq(objective, 1e-6, 5.0)
    except ValueError:
        return np.nan


# ------------------------------------------------------------
# 4. Plot Greeks vs stock price
# ------------------------------------------------------------

def plot_greeks_vs_stock_price():
    S0_values = np.linspace(50, 150, 200)

    K = 100
    T = 1
    r = 0.05
    sigma = 0.20
    option_type = "call"

    greek_rows = []

    for S0 in S0_values:
        greeks = black_scholes_greeks(S0, K, T, r, sigma, option_type)
        greeks["Stock Price"] = S0
        greek_rows.append(greeks)

    df = pd.DataFrame(greek_rows)

    for greek in ["Delta", "Gamma", "Vega", "Theta", "Rho"]:
        plt.figure(figsize=(10, 5))
        plt.plot(df["Stock Price"], df[greek])
        plt.axvline(K, linestyle="--", label="Strike Price")
        plt.title(f"{greek} vs Stock Price")
        plt.xlabel("Stock Price")
        plt.ylabel(greek)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{greek.lower()}_vs_stock_price.png", dpi=300)
        plt.close()

    df.to_csv(OUTPUT_DIR / "greeks_vs_stock_price.csv", index=False)

    return df


# ------------------------------------------------------------
# 5. Create synthetic market option prices
# ------------------------------------------------------------

def generate_synthetic_option_market():
    """
    Creates a synthetic option chain using a volatility smile.

    This is not real market data. It is used to show how implied volatility
    is recovered from option prices.
    """

    S0 = 100
    r = 0.05
    option_type = "call"

    strikes = np.arange(70, 131, 5)
    maturities = np.array([0.25, 0.5, 1.0, 1.5, 2.0])

    rows = []

    for T in maturities:
        for K in strikes:
            moneyness = K / S0

            # Synthetic smile:
            # volatility is higher for deep OTM/ITM options and lower near ATM.
            true_vol = 0.18 + 0.40 * (moneyness - 1) ** 2 + 0.02 * T

            market_price = black_scholes_price(S0, K, T, r, true_vol, option_type)

            iv = implied_volatility(market_price, S0, K, T, r, option_type)

            rows.append({
                "S0": S0,
                "Strike": K,
                "Maturity": T,
                "Moneyness": moneyness,
                "True Volatility": true_vol,
                "Market Price": market_price,
                "Implied Volatility": iv
            })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "synthetic_option_market_iv.csv", index=False)

    return df


# ------------------------------------------------------------
# 6. Plot volatility smile
# ------------------------------------------------------------

def plot_volatility_smile(iv_df):
    one_year = iv_df[iv_df["Maturity"] == 1.0]

    plt.figure(figsize=(10, 5))
    plt.plot(
        one_year["Strike"],
        one_year["Implied Volatility"],
        marker="o",
        label="1Y Implied Volatility"
    )
    plt.title("Synthetic Volatility Smile")
    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "synthetic_volatility_smile.png", dpi=300)
    plt.close()


# ------------------------------------------------------------
# 7. Plot volatility surface
# ------------------------------------------------------------

def plot_volatility_surface(iv_df):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_trisurf(
        iv_df["Strike"],
        iv_df["Maturity"],
        iv_df["Implied Volatility"],
        linewidth=0.2,
        antialiased=True
    )

    ax.set_title("Synthetic Implied Volatility Surface")
    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity")
    ax.set_zlabel("Implied Volatility")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "synthetic_volatility_surface.png", dpi=300)
    plt.close()


# ------------------------------------------------------------
# 8. Main run
# ------------------------------------------------------------

def main():
    print("\nBLACK-SCHOLES GREEKS AND IMPLIED VOLATILITY EXTENSION")
    print("=" * 70)

    S0 = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.20

    call_price = black_scholes_price(S0, K, T, r, sigma, "call")
    put_price = black_scholes_price(S0, K, T, r, sigma, "put")

    call_greeks = black_scholes_greeks(S0, K, T, r, sigma, "call")
    put_greeks = black_scholes_greeks(S0, K, T, r, sigma, "put")

    print("\nBLACK-SCHOLES PRICES")
    print("-" * 70)
    print(f"Call Price: {call_price:.4f}")
    print(f"Put Price:  {put_price:.4f}")

    print("\nCALL GREEKS")
    print("-" * 70)
    for greek, value in call_greeks.items():
        print(f"{greek}: {value:.6f}")

    print("\nPUT GREEKS")
    print("-" * 70)
    for greek, value in put_greeks.items():
        print(f"{greek}: {value:.6f}")

    # Recover implied volatility from the call price
    recovered_iv = implied_volatility(call_price, S0, K, T, r, "call")
    print("\nIMPLIED VOLATILITY CHECK")
    print("-" * 70)
    print(f"Original volatility:  {sigma:.4f}")
    print(f"Recovered volatility: {recovered_iv:.4f}")

    # Generate outputs
    greeks_df = plot_greeks_vs_stock_price()
    iv_df = generate_synthetic_option_market()
    plot_volatility_smile(iv_df)
    plot_volatility_surface(iv_df)

    print("\nSaved new Greeks and implied volatility outputs to the outputs/ folder.")


if __name__ == "__main__":
    main()