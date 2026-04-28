# Project Explanation: Geometric Brownian Motion Monte Carlo Option Pricing Engine

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
- Black-Scholes Greeks
- implied volatility recovery
- volatility smile and volatility surface visualisation
- visualisation of simulated paths, payoff distributions and convergence behaviour

The project is designed as a first quantitative finance project: simple enough to explain clearly, but complete enough to demonstrate stochastic modelling, numerical simulation, option pricing, coding, and financial interpretation.

---

## 2. Motivation

The motivation behind this project is to connect theoretical financial mathematics with computational implementation.

In financial mathematics, asset prices are commonly modelled as stochastic processes because market prices evolve under uncertainty. One of the most important models is Geometric Brownian Motion, which is the stock-price model underlying Black-Scholes option pricing.

Although Black-Scholes gives an analytical solution for European options, many more complex derivatives do not have closed-form solutions. In those cases, Monte Carlo simulation is useful because it estimates derivative prices by simulating many possible future asset paths and averaging the discounted payoff.

This project demonstrates:

1. understanding of Brownian motion and GBM;
2. implementation of Monte Carlo simulation;
3. use of risk-neutral pricing;
4. comparison of numerical results with an analytical benchmark;
5. interpretation of convergence and simulation error;
6. extension from theoretical pricing into Greeks, implied volatility and volatility-surface intuition.

---

## 3. Brownian Motion

The starting point is Brownian motion, also known as a Wiener process.

A standard Brownian motion $W_t$ satisfies:

1. $W_0 = 0$
2. $W_t$ has independent increments
3. $W_t - W_s \sim \mathcal{N}(0,t-s)$ for $t > s$
4. paths are continuous
5. increments are normally distributed

For a small time step $\Delta t$, the Brownian increment can be simulated as:

$$
\Delta W_t = \sqrt{\Delta t}\,Z
$$

where:

$$
Z \sim \mathcal{N}(0,1)
$$

The Brownian path is then built recursively:

$$
W_{t+\Delta t} = W_t + \Delta W_t
$$

This was the starting point for the MATLAB version of the project.

---

## 4. From Brownian Motion to Geometric Brownian Motion

Brownian motion itself can take negative values, so it is not directly suitable for modelling stock prices. Stock prices must remain positive.

The Black-Scholes framework therefore models stock prices using **Geometric Brownian Motion**:

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t
$$

where:

- $S_t$ is the stock price at time $t$;
- $\mu$ is the expected return;
- $\sigma$ is volatility;
- $W_t$ is Brownian motion.

For option pricing, we use the **risk-neutral measure**, where the expected return $\mu$ is replaced by the risk-free rate $r$:

$$
dS_t = rS_t\,dt + \sigma S_t\,dW_t
$$

The exact discretisation used in the project is:

$$
S_{t+\Delta t}=S_t\exp\left(\left(r-\frac{1}{2}\sigma^2\right)\Delta t+\sigma\sqrt{\Delta t}\,Z\right)
$$

where:

$$
Z \sim \mathcal{N}(0,1)
$$

This formula is used to simulate the stock-price paths. Each path represents one possible future market outcome. As time increases, the paths spread out because uncertainty accumulates through the volatility term.

---

## 5. Risk-Neutral Pricing

The project uses the risk-neutral pricing formula.

For a derivative with payoff $V_T$ at maturity $T$, the time-0 value is:

$$
V_0 = e^{-rT}\mathbb{E}^{Q}[V_T]
$$

where:

- $\mathbb{E}^{Q}$ is the expectation under the risk-neutral measure;
- $e^{-rT}$ is the discount factor;
- $V_T$ is the payoff at maturity.

For a European call option:

$$
V_T = \max(S_T-K,0)
$$

For a European put option:

$$
V_T = \max(K-S_T,0)
$$

The Monte Carlo price is obtained by averaging simulated discounted payoffs:

$$
V_0
\approx
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}V_T^{(i)}
$$

where:

- $V_0$ is the option price today;
- $V_T^{(i)}$ is the payoff from the $i$-th simulated path;
- $N$ is the number of simulated paths;
- $e^{-rT}$ is the discount factor.

---

## 6. Monte Carlo Pricing Method

The Monte Carlo procedure is:

1. Choose input parameters:
   - initial stock price $S_0$
   - strike price $K$
   - maturity $T$
   - risk-free rate $r$
   - volatility $\sigma$
   - number of time steps
   - number of simulated paths

2. Simulate many stock-price paths under risk-neutral GBM.

3. Extract the terminal stock prices $S_T$.

4. Calculate European option payoffs:

$$
\text{Call payoff} = \max(S_T-K,0)
$$

$$
\text{Put payoff} = \max(K-S_T,0)
$$

5. Discount the average payoff back to time 0.

6. Compare the Monte Carlo estimate with the Black-Scholes analytical price.

7. Calculate standard error and confidence intervals.

8. Analyse convergence as the number of simulated paths increases.

---

## 7. Black-Scholes Benchmark

The Black-Scholes formula provides an analytical benchmark for European call and put options.

For a European call:

$$
C=S_0N(d_1)-Ke^{-rT}N(d_2)
$$

For a European put:

$$
P=Ke^{-rT}N(-d_2)-S_0N(-d_1)
$$

where:

$$
d_1=\frac{\ln\left(\frac{S_0}{K}\right)+\left(r+\frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}
$$

and:

$$
d_2=d_1-\sigma\sqrt{T}
$$

Here, $N(\cdot)$ is the standard normal cumulative distribution function.

The project compares the Monte Carlo option prices against the Black-Scholes values. Since both methods price the same European options under the same assumptions, the Monte Carlo values should converge toward the Black-Scholes benchmarks as the number of simulations increases.

## 8. Parameters Used

The base project uses the following benchmark parameters:

~~~text
Initial stock price, S0       = 100
Strike price, K               = 100
Time to maturity, T           = 1 year
Risk-free rate, r             = 5%
Volatility, sigma             = 20%
Number of time steps          = 252
Number of Monte Carlo paths   = 50,000
~~~

The option is at-the-money because:

$$
S_0 = K = 100
$$

The use of 252 time steps represents daily trading days over one year.

---

## 9. Python Implementation

The Python implementation is the main version of the project.

It contains several core components.

### 9.1 Black-Scholes Function

The function `black_scholes_price()` calculates the analytical Black-Scholes price for either a European call or put.

Inputs:

~~~python
S0, K, T, r, sigma, option_type
~~~

Output:

~~~python
option_price
~~~

This function provides the theoretical benchmark for the Monte Carlo simulation.

---

### 9.2 GBM Path Simulation

The function `simulate_gbm_paths()` simulates risk-neutral GBM paths.

It generates standard normal random variables:

~~~python
Z = rng.standard_normal((n_steps, n_paths))
~~~

Then it calculates log increments:

~~~python
log_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
~~~

The cumulative sum creates the log-stock path:

~~~python
log_paths = np.cumsum(log_increments, axis=0)
~~~

Exponentiating gives simulated stock prices:

~~~python
paths = S0 * np.exp(log_paths)
~~~

---

### 9.3 Monte Carlo Option Pricing

The function `monte_carlo_option_price()` calculates the Monte Carlo price.

It takes terminal stock prices:

~~~python
terminal_prices = paths[-1]
~~~

Then calculates payoffs.

For a call:

~~~python
payoffs = np.maximum(terminal_prices - K, 0)
~~~

For a put:

~~~python
payoffs = np.maximum(K - terminal_prices, 0)
~~~

Then discounts the payoffs:

~~~python
discounted_payoffs = np.exp(-r * T) * payoffs
~~~

The Monte Carlo price is:

~~~python
price = discounted_payoffs.mean()
~~~

---

## 10. Standard Error and Confidence Intervals

Monte Carlo simulation produces an estimate, not an exact value.

The standard error is calculated as:

$$
SE=\frac{\sigma_{\text{payoff}}}{\sqrt{N}}
$$

where:

- $\sigma_{\text{payoff}}$ is the standard deviation of discounted payoffs;
- $N$ is the number of simulated paths.

A 95% confidence interval is calculated as:

$$
\text{Price}\pm1.96\times SE
$$

This shows the uncertainty around the Monte Carlo estimate.

Including standard errors and confidence intervals strengthens the project because it demonstrates that the Monte Carlo result is treated as a statistical estimate rather than an exact number.

---

## 11. Convergence Analysis

The project tests how the Monte Carlo price changes as the number of simulated paths increases.

The path counts used are:

~~~text
100
500
1,000
5,000
10,000
25,000
50,000
100,000
~~~

For each number of paths, the project calculates:

- Monte Carlo option price
- Black-Scholes benchmark
- standard error
- 95% confidence interval
- absolute error

The convergence chart shows the Monte Carlo estimate approaching the Black-Scholes benchmark as the number of simulations increases.

This is consistent with the law of large numbers: as the sample size increases, the average simulated payoff should converge toward the true expected payoff.

---

## 12. Antithetic Variates

The project includes antithetic variates as a basic variance-reduction technique.

In standard Monte Carlo, the simulation uses random normal draws $Z$.

With antithetic variates, for every draw $Z$, the simulation also uses:

$$
-Z
$$

This pairs positive and negative shocks.

The idea is that high and low outcomes partially offset each other, reducing the variance of the estimator.

The project compares:

- standard Monte Carlo price and standard error;
- antithetic Monte Carlo price and standard error.

This demonstrates awareness of variance reduction, which is important in computational finance.

---

## 13. MATLAB Implementation

The MATLAB version has two parts.

### 13.1 Basic Brownian Motion Simulation

The file `brownian_motion_basic.m` simulates discretised Brownian motion using:

$$
dW = \sqrt{dt}\,Z
$$

and:

$$
W_j = W_{j-1}+dW_j
$$

This recreates the Brownian motion simulation studied in Computational Methods in Finance.

---

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

---

## 14. Visual Outputs

The project generates several visual outputs.

### 14.1 Simulated GBM Stock-Price Paths

This chart shows multiple simulated stock-price paths over one year.

Each path represents one possible future evolution of the stock price under risk-neutral GBM.

The paths spread out over time because uncertainty increases over longer horizons.

---

### 14.2 Terminal Stock-Price Distribution

This histogram shows the distribution of terminal stock prices $S_T$.

Under GBM, terminal stock prices are lognormally distributed. This means:

- prices remain positive;
- the distribution is right-skewed;
- large upside moves are possible;
- downside is bounded by zero.

---

### 14.3 European Call Payoff Distribution

This histogram shows the distribution of European call payoffs:

$$
\max(S_T-K,0)
$$

Many payoffs are zero when the option finishes out-of-the-money.

Positive payoffs occur when:

$$
S_T > K
$$

---

### 14.4 Monte Carlo Convergence Chart

This chart shows the Monte Carlo call price as the number of simulated paths increases.

It also includes:

- the Black-Scholes benchmark;
- the 95% confidence interval.

This is one of the most important charts because it shows that the Monte Carlo estimate behaves as expected and moves toward the theoretical value as simulation size increases.

---

## 15. Results Interpretation

The Monte Carlo call and put prices are close to the Black-Scholes benchmark values.

This shows that the simulation is correctly approximating the theoretical option prices.

The convergence chart shows that:

- with a small number of paths, the Monte Carlo estimate is noisy;
- as the number of paths increases, the estimate becomes more stable;
- the confidence interval narrows as simulation size increases;
- the estimate moves closer to the Black-Scholes analytical price.

The standard error decreases as the number of paths increases because:

$$
SE \propto \frac{1}{\sqrt{N}}
$$

This is consistent with Monte Carlo theory.

---

## 16. Black-Scholes Greeks

The project was extended to include Black-Scholes Greeks.

Greeks measure how sensitive an option price is to different market variables. This is important because traders and risk managers do not only care about the option price; they also care about how that price changes when market conditions change.

The Greeks included are:

| Greek | Interpretation |
|---|---|
| Delta | Sensitivity of the option price to the underlying stock price |
| Gamma | Sensitivity of Delta to changes in the stock price |
| Vega | Sensitivity of the option price to volatility |
| Theta | Sensitivity of the option price to time decay |
| Rho | Sensitivity of the option price to interest rates |

### Delta

Delta measures sensitivity to the underlying stock price:

$$
\Delta = \frac{\partial V}{\partial S}
$$

The Delta chart shows how the call option becomes more sensitive to the stock price as the option moves deeper in-the-money.

When the option is far out-of-the-money, Delta is close to zero because changes in the stock price have little effect on the option value. When the option is deep in-the-money, Delta approaches one because the option behaves more like the underlying stock.

### Gamma

Gamma measures the rate of change of Delta:

$$
\Gamma = \frac{\partial^2 V}{\partial S^2}
$$

Gamma is highest near the strike price, meaning at-the-money options have the most unstable hedge ratio. This is important for options traders because high Gamma means the position’s exposure changes quickly as the underlying price moves.

### Vega

Vega measures sensitivity to volatility:

$$
\text{Vega} = \frac{\partial V}{\partial \sigma}
$$

Vega is usually highest near the strike price because at-the-money options are most affected by changes in uncertainty. This matters because option prices can rise or fall significantly when implied volatility changes, even if the underlying stock price does not move much.

### Theta

Theta measures sensitivity to the passage of time:

$$
\Theta = \frac{\partial V}{\partial t}
$$

For long options, Theta is generally negative because the option loses time value as maturity approaches. This reflects the cost of holding optionality over time.

### Rho

Rho measures sensitivity to interest rates:

$$
\rho = \frac{\partial V}{\partial r}
$$

Rho is usually less important for short-dated equity options than Delta, Gamma, Vega and Theta, but it is still part of the full Black-Scholes risk-sensitivity framework.

---

## 17. Implied Volatility

The project also adds an implied volatility solver.

Implied volatility is the volatility value that makes the Black-Scholes price equal to a given market option price.

Mathematically, implied volatility $\sigma_{\text{imp}}$ solves:

$$
V_{\text{BS}}(S_0,K,T,r,\sigma_{\text{imp}})=V_{\text{market}}
$$

This is important because market participants often quote and compare options in volatility terms rather than price terms.

## 17. Implied Volatility

The project also adds an implied volatility solve.

Implied volatility is the volatility value that makes the Black-Scholes price equal to a given market option price.

Mathematically, implied volatility $\sigma_{\text{imp}}$ solves:

$$
V_{\text{BS}}(S_0,K,T,r,\sigma_{\text{imp}})=V_{\text{market}}
$$

This is important because market participants often quote and compare options in volatility terms rather than price terms.

The implied volatility section uses synthetic option prices to recover implied volatilities across different strikes and maturities. This creates a volatility smile and volatility surface.

---

## 18. Volatility Smile and Volatility Surface

### Volatility Smile

The volatility smile shows how implied volatility changes across strikes for one maturity.

In the real market, implied volatility is usually not constant across strikes. This shows one of the main limitations of the basic Black-Scholes model, which assumes one constant volatility.

### Volatility Surface

The volatility surface extends the volatility smile across both strike and maturity.

It shows how implied volatility varies across different option strikes and expiries. This is closer to how options are analysed in practice, where traders look at the entire volatility surface rather than using a single volatility input.

---

## 19. Why This Project Is Relevant to Quantitative Finance

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
- Greeks and risk sensitivities
- implied volatility and volatility-surface intuition

These are important foundations for:

- derivatives pricing
- quant research
- model validation
- risk management
- volatility modelling
- computational finance
- systematic trading research

Although the model is simple, it provides the base for more advanced work such as exotic option pricing, implied volatility modelling, stochastic volatility models, volatility surfaces and statistical trading strategies.

---

## 20. Limitations

### 20.1 Constant Volatility

The model assumes volatility is constant.

In real markets, volatility changes through time and differs across strikes and maturities.

### 20.2 No Jumps

GBM assumes continuous price paths.

Real markets can experience jumps due to earnings announcements, macroeconomic data, central bank decisions, geopolitical events or liquidity shocks.

### 20.3 European Options Only

The project prices European options, which can only be exercised at maturity.

American options require different numerical methods, such as:

- binomial trees
- finite-difference methods
- regression-based Monte Carlo

### 20.4 No Transaction Costs or Liquidity Effects

The model ignores:

- transaction costs
- bid-ask spreads
- liquidity
- execution risk
- market impact

These matter in real trading.

### 20.5 No Calibration to Market Data

The base model uses fixed input parameters rather than calibrating volatility from real market option prices.

A more advanced version would use real option-chain data to estimate implied volatility.

### 20.6 Black-Scholes Assumptions

The Black-Scholes framework assumes:

- lognormal stock prices
- constant volatility
- constant risk-free rate
- continuous trading
- frictionless markets
- no jumps
- European exercise

These assumptions are useful for a benchmark model but are simplified relative to real markets.

---

## 21. Future Improvements

Future versions could include:

- real market option-chain data
- implied volatility calibration
- volatility smile and surface fitting
- stochastic volatility models
- jump-diffusion models
- American option pricing
- Asian options
- barrier options
- lookback options
- comparison of exact GBM discretisation with Euler-Maruyama
- hedging simulations using Delta and Gamma
- live option-chain analysis

---

## 22. Key Learning Outcomes

This project helped develop understanding of:

1. how Brownian motion is simulated computationally;
2. how Brownian motion leads to Geometric Brownian Motion;
3. how GBM is used in the Black-Scholes framework;
4. why risk-neutral pricing uses the risk-free rate as drift;
5. how European option payoffs are calculated;
6. how Monte Carlo simulation estimates discounted expected payoffs;
7. how to compare numerical estimates against analytical benchmarks;
8. how to calculate standard errors and confidence intervals;
9. how Monte Carlo convergence behaves;
10. how variance reduction can improve simulation efficiency;
11. how Greeks measure option risk sensitivities;
12. how implied volatility is recovered from option prices;
13. how volatility smiles and surfaces show limitations of constant-volatility Black-Scholes;
14. how to present quantitative results through charts and tables.

---

## 23. Summary

This project transforms a basic Brownian motion simulation into a complete introductory quantitative finance project.

It begins with stochastic process simulation, extends into Geometric Brownian Motion, applies risk-neutral valuation, prices European options using Monte Carlo simulation, benchmarks against Black-Scholes, analyses convergence and simulation error, and extends into Greeks, implied volatility, volatility smiles and volatility surfaces.

The project provides a foundation for future work in:

- derivatives pricing
- statistical arbitrage
- volatility modelling
- portfolio optimisation
- systematic trading research
- quantitative finance

## Project Explanation and Mathematical Intuition Behind Black-Scholes, Greeks, and Implied Volatility

This project builds a derivatives-pricing framework using Geometric Brownian Motion (GBM), Monte Carlo simulation, and the **Black-Scholes model. The main objective is to simulate possible future stock-price paths, price European call and put options from those simulated outcomes, and compare the Monte Carlo estimates against Black-Scholes analytical prices.

The project starts from the idea that stock prices are uncertain and can be modelled as stochastic processes. A basic Brownian motion process captures random movement through normally distributed increments. However, Brownian motion itself can become negative, which is not suitable for stock prices. To model stock prices, the project uses Geometric Brownian Motion, which keeps simulated prices positive and gives lognormally distributed terminal stock prices.

Under the risk-neutral measure, the stock-price process is modelled as:

$$
dS_t = rS_t\,dt + \sigma S_t\,dW_t
$$

where:

- $S_t$ is the stock price at time $t$;
- $r$ is the risk-free rate;
- $\sigma$ is volatility;
- $dW_t$ is the Brownian motion shock.

The risk-neutral framework is important because option pricing is not based on the real-world expected return of the stock. Instead, the expected drift is replaced by the risk-free rate $r$. This allows the option value to be calculated as the discounted expected payoff under the risk-neutral measure.

The simulated stock-price paths are generated using the exact GBM discretisation:

$$
S_{t+\Delta t}=S_t\exp\left(\left(r-\frac{1}{2}\sigma^2\right)\Delta t+\sigma\sqrt{\Delta t}\,Z\right)
$$

where:

$$
Z\sim\mathcal{N}(0,1)
$$

This formula creates many possible future paths for the stock price. Each path represents one possible future market outcome. As time increases, the paths spread out because uncertainty accumulates through the volatility term $\sigma\sqrt{\Delta t}\,Z$.

Once the stock-price paths are simulated, the project prices European options by calculating the payoff at maturity.

For a European call option, the payoff is:

$$
\max(S_T-K,0)
$$

For a European put option, the payoff is:

$$
\max(K-S_T,0)
$$

where $S_T$ is the terminal stock price and $K$ is the strike price.

The Monte Carlo option price is calculated by averaging the discounted payoffs:

$$
V_0=e^{-rT}\frac{1}{N}\sum_{i=1}^{N}V_T^{(i)}
$$

where:

- $V_0$ is the option price today;
- $V_T^{(i)}$ is the payoff from the $i$-th simulated path;
- $N$ is the number of simulated paths;
- $e^{-rT}$ is the discount factor.

The Monte Carlo results are compared against the Black-Scholes analytical benchmark. This is useful because Black-Scholes gives a closed-form price for European options under the same assumptions: constant volatility, continuous trading, no jumps, no transaction costs, and lognormally distributed stock prices. If the Monte Carlo engine is working correctly, the simulated option price should be close to the Black-Scholes price and converge toward it as the number of simulated paths increases.

The project also calculates the standard error and $95\%$ confidence interval of the Monte Carlo estimate. This is important because Monte Carlo pricing is statistical rather than exact. The standard error measures the uncertainty in the estimate:

$$
SE=\frac{\sigma_{\text{payoff}}}{\sqrt{N}}
$$

As the number of simulations $N$ increases, the standard error decreases. This means the Monte Carlo price becomes more stable and the confidence interval becomes narrower.

The convergence chart demonstrates this effect visually. With a small number of paths, the Monte Carlo estimate is noisy and may be far from the Black-Scholes price. As the number of paths increases, the estimate becomes more accurate and approaches the analytical benchmark. This reflects the law of large numbers.

The project also includes antithetic variates, a simple variance-reduction technique. Instead of only simulating random shocks $Z$, the model also simulates the opposite shocks $-Z$. This helps balance upward and downward movements and can reduce the variance of the Monte Carlo estimator. This is useful in computational finance because lower variance means more accurate estimates without necessarily requiring a much larger number of simulations.

---

## Black-Scholes Greeks

The project was extended to include Black-Scholes Greeks. Greeks measure how sensitive an option price is to different market variables. This is important because traders and risk managers do not only care about the option price; they also care about how that price changes when market conditions change.

The Greeks included are:

| Greek | Symbol | Interpretation |
|---|---:|---|
| Delta | $\Delta$ | Sensitivity of the option price to the underlying stock price |
| Gamma | $\Gamma$ | Sensitivity of Delta to changes in the underlying stock price |
| Vega | $\nu$ | Sensitivity of the option price to volatility |
| Theta | $\Theta$ | Sensitivity of the option price to time decay |
| Rho | $\rho$ | Sensitivity of the option price to interest rates |

---

### Delta

Delta measures the sensitivity of the option value $V$ to changes in the underlying stock price $S$:

$$
\Delta=\frac{\partial V}{\partial S}
$$

The Delta chart shows how the call option becomes more sensitive to the stock price as the option moves deeper in-the-money. When the option is far out-of-the-money, Delta is close to $0$ because changes in the stock price have little effect on the option value. When the option is deep in-the-money, Delta approaches $1$ because the option behaves more like the underlying stock.

For a European call option under Black-Scholes:

$$
\Delta_{\text{call}}=N(d_1)
$$

For a European put option:

$$
\Delta_{\text{put}}=N(d_1)-1
$$

---

### Gamma

Gamma measures how quickly Delta changes as the stock price changes:

$$
\Gamma=\frac{\partial^2 V}{\partial S^2}
$$

Gamma is highest near the strike price $K$, meaning at-the-money options have the most unstable hedge ratio. This is important for options traders because high Gamma means the position’s exposure changes quickly as the underlying price moves.

Under Black-Scholes:

$$
\Gamma=\frac{N'(d_1)}{S\sigma\sqrt{T}}
$$

where $N'(d_1)$ is the standard normal probability density function evaluated at $d_1$.

---

### Vega

Vega measures the sensitivity of the option price to volatility:

$$
\text{Vega}=\frac{\partial V}{\partial \sigma}
$$

The Vega chart shows sensitivity to volatility. Vega is usually highest near the strike price because at-the-money options are most affected by changes in uncertainty. This matters because option prices can rise or fall significantly when implied volatility changes, even if the underlying stock price does not move much.

Under Black-Scholes:

$$
\text{Vega}=S\,N'(d_1)\sqrt{T}
$$

In the Python implementation, Vega is divided by $100$ so that it represents the option price change for a $1\%$ change in volatility.

---

### Theta

Theta measures sensitivity to the passage of time:

$$
\Theta=\frac{\partial V}{\partial t}
$$

The Theta chart shows time decay. For long options, Theta is generally negative because the option loses time value as maturity approaches. This reflects the cost of holding optionality over time.

For a European call option under Black-Scholes:

$$
\Theta_{\text{call}}
=
-\frac{S N'(d_1)\sigma}{2\sqrt{T}}
-
rKe^{-rT}N(d_2)
$$

For a European put option:

$$
\Theta_{\text{put}}
=
-\frac{S N'(d_1)\sigma}{2\sqrt{T}}
+
rKe^{-rT}N(-d_2)
$$

In the Python implementation, Theta is divided by $365$ so that it represents daily time decay.

---

### Rho

Rho measures sensitivity to interest rates:

$$
\rho=\frac{\partial V}{\partial r}
$$

The Rho chart shows sensitivity to interest rates. Rho is usually less important for short-dated equity options than Delta, Gamma, Vega and Theta, but it is still part of the full Black-Scholes risk-sensitivity framework.

For a European call option:

$$
\rho_{\text{call}}=KT e^{-rT}N(d_2)
$$

For a European put option:

$$
\rho_{\text{put}}=-KT e^{-rT}N(-d_2)
$$

In the Python implementation, Rho is divided by $100$ so that it represents the option price change for a $1\%$ change in interest rates.

---

## Implied Volatility

The project also adds an implied volatility solver. Implied volatility is the volatility value that makes the Black-Scholes price equal to a given market option price.

Mathematically, implied volatility $\sigma_{\text{imp}}$ solves:

$$
V_{\text{BS}}(S_0,K,T,r,\sigma_{\text{imp}})=V_{\text{market}}
$$

This is important because market participants often quote and compare options in volatility terms rather than price terms.

The project solves for implied volatility using a numerical root-finding method. The solver searches for the volatility input $\sigma$ that makes the difference between the Black-Scholes price and the market price equal to zero:

$$
V_{\text{BS}}(\sigma)-V_{\text{market}}=0
$$

The implied volatility section uses synthetic option prices to recover implied volatilities across different strikes and maturities. This creates a volatility smile and a volatility surface.

---

## Volatility Smile

The volatility smile shows how implied volatility changes across strikes for one maturity.

In the basic Black-Scholes model, volatility is assumed to be constant. That means every option with the same underlying should use the same volatility input $\sigma$. In real markets, this is usually not true. Options with different strikes often trade at different implied volatilities.

The volatility smile shows this visually. It plots implied volatility against strike price $K$ for a fixed maturity $T$.

A simplified interpretation is:

- near-the-money options may have one implied volatility;
- deep out-of-the-money options may have higher implied volatility;
- deep in-the-money options may also have different implied volatility;
- the curve reveals how the market prices risk differently across strikes.

This highlights one of the main limitations of the basic Black-Scholes model: the assumption of one constant volatility.

---

## Volatility Surface

The volatility surface extends the volatility smile across both strike and maturity.

Instead of only plotting implied volatility against strike for one expiry, the volatility surface shows implied volatility as a function of both strike $K$ and maturity $T$:

$$
\sigma_{\text{imp}}=\sigma_{\text{imp}}(K,T)
$$

This is closer to how options are analysed in practice. Options traders do not usually think in terms of one single volatility number. They look at the full volatility surface across strikes and expiries.

The volatility surface helps show:

- how implied volatility changes across strike;
- how implied volatility changes across maturity;
- how short-dated and long-dated options are priced differently;
- where the market may be assigning higher or lower uncertainty.

---

## Overall Interpretation

Overall, this project demonstrates the full connection between stochastic modelling, option pricing, simulation, model validation and risk sensitivity.

It starts with Brownian motion, extends to GBM stock-price simulation, applies risk-neutral valuation, prices European options using Monte Carlo simulation, benchmarks against Black-Scholes, analyses convergence and simulation error, and then extends into Greeks, implied volatility, volatility smiles and volatility surfaces.

The project is not intended to be a live trading model. Its purpose is to demonstrate the mathematical and computational foundations behind derivative pricing.

The main limitations are that the model assumes:

- constant volatility;
- no jumps;
- no transaction costs;
- no liquidity effects;
- European-style exercise only;
- no calibration to real option-chain data.

Future improvements could include:

- real option-chain data;
- implied volatility calibration;
- stochastic volatility models;
- jump-diffusion models;
- American option pricing;
- delta-hedging simulation;
- exotic options such as Asian, barrier and lookback options.
