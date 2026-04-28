# Project Explanation: Geomatric Brownian Motion Monte Carlo Option Pricing Engine

## 1. Project Overview

This project is a quantitative finance implementation of a Monte Carlo option-pricing engine using Geometric Brownian Motion (GBM).

The aim is to simulate possible future stock-price paths under the risk-neutral measure, calculate European option payoffs at maturity, discount those expected payoffs back to the present, and compare the Monte Carlo estimates against the closed-form Black-Scholes benchmark.

The project includes both:

- a Python implementation, designed for GitHub and future quant project development;
- a MATLAB implementation, linked to Brownian motion simulation work from my Computational Methods in Finance module.

The project covers:

- Brownian motion simulation
- Geometric Brownian Motion stock-price modelling
- risk-neutral derivative pricing
- European call and put valuation
- Monte Carlo estimation
- Black-Scholes benchmark comparison
- standard errors and confidence intervals
- convergence analysis
- antithetic variates as a variance-reduction method
- visualisation of simulated paths, payoff distributions and convergence behaviour

The project is designed as a first quantitative finance project: simple enough to explain clearly, but complete enough to demonstrate stochastic modelling, numerical simulation, option pricing, coding, and financial interpretation.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 2. Motivation

The motivation behind this project is to connect theoretical financial mathematics with computational implementation.

In financial mathematics, asset prices are commonly modelled as stochastic processes because market prices evolve under uncertainty. One of the most important models is Geometric Brownian Motion, which is the stock-price model underlying Black-Scholes option pricing.

Although Black-Scholes gives an analytical solution for European options, many more complex derivatives do not have closed-form solutions. In those cases, Monte Carlo simulation is useful because it estimates derivative prices by simulating many possible future asset paths and averaging the discounted payoff.

This project therefore demonstrates:

1. understanding of Brownian motion and GBM;
2. implementation of Monte Carlo simulation;
3. use of risk-neutral pricing;
4. comparison of numerical results with an analytical benchmark;
5. interpretation of convergence and simulation error.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Brownian Motion

The starting point is Brownian motion, also known as a Wiener process.

A standard Brownian motion \( W_t \) satisfies:

1. \( W_0 = 0 \)
2. \( W_t \) has independent increments
3. \( W_t - W_s \sim N(0, t-s) \) for \( t > s \)
4. paths are continuous
5. increments are normally distributed

For a small time step \( \Delta t \), the Brownian increment can be simulated as:

\[
\Delta W_t = \sqrt{\Delta t}Z
\]

where:

\[
Z \sim N(0,1)
\]

The Brownian path is then built recursively:

\[
W_{t+\Delta t} = W_t + \Delta W_t
\]

This was the starting point for the MATLAB version of the project.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 4. From Brownian Motion to Geometric Brownian Motion

Brownian motion itself can take negative values, so it is not directly suitable for modelling stock prices. Stock prices must remain positive.

The Black-Scholes framework therefore models stock prices using Geometric Brownian Motion:

\[
dS_t = \mu S_tdt + \sigma S_tdW_t
\]

where:

- \( S_t \) is the stock price at time \( t \)
- \( \mu \) is the expected return
- \( \sigma \) is volatility
- \( W_t \) is Brownian motion

For option pricing, we use the risk-neutral measure, where the expected return \( \mu \) is replaced by the risk-free rate \( r \):

\[
dS_t = rS_tdt + \sigma S_tdW_t
\]

The exact discretisation used in the project is:

\[
S_{t+\Delta t}
=
S_t \exp\left((r-\frac{1}{2}\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z\right)
\]

where:

\[
Z \sim N(0,1)
\]

This formula is used to simulate the stock-price paths.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 5. Risk-Neutral Pricing

The project uses the risk-neutral pricing formula.

For a derivative with payoff \( V_T \) at maturity \( T \), the time-0 value is:

\[
V_0 = e^{-rT}\mathbb{E}^{Q}[V_T]
\]

where:

- \( \mathbb{E}^{Q} \) is the expectation under the risk-neutral measure;
- \( e^{-rT} \) is the discount factor;
- \( V_T \) is the payoff at maturity.

For a European call option:

\[
V_T = \max(S_T-K,0)
\]

For a European put option:

\[
V_T = \max(K-S_T,0)
\]

The Monte Carlo price is obtained by averaging simulated discounted payoffs:

\[
V_0 \approx e^{-rT}\frac{1}{N}\sum_{i=1}^{N}V_T^{(i)}
\]

where \( N \) is the number of simulated paths.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 6. Monte Carlo Pricing Method

The Monte Carlo procedure is:

1. Choose input parameters:
   - initial stock price \( S_0 \)
   - strike price \( K \)
   - maturity \( T \)
   - risk-free rate \ ( r \)
   - volatility \( \sigma \)
   - number of time steps
   - number of simulated paths

2. Simulate many stock-price paths under risk-neutral GBM.

3. Extract the terminal stock prices \( S_T \).

4. Calculate European option payoffs:

\[
\text{Call payoff} = \max(S_T-K,0)
\]

\[
\text{Put payoff} = \max(K-S_T,0)
\]

5. Discount the average payoff back to time 0.

6. Compare the Monte Carlo estimate with the Black-Scholes analytical price.

7. Calculate standard error and confidence intervals.

8. Analyse convergence as the number of simulated paths increases.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 7. Black-Scholes Benchmark

The Black-Scholes formula provides an analytical benchmark for European call and put options.

For a European call:

\[
C = S_0N(d_1)-Ke^{-rT}N(d_2)
\]

For a European put:

\[
P = Ke^{-rT}N(-d_2)-S_0N(-d_1)
\]

where:

\[
d_1 =
\frac{\ln(S_0/K)+(r+\frac{1}{2}\sigma^2)T}
{\sigma\sqrt{T}}
\]

\[
d_2 = d_1-\sigma\sqrt{T}
\]

and \( N(\cdot) \) is the standard normal cumulative distribution function.

The project compares the Monte Carlo option prices against the Black-Scholes values. Since both methods price the same European options under the same assumptions, the Monte Carlo values should converge toward the Black-Scholes benchmarks as the number of simulations increases.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 8. Parameters Used

The base project uses the following benchmark parameters:

```text
Initial stock price, S0       = 100
Strike price, K               = 100
Time to maturity, T           = 1 year
Risk-free rate, r             = 5%
Volatility, sigma             = 20%
Number of time steps          = 252
Number of Monte Carlo paths   = 50,000
```

The option is at-the-money because:

\[
S_0 = K = 100
\]

The use of 252 time steps represents daily trading days over one year.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 9. Python Implementation

The Python implementation is the main version of the project.

It contains several core components:

### 9.1 Black-Scholes Function

The function `black_scholes_price()` calculates the analytical Black-Scholes price for either a European call or put.

Inputs:

```python
S0, K, T, r, sigma, option_type
```

Output:

```python
option_price
```

This function provides the theoretical benchmark for the Monte Carlo simulation.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 9.2 GBM Path Simulation

The function `simulate_gbm_paths()` simulates risk-neutral GBM paths.

It generates standard normal random variables:

```python
Z = rng.standard_normal((n_steps, n_paths))
```

Then calculates log increments:

```python
log_increments = (r - 0.5 * sigma2) * dt + sigma * np.sqrt(dt) * Z
```

The cumulative sum creates the log-stock path:

```python
log_paths = np.cumsum(log_increments, axis=0)
```

Exponentiating gives simulated stock prices:

```python
paths = S0 * np.exp(log_paths)
```

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 9.3 Monte Carlo Option Pricing

The function `monte_carlo_option_price()` calculates the Monte Carlo price.

It takes terminal stock prices:

```python
terminal_prices = paths[-1]
```

Then calculates payoffs.

For a call:

```python
payoffs = np.maximum(terminal_prices - K, 0)
```

For a put:

```python
payoffs = np.maximum(K - terminal_prices, 0)
```

Then discounts the payoffs:

```python
discounted_payoffs = np.exp(-r * T) * payoffs
```

The Monte Carlo price is:

```python
price = discounted_payoffs.mean()
```

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 10. Standard Error and Confidence Intervals

Monte Carlo simulation produces an estimate, not an exact value.

The standard error is calculated as:

\[
SE = \frac{\sigma_{\text{payoff}}}{\sqrt{N}}
\]

where:

- \( \sigma_{\text{payoff}} \) is the standard deviation of discounted payoffs;
- \( N \) is the number of simulated paths.

A 95% confidence interval is calculated as:

\[
\text{Price} \pm 1.96 \times SE
\]

This shows the uncertainty around the Monte Carlo estimate.

Including standard errors and confidence intervals strengthens the project because it demonstrates that the Monte Carlo result is treated as a statistical estimate rather than an exact number.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 11. Convergence Analysis

The project tests how the Monte Carlo price changes as the number of simulated paths increases.

The path counts used are:

```text
100
500
1,000
5,000
10,000
25,000
50,000
100,000
```

For each number of paths, the project calculates:

- Monte Carlo option price
- Black-Scholes benchmark
- standard error
- 95% confidence interval
- absolute error

The convergence chart shows the Monte Carlo estimate approaching the Black-Scholes benchmark as the number of simulations increases.

This is consistent with the law of large numbers: as the sample size increases, the average simulated payoff should converge toward the true expected payoff.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 12. Antithetic Variates

The project includes antithetic variates as a basic variance-reduction technique.

In standard Monte Carlo, the simulation uses random normal draws \( Z \).

With antithetic variates, for every draw \( Z \), the simulation also uses:

\[
-Z
\]

This pairs positive and negative shocks.

The idea is that high and low outcomes partially offset each other, reducing the variance of the estimator.

The project compares:

- standard Monte Carlo price and standard error;
- antithetic Monte Carlo price and standard error.

This demonstrates awareness of variance reduction, which is important in computational finance.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 13. MATLAB Implementation

The MATLAB version has two parts.

### 13.1 Basic Brownian Motion Simulation

The file `brownian_motion_basic.m` simulates discretised Brownian motion using:

\[
dW = \sqrt{dt}Z
\]

and:

\[
W_j = W_{j-1}+dW_j
\]

This recreates the Brownian motion simulation studied in Computational Methods in Finance.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 13.2 GBM Monte Carlo Option Pricing

The file `gbm_monte_carlo_option_pricing.m` extends the Brownian motion simulation into a full option-pricing model.

It includes:

- GBM stock-path simulation
- European call and put payoff calculation
- Monte Carlo pricing
- Black-Scholes benchmark comparison
- standard errors
- confidence intervals
- convergence analysis
- antithetic variates
- saved output charts

The MATLAB implementation shows the academic foundation of the project, while the Python version is more suitable for GitHub, project expansion and future quantitative research.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 14. Visual Outputs

The project generates several visual outputs.

### 14.1 Simulated GBM Stock-Price Paths

This chart shows multiple simulated stock-price paths over one year.

Each path represents one possible future evolution of the stock price under risk-neutral GBM.

The paths spread out over time because uncertainty increases over longer horizons.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 14.2 Terminal Stock-Price Distribution

This histogram shows the distribution of terminal stock prices \( S_T \).

Under GBM, terminal stock prices are lognormally distributed. This means:

- prices remain positive;
- the distribution is right-skewed;
- large upside moves are possible;
- downside is bounded by zero.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 14.3 European Call Payoff Distribution

This histogram shows the distribution of European call payoffs:

\[
\max(S_T-K,0)
\]

Many payoffs are zero when the option finishes out-of-the-money.

Positive payoffs occur when:

\[
S_T > K
\]

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 14.4 Monte Carlo Convergence Chart

This chart shows the Monte Carlo call price as the number of simulated paths increases.

It also includes:

- the Black-Scholes benchmark;
- the 95% confidence interval.

This is one of the most important charts because it shows that the Monte Carlo estimate behaves as expected and moves toward the theoretical value as simulation size increases.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 15. Results Interpretation

The Monte Carlo call and put prices are close to the Black-Scholes benchmark values.

This shows that the simulation is correctly approximating the theoretical option prices.

The convergence chart shows that:

- with a small number of paths, the Monte Carlo estimate is noisy;
- as the number of paths increases, the estimate becomes more stable;
- the confidence interval narrows as simulation size increases;
- the estimate moves closer to the Black-Scholes analytical price.

The standard error decreases as the number of paths increases because:

\[
SE \propto \frac{1}{\sqrt{N}}
\]

This is consistent with Monte Carlo theory.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 16. Why This Project Is Relevant to Quantitative Finance

This project is relevant to quantitative finance because it combines:

- stochastic processes
- Brownian motion
- Geometric Brownian Motion
- derivative pricing
- risk-neutral valuation
- numerical simulation
- statistical estimation
- Python
- MATLAB
- model validation
- financial interpretation

These are important foundations for:

- derivatives pricing
- quant research
- model validation
- risk management
- volatility modelling
- computational finance
- systematic trading research

Although the model is simple, it provides the base for more advanced work such as exotic option pricing, implied volatility modelling, volatility surfaces and statistical trading strategies.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 17. Limitations

### 17.1 Constant Volatility

The model assumes volatility is constant.

In real markets, volatility changes through time and differs across strikes and maturities.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 17.2 No Jumps

GBM assumes continuous price paths.

Real markets can experience jumps due to earnings announcements, macroeconomic data, central bank decisions, geopolitical events or liquidity shocks.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 17.3 European Options Only

The project prices European options, which can only be exercised at maturity.

American options require different numerical methods, such as:

- binomial trees
- finite-difference methods
- regression-based Monte Carlo

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 17.4 No Transaction Costs or Liquidity Effects

The model ignores:

- transaction costs
- bid-ask spreads
- liquidity
- execution risk
- market impact

These matter in real trading.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 17.5 No Calibration to Market Data

The base model uses fixed input parameters rather than calibrating volatility from real market option prices.

A more advanced version would use real option-chain data to estimate implied volatility.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 17.6 Black-Scholes Assumptions

The Black-Scholes framework assumes:

- lognormal stock prices
- constant volatility
- constant risk-free rate
- continuous trading
- frictionless markets
- no jumps
- European exercise

These assumptions are useful for a benchmark model but are simplified relative to real markets.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 18. Future Improvements

### 18.1 Add Greeks

Future versions can calculate:

- Delta
- Gamma
- Vega
- Theta
- Rho

These measure the sensitivity of the option price to changes in underlying price, volatility, time and interest rates.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 18.2 Add Implied Volatility

The project can be extended by solving for implied volatility from market option prices.

This would connect theoretical pricing with real market data.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 18.3 Build a Volatility Smile and Surface

Using implied volatility across strikes and maturities, the project can be extended to plot:

- volatility smiles
- volatility skews
- volatility surfaces

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 18.4 Price Exotic Options

Monte Carlo simulation is especially useful for path-dependent options.

Future extensions could price:

- Asian options
- barrier options
- lookback options

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 18.5 Compare Exact GBM with Euler-Maruyama

The current project uses exact GBM discretisation.

An extension could compare this with Euler-Maruyama discretisation and analyse discretisation error.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 18.6 Use Real Market Data

The project could be calibrated using:

- real stock prices
- real option-chain data
- implied volatility data

This would make the project closer to institutional quantitative finance work.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 19. Key Learning Outcomes

This project helped develop understanding of:

1. how Brownian motion is simulated computationally
2. how Brownian motion leads to Geometric Brownian Motion
3. how GBM is used in the Black-Scholes framework
4. why risk-neutral pricing uses the risk-free rate as drift
5. how European option payoffs are calculated
6. how Monte Carlo simulation estimates discounted expected payoffs
7. how to compare numerical estimates against analytical benchmarks
8. how to calculate standard errors and confidence intervals
9. how Monte Carlo convergence behaves
10. how variance reduction can improve simulation efficiency
11. how to present quantitative results through charts and tables

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 20. Summary

This project transforms a basic Brownian motion simulation into a complete introductory quantitative finance project.

It begins with stochastic process simulation, extends into Geometric Brownian Motion, applies risk-neutral valuation, prices European options using Monte Carlo simulation, benchmarks against Black-Scholes, and analyses convergence and simulation error.

The project provides a foundation for future work in:

- derivatives pricing
- statistical arbitrage
- volatility modelling
- portfolio optimisation
- systematic trading research
- quantitative finance
