# Project Summary: GBM Monte Carlo Option Pricing

## Objective
The aim of this project is to simulate stock-price paths using risk-neutral Geometric Brownian Motion and use Monte Carlo simulation to price European call and put options.

## Methodology
1. Simulate stock prices using exact GBM discretisation.
2. Calculate terminal payoffs for European call and put options.
3. Discount the average payoff to estimate the option price.
4. Compare Monte Carlo prices with Black-Scholes analytical prices.
5. Analyse convergence as the number of simulation paths increases.
6. Estimate standard errors and 95% confidence intervals.
7. Compare standard Monte Carlo with antithetic variates.

## Key Outputs
- GBM simulated path chart
- Terminal stock-price distribution
- Payoff distribution
- Convergence chart
- Pricing summary table

## Discussion Points
- Monte Carlo estimates converge toward the Black-Scholes benchmark as the number of paths increases.
- Standard error falls as simulation size increases.
- Antithetic variates can reduce variance by pairing each normal draw with its opposite.
- The model assumes constant volatility, continuous trading, lognormal stock prices and risk-neutral pricing.

## Limitations
- Constant volatility assumption.
- No transaction costs or liquidity effects.
- European options only.
- No calibration to real option market data.
- No stochastic volatility or jumps.

## Future Improvements
- Add Greeks and implied volatility.
- Extend to Asian, barrier and lookback options.
- Calibrate volatility using market option data.
- Compare GBM with stochastic volatility models.
