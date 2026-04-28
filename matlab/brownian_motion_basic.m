%% Basic Brownian Motion Simulation
% This script reproduces the core idea from Computational Methods in Finance:
% simulate Brownian motion using increments dW = sqrt(dt) * Z, where Z ~ N(0,1).

clear; close all; clc;

rng(100);        % seed for reproducibility
T = 1;           % time horizon
N = 500;         % number of time steps
dt = T / N;      % time step

dW = zeros(1, N);
W = zeros(1, N);

dW(1) = sqrt(dt) * randn;
W(1) = dW(1);

for j = 2:N
    dW(j) = sqrt(dt) * randn;
    W(j) = W(j-1) + dW(j);
end

t = 0:dt:T;

figure;
plot(t, [0, W], '-r', 'LineWidth', 1.2);
xlabel('$t$', 'FontSize', 14, 'Interpreter', 'latex');
ylabel('$W(t)$', 'FontSize', 14, 'Interpreter', 'latex', 'Rotation', 0);
title('Discretised Brownian Motion Path');
grid on;
