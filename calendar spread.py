import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def call_option(stock_price, strike_price):
    payoff = max(stock_price - strike_price, 0)
    return payoff

def pricer(stock_price, strike_price, volatility, time, risk_free_interest):
    d1 = (np.log(stock_price / strike_price)
          + (risk_free_interest + 0.5 * volatility**2) * time) / (volatility * np.sqrt(time))
    d2 = d1 - volatility * np.sqrt(time)
    price_call = (norm.cdf(d1) * stock_price
                  - norm.cdf(d2) * strike_price * np.exp(-risk_free_interest * time))
    return price_call

def implied_volatility(volatility_1,volatility_2, time_1, time_2):
    imp_vol=np.sqrt((time_2*volatility_2**2-time_1*volatility_1**2)/(time_2-time_1))
    return imp_vol

def calendar_payoff(stock_price, strike_price, volatility_1,volatility_2 ,risk_free_interest, time_1,time_2):
    payoff = pricer(stock_price, strike_price,implied_volatility(volatility_1,volatility_2, time_1, time_2), (time_2-time_1), risk_free_interest) \
             - call_option(stock_price, strike_price)-pricer(strike_price,strike_price,volatility_2,time_2,risk_free_interest)+pricer(strike_price,strike_price,volatility_1,time_1,risk_free_interest)
    return payoff

# Parameters
strike_price = 100
volatility_1 = 0.32
volatility_2= 0.3
risk_free_interest = 0.04
time_1 = 30 / 365
time_2= 60/365

# Stock price range
stock_prices = np.linspace(strike_price-50, strike_price+50, 200)

# Compute payoff
payoffs = [
    calendar_payoff(s, strike_price, volatility_1,volatility_2 ,risk_free_interest, time_1,time_2)
    for s in stock_prices
]

# Plot
plt.figure()
plt.plot(stock_prices, payoffs)
plt.axhline(0)
plt.xlabel("Stock Price")
plt.ylabel("Calendar Payoff (P&L)")
plt.title("Calendar Spread P&L")
plt.show()


