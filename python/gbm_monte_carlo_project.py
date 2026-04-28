"""
GBM Monte Carlo Option Pricing Project

This script simulates Geometric Brownian Motion stock-price paths,
prices European call and put options using Monte Carlo simulation,
benchmarks against Black-Scholes prices, and analyses convergence.

Run from the project root:

    python python/gbm_monte_carlo_project.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def black_scholes_price(S0, K, T, r, sigma, option_type="call"):
    """Return the Black-Scholes price of a European call or put."""
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive.")

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == "call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    if option_type.lower() == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    raise ValueError("option_type must be 'call' or 'put'.")


def simulate_gbm_paths(S0, T, r, sigma, n_steps, n_paths, seed=42):
    """
    Simulate stock-price paths using exact risk-neutral GBM discretisation.

    dS_t = r S_t dt + sigma S_t dW_t
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps

    z = rng.standard_normal((n_steps, n_paths))
    log_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    log_paths = np.vstack([np.zeros(n_paths), np.cumsum(log_increments, axis=0)])

    paths = S0 * np.exp(log_paths)
    time_grid = np.linspace(0, T, n_steps + 1)

    return time_grid, paths


def monte_carlo_option_price(S0, K, T, r, sigma, n_steps, n_paths, option_type="call", seed=42):
    """Price a European option by Monte Carlo simulation."""
    _, paths = simulate_gbm_paths(S0, T, r, sigma, n_steps, n_paths, seed=seed)
    terminal_prices = paths[-1]

    if option_type.lower() == "call":
        payoffs = np.maximum(terminal_prices - K, 0.0)
    elif option_type.lower() == "put":
        payoffs = np.maximum(K - terminal_prices, 0.0)
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    discounted_payoffs = np.exp(-r * T) * payoffs

    price = discounted_payoffs.mean()
    std_error = discounted_payoffs.std(ddof=1) / np.sqrt(n_paths)
    ci_low = price - 1.96 * std_error
    ci_high = price + 1.96 * std_error

    return {
        "price": price,
        "std_error": std_error,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "payoffs": payoffs,
        "discounted_payoffs": discounted_payoffs,
        "terminal_prices": terminal_prices,
        "paths": paths,
    }


def monte_carlo_antithetic_price(S0, K, T, r, sigma, n_steps, n_paths, option_type="call", seed=42):
    """
    Price a European option using antithetic variates.

    For every normal draw Z, the simulation also uses -Z.
    """
    if n_paths % 2 != 0:
        n_paths += 1

    rng = np.random.default_rng(seed)
    dt = T / n_steps
    half_paths = n_paths // 2

    z = rng.standard_normal((n_steps, half_paths))
    z_antithetic = -z

    def terminal_prices(z_matrix):
        log_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z_matrix
        return S0 * np.exp(np.sum(log_increments, axis=0))

    st_1 = terminal_prices(z)
    st_2 = terminal_prices(z_antithetic)
    st = np.concatenate([st_1, st_2])

    if option_type.lower() == "call":
        payoffs = np.maximum(st - K, 0.0)
    elif option_type.lower() == "put":
        payoffs = np.maximum(K - st, 0.0)
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    discounted_payoffs = np.exp(-r * T) * payoffs

    price = discounted_payoffs.mean()
    std_error = discounted_payoffs.std(ddof=1) / np.sqrt(n_paths)

    return {
        "price": price,
        "std_error": std_error,
        "ci_low": price - 1.96 * std_error,
        "ci_high": price + 1.96 * std_error,
    }


def convergence_analysis(S0, K, T, r, sigma, n_steps, path_counts, option_type="call"):
    """Calculate Monte Carlo prices across increasing numbers of paths."""
    benchmark = black_scholes_price(S0, K, T, r, sigma, option_type)
    rows = []

    for n_paths in path_counts:
        result = monte_carlo_option_price(S0, K, T, r, sigma, n_steps, n_paths, option_type, seed=42)
        rows.append(
            {
                "n_paths": n_paths,
                "monte_carlo_price": result["price"],
                "black_scholes_price": benchmark,
                "std_error": result["std_error"],
                "ci_low": result["ci_low"],
                "ci_high": result["ci_high"],
                "absolute_error": abs(result["price"] - benchmark),
            }
        )

    return pd.DataFrame(rows)


def plot_sample_paths(time_grid, paths, max_paths=100):
    plt.figure(figsize=(10, 5))
    for i in range(min(max_paths, paths.shape[1])):
        plt.plot(time_grid, paths[:, i], linewidth=0.8, alpha=0.7)
    plt.title("Simulated Risk-Neutral GBM Stock-Price Paths")
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "gbm_sample_paths.png", dpi=300)
    plt.show()


def plot_terminal_distribution(terminal_prices, S0):
    plt.figure(figsize=(10, 5))
    plt.hist(terminal_prices, bins=60, edgecolor="black", alpha=0.75)
    plt.axvline(S0, linestyle="--", label="Initial Stock Price")
    plt.title("Distribution of Terminal Stock Prices")
    plt.xlabel("Terminal Stock Price")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "terminal_stock_distribution.png", dpi=300)
    plt.show()


def plot_payoff_distribution(payoffs, option_type):
    plt.figure(figsize=(10, 5))
    plt.hist(payoffs, bins=60, edgecolor="black", alpha=0.75)
    plt.title(f"Distribution of European {option_type.capitalize()} Payoffs")
    plt.xlabel("Payoff")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"{option_type}_payoff_distribution.png", dpi=300)
    plt.show()


def plot_convergence(convergence_df, option_type):
    plt.figure(figsize=(10, 5))
    plt.plot(
        convergence_df["n_paths"],
        convergence_df["monte_carlo_price"],
        marker="o",
        label="Monte Carlo Price",
    )
    plt.axhline(
        convergence_df["black_scholes_price"].iloc[0],
        linestyle="--",
        label="Black-Scholes Benchmark",
    )
    plt.fill_between(
        convergence_df["n_paths"],
        convergence_df["ci_low"],
        convergence_df["ci_high"],
        alpha=0.2,
        label="95% Confidence Interval",
    )
    plt.xscale("log")
    plt.title(f"Monte Carlo Convergence: European {option_type.capitalize()} Option")
    plt.xlabel("Number of Simulation Paths")
    plt.ylabel("Option Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"{option_type}_convergence.png", dpi=300)
    plt.show()


def main():
    # Base parameters
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.05
    sigma = 0.20
    n_steps = 252
    n_paths = 50_000

    print("\nGBM MONTE CARLO OPTION PRICING PROJECT")
    print("=" * 60)
    print(f"S0={S0}, K={K}, T={T}, r={r}, sigma={sigma}, steps={n_steps}, paths={n_paths}")

    time_grid, paths = simulate_gbm_paths(S0, T, r, sigma, n_steps, n_paths)

    call_mc = monte_carlo_option_price(S0, K, T, r, sigma, n_steps, n_paths, "call")
    put_mc = monte_carlo_option_price(S0, K, T, r, sigma, n_steps, n_paths, "put")
    call_bs = black_scholes_price(S0, K, T, r, sigma, "call")
    put_bs = black_scholes_price(S0, K, T, r, sigma, "put")
    call_anti = monte_carlo_antithetic_price(S0, K, T, r, sigma, n_steps, n_paths, "call")

    summary = pd.DataFrame(
        [
            {
                "option": "call",
                "black_scholes": call_bs,
                "monte_carlo": call_mc["price"],
                "std_error": call_mc["std_error"],
                "ci_low": call_mc["ci_low"],
                "ci_high": call_mc["ci_high"],
                "absolute_error": abs(call_mc["price"] - call_bs),
            },
            {
                "option": "put",
                "black_scholes": put_bs,
                "monte_carlo": put_mc["price"],
                "std_error": put_mc["std_error"],
                "ci_low": put_mc["ci_low"],
                "ci_high": put_mc["ci_high"],
                "absolute_error": abs(put_mc["price"] - put_bs),
            },
        ]
    )

    print("\nPRICING SUMMARY")
    print("-" * 60)
    print(summary.to_string(index=False))

    print("\nANTITHETIC VARIATES CHECK")
    print("-" * 60)
    print(f"Standard MC call price:        {call_mc['price']:.4f}")
    print(f"Standard MC standard error:    {call_mc['std_error']:.6f}")
    print(f"Antithetic MC call price:      {call_anti['price']:.4f}")
    print(f"Antithetic MC standard error:  {call_anti['std_error']:.6f}")

    path_counts = [100, 500, 1_000, 5_000, 10_000, 25_000, 50_000, 100_000]
    convergence = convergence_analysis(S0, K, T, r, sigma, n_steps, path_counts, "call")

    print("\nCONVERGENCE TABLE")
    print("-" * 60)
    print(convergence.to_string(index=False))

    summary.to_csv(OUTPUT_DIR / "option_pricing_summary.csv", index=False)
    convergence.to_csv(OUTPUT_DIR / "call_convergence_results.csv", index=False)

    plot_sample_paths(time_grid, paths, max_paths=100)
    plot_terminal_distribution(call_mc["terminal_prices"], S0)
    plot_payoff_distribution(call_mc["payoffs"], "call")
    plot_convergence(convergence, "call")

    print(f"\nSaved charts and CSV files to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
