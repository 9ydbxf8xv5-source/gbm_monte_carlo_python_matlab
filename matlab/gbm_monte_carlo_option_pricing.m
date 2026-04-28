%% GBM Monte Carlo Option Pricing Project
% Python + MATLAB project for quantitative finance.
%
% This script extends a basic Brownian motion simulation into:
% 1. Geometric Brownian Motion stock-price simulation
% 2. European call and put Monte Carlo pricing
% 3. Black-Scholes benchmark comparison
% 4. Confidence intervals and convergence analysis
%
% Run from the project root:
% run("matlab/gbm_monte_carlo_option_pricing.m")

clear; close all; clc;

%% Output folder
outputDir = "outputs_matlab";
if ~exist(outputDir, "dir")
    mkdir(outputDir);
end

%% Parameters
S0 = 100;          % initial stock price
K = 100;           % strike price
T = 1;             % maturity in years
r = 0.05;          % risk-free rate
sigma = 0.20;      % volatility
nSteps = 252;      % daily time steps
nPaths = 50000;    % number of Monte Carlo paths
rng(42);           % seed for reproducibility

fprintf("\nGBM MONTE CARLO OPTION PRICING PROJECT - MATLAB\n");
fprintf("=====================================================\n");
fprintf("S0=%.2f, K=%.2f, T=%.2f, r=%.4f, sigma=%.4f, steps=%d, paths=%d\n", ...
    S0, K, T, r, sigma, nSteps, nPaths);

%% Simulate GBM paths
[timeGrid, paths] = simulateGBMPaths(S0, T, r, sigma, nSteps, nPaths);

terminalPrices = paths(end, :);

%% Monte Carlo option prices
callPayoffs = max(terminalPrices - K, 0);
putPayoffs = max(K - terminalPrices, 0);

discountFactor = exp(-r * T);

discountedCallPayoffs = discountFactor * callPayoffs;
discountedPutPayoffs = discountFactor * putPayoffs;

mcCall = mean(discountedCallPayoffs);
mcPut = mean(discountedPutPayoffs);

callStdError = std(discountedCallPayoffs) / sqrt(nPaths);
putStdError = std(discountedPutPayoffs) / sqrt(nPaths);

callCI = [mcCall - 1.96 * callStdError, mcCall + 1.96 * callStdError];
putCI = [mcPut - 1.96 * putStdError, mcPut + 1.96 * putStdError];

%% Black-Scholes benchmark
bsCall = blackScholesPrice(S0, K, T, r, sigma, "call");
bsPut = blackScholesPrice(S0, K, T, r, sigma, "put");

%% Print pricing results
fprintf("\nPRICING SUMMARY\n");
fprintf("-----------------------------------------------------\n");
fprintf("Black-Scholes Call Price:    %.6f\n", bsCall);
fprintf("Monte Carlo Call Price:      %.6f\n", mcCall);
fprintf("Call 95%% CI:                 [%.6f, %.6f]\n", callCI(1), callCI(2));
fprintf("Call Standard Error:         %.6f\n", callStdError);
fprintf("\n");
fprintf("Black-Scholes Put Price:     %.6f\n", bsPut);
fprintf("Monte Carlo Put Price:       %.6f\n", mcPut);
fprintf("Put 95%% CI:                  [%.6f, %.6f]\n", putCI(1), putCI(2));
fprintf("Put Standard Error:          %.6f\n", putStdError);

%% Antithetic variates for call option
[antiCall, antiSE] = antitheticCallPrice(S0, K, T, r, sigma, nSteps, nPaths);

fprintf("\nANTITHETIC VARIATES CHECK\n");
fprintf("-----------------------------------------------------\n");
fprintf("Standard MC Call Price:      %.6f\n", mcCall);
fprintf("Standard MC Std Error:       %.6f\n", callStdError);
fprintf("Antithetic MC Call Price:    %.6f\n", antiCall);
fprintf("Antithetic MC Std Error:     %.6f\n", antiSE);

%% Convergence analysis
pathCounts = [100, 500, 1000, 5000, 10000, 25000, 50000, 100000];

convN = zeros(length(pathCounts), 1);
convPrice = zeros(length(pathCounts), 1);
convSE = zeros(length(pathCounts), 1);
convLow = zeros(length(pathCounts), 1);
convHigh = zeros(length(pathCounts), 1);
convError = zeros(length(pathCounts), 1);

for i = 1:length(pathCounts)
    n = pathCounts(i);
    [~, tempPaths] = simulateGBMPaths(S0, T, r, sigma, nSteps, n);
    ST = tempPaths(end, :);
    payoffs = max(ST - K, 0);
    discounted = exp(-r*T) * payoffs;

    price = mean(discounted);
    se = std(discounted) / sqrt(n);

    convN(i) = n;
    convPrice(i) = price;
    convSE(i) = se;
    convLow(i) = price - 1.96 * se;
    convHigh(i) = price + 1.96 * se;
    convError(i) = abs(price - bsCall);
end

convergenceTable = table(convN, convPrice, repmat(bsCall, length(pathCounts), 1), ...
    convSE, convLow, convHigh, convError, ...
    'VariableNames', {'n_paths', 'monte_carlo_price', 'black_scholes_price', ...
    'std_error', 'ci_low', 'ci_high', 'absolute_error'});

disp(" ");
disp("CONVERGENCE TABLE");
disp(convergenceTable);

writetable(convergenceTable, fullfile(outputDir, "call_convergence_results_matlab.csv"));

summaryTable = table(["call"; "put"], [bsCall; bsPut], [mcCall; mcPut], ...
    [callStdError; putStdError], [callCI(1); putCI(1)], [callCI(2); putCI(2)], ...
    [abs(mcCall - bsCall); abs(mcPut - bsPut)], ...
    'VariableNames', {'option', 'black_scholes', 'monte_carlo', ...
    'std_error', 'ci_low', 'ci_high', 'absolute_error'});

writetable(summaryTable, fullfile(outputDir, "option_pricing_summary_matlab.csv"));

%% Charts

% Sample paths
figure;
plot(timeGrid, paths(:, 1:100), 'LineWidth', 0.8);
title("Simulated Risk-Neutral GBM Stock-Price Paths");
xlabel("Time");
ylabel("Stock Price");
grid on;
saveas(gcf, fullfile(outputDir, "gbm_sample_paths_matlab.png"));

% Terminal distribution
figure;
histogram(terminalPrices, 60);
xline(S0, "--", "Initial Price");
title("Distribution of Terminal Stock Prices");
xlabel("Terminal Stock Price");
ylabel("Frequency");
grid on;
saveas(gcf, fullfile(outputDir, "terminal_stock_distribution_matlab.png"));

% Call payoff distribution
figure;
histogram(callPayoffs, 60);
title("Distribution of European Call Payoffs");
xlabel("Call Payoff");
ylabel("Frequency");
grid on;
saveas(gcf, fullfile(outputDir, "call_payoff_distribution_matlab.png"));

% Convergence chart
figure;
semilogx(convN, convPrice, "-o", "LineWidth", 1.2);
hold on;
yline(bsCall, "--", "Black-Scholes Benchmark");
plot(convN, convLow, ":", "LineWidth", 1);
plot(convN, convHigh, ":", "LineWidth", 1);
title("Monte Carlo Convergence: European Call Option");
xlabel("Number of Simulation Paths");
ylabel("Option Price");
legend("Monte Carlo Price", "Black-Scholes Price", "95% CI Low", "95% CI High", "Location", "best");
grid on;
saveas(gcf, fullfile(outputDir, "call_convergence_matlab.png"));

fprintf("\nSaved MATLAB outputs in: %s\n", outputDir);

%% Local functions

function [timeGrid, paths] = simulateGBMPaths(S0, T, r, sigma, nSteps, nPaths)
    dt = T / nSteps;
    Z = randn(nSteps, nPaths);

    logIncrements = (r - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z;
    logPaths = [zeros(1, nPaths); cumsum(logIncrements, 1)];

    paths = S0 * exp(logPaths);
    timeGrid = linspace(0, T, nSteps + 1)';
end

function price = blackScholesPrice(S0, K, T, r, sigma, optionType)
    d1 = (log(S0/K) + (r + 0.5*sigma^2)*T) / (sigma*sqrt(T));
    d2 = d1 - sigma*sqrt(T);

    N = @(x) 0.5 * (1 + erf(x / sqrt(2)));

    if optionType == "call"
        price = S0 * N(d1) - K * exp(-r*T) * N(d2);
    elseif optionType == "put"
        price = K * exp(-r*T) * N(-d2) - S0 * N(-d1);
    else
        error("optionType must be call or put");
    end
end

function [price, se] = antitheticCallPrice(S0, K, T, r, sigma, nSteps, nPaths)
    if mod(nPaths, 2) ~= 0
        nPaths = nPaths + 1;
    end

    dt = T / nSteps;
    halfPaths = nPaths / 2;

    Z = randn(nSteps, halfPaths);
    ZA = -Z;

    logInc1 = (r - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z;
    logInc2 = (r - 0.5*sigma^2)*dt + sigma*sqrt(dt)*ZA;

    ST1 = S0 * exp(sum(logInc1, 1));
    ST2 = S0 * exp(sum(logInc2, 1));

    ST = [ST1, ST2];

    payoffs = max(ST - K, 0);
    discounted = exp(-r*T) * payoffs;

    price = mean(discounted);
    se = std(discounted) / sqrt(nPaths);
end
