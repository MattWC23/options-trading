import yfinance as yf
import datetime
from model import Option
from black_scholes import BlackScholes

# Function to calculate time to expiration (in years)
def time_to_expiration(expiration_date):
    today = datetime.date.today()
    exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
    delta = exp_date - today
    return delta.days / 365.0

# Fetch options data from Yahoo Finance
def fetch_options(symbol, expiration_date):
    stock = yf.Ticker(symbol)
    options_chain = stock.option_chain(expiration_date)
   # print(f'keys: {stock.info.keys()}')
    return options_chain.calls, stock.info['currentPrice']

# Main function to integrate with Black-Scholes
def main():
    # Initialize Black-Scholes model
    bs_model = BlackScholes()
    
    # Specify stock symbol and expiration date
    symbol = "AAPL"  # Replace with your desired stock symbol
    expiration_date = "2025-01-31"  # Replace with the desired expiration date

    # Fetch options data and stock price
    calls, S = fetch_options(symbol, expiration_date)

    # Define risk-free rate (use a placeholder or get real data)
    r = 0.05  # Example: 5% annual risk-free rate
    
    # Process the options and feed them into the Black-Scholes model
    for index, row in calls.iterrows():
        K = row['strike']
        sigma = row['impliedVolatility']
        T = time_to_expiration(expiration_date)
        name = f"{symbol}_strike_{K}_exp_{expiration_date}"

        # Create an Option object
        option = Option(S=S, K=K, T=T, r=r, sigma=sigma, name=name)

        # Add the option to the model and calculate prices
        call_price, put_price = bs_model.add_option(option)
        print(f"Option: {name}, Call Price: ${call_price:.2f}, Put Price: ${put_price:.2f}")

# Run the script
if __name__ == "__main__":
    main()