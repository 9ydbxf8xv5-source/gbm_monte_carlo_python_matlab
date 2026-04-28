# GBM Monte Carlo Option Pricing — Python & MATLAB

## Project Overview

This project extends a basic Brownian motion simulation into a small quantitative finance project.

It simulates stock-price paths using **Geometric Brownian Motion (GBM)**, prices **European call and put options** using Monte Carlo simulation, compares the estimates with **Black-Scholes analytical prices**, and analyses simulation error through confidence intervals and convergence plots.

The project includes both:

- a **Python implementation** for GitHub/CV use;
- a **MATLAB implementation** linked to Computational Methods in Finance coursework.

## Mathematical Model

Under the risk-neutral measure, the stock price is modelled as:

```text
dS_t = r S_t dt + sigma S_t dW_t
```

Using exact GBM discretisation:

```text
S_{t+dt} = S_t * exp((r - 0.5 sigma^2) dt + sigma sqrt(dt) Z)
```

where:

```text
Z ~ N(0, 1)
```

For a European call:

```text
Payoff = max(S_T - K, 0)
```

For a European put:

```text
Payoff = max(K - S_T, 0)
```

The Monte Carlo option price is:

```text
Option Price = exp(-rT) * average(payoff)
```

## Folder Structure

```text
gbm_monte_carlo_python_matlab/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── python/
│   └── gbm_monte_carlo_project.py
│
├── matlab/
│   ├── brownian_motion_basic.m
│   └── gbm_monte_carlo_option_pricing.m
│
├── outputs/
│   └── .gitkeep
│
└── report/
    └── project_summary_template.md
```

## Results and Visualisations

### Pricing Summary

| Option | Black-Scholes Price | Monte Carlo Price | Standard Error | 95% Confidence Interval | Absolute Error |
|---|---:|---:|---:|---:|---:|
| Call | 10.4506 | 10.4898 | 0.0661 | [10.3602, 10.6195] | 0.0393 |
| Put | 5.5735 | 5.5755 | 0.0387 | [5.4996, 5.6514] | 0.0020 |

The Monte Carlo call and put prices are close to the Black-Scholes analytical benchmarks, showing that the simulation is correctly approximating the theoretical option values.

### Simulated GBM Stock-Price Paths

![Simulated GBM paths](outputs/gbm_sample_paths.png)

### Terminal Stock Price Distribution

![Terminal stock distribution](outputs/terminal_stock_distribution.png)

### European Call Payoff Distribution

![Call payoff distribution](outputs/call_payoff_distribution.png)

### Monte Carlo Convergence

![Monte Carlo convergence](outputs/call_convergence.png)

The convergence chart shows the Monte Carlo price approaching the Black-Scholes benchmark as the number of simulated paths increases. The confidence interval narrows as the number of simulations increases, showing the reduction in estimation error.

## Output Data

- [Option pricing summary CSV](outputs/option_pricing_summary.csv)
- [Monte Carlo convergence results CSV](outputs/call_convergence_results.csv)
