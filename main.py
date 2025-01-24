import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Streamlit UI
st.title("Real-Time Stock Price Dashboard")

# User input for stock ticker or company name
symbol_or_name = st.text_input("Enter Stock Ticker Symbol")

# Time Interval
interval = st.selectbox("Select Time Interval", ["1m", "5m", "15m", "30m", "60m", "1d", "1wk", "1mo"])
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)  # default to 1 year of data


# Function to fetch stock data using yfinance
def fetch_stock_data(symbol, interval, start_date, end_date):
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(start=start_date, end=end_date, interval=interval)
        if data.empty:
            st.warning(f"No data found for {symbol}. Try a different time range or symbol.")
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


# Function to search for stock symbol using company name
def get_stock_symbol(company_name):
    try:
        ticker = yf.Ticker(company_name)
        info = ticker.info
        return info.get('symbol', None), info
    except Exception as e:
        st.error(f"Error finding symbol for {company_name}: {e}")
        return None, None


# Process user input
symbol = symbol_or_name.strip()
if not symbol:
    st.error("Please enter a valid stock ticker or company name.")
else:
    # Determine if the input is a symbol or a name
    if not symbol.isalpha() or len(symbol) > 5:  # If the input seems like a company name
        symbol, stock_info = get_stock_symbol(symbol)
    else:
        stock_info = yf.Ticker(symbol).info

    if symbol:  # Proceed only if a valid symbol is obtained
        # Display stock identification details
        if stock_info:
            st.subheader(f"Stock Information for {symbol}")
            company_name = stock_info.get('longName', 'N/A')
            sector = stock_info.get('sector', 'N/A')
            market_cap = stock_info.get('marketCap', 'N/A')
            st.write(f"**Company Name:** {company_name}")
            st.write(f"**Sector:** {sector}")
            st.write(f"**Market Cap:** {market_cap:,} USD" if isinstance(market_cap, int) else "**Market Cap:** N/A")

        # Fetch stock data
        data = fetch_stock_data(symbol, interval, start_date, end_date)

        if not data.empty:
            st.write(f"Stock Data for {symbol}")

            # Display stock data table
            st.write(data)

            # Stock Data Overview in Table
            st.subheader("Stock Data Overview")
            latest_data = data.iloc[-1]
            overview_df = pd.DataFrame({
                "Metric": ["Open", "Close", "High", "Low", "Volume"],
                "Value": [
                    latest_data['Open'],
                    latest_data['Close'],
                    latest_data['High'],
                    latest_data['Low'],
                    latest_data['Volume']
                ]
            })
            st.table(overview_df)

            # Plot data using Streamlit built-in chart
            st.line_chart(data['Close'], use_container_width=True)
        else:
            st.error("No data available for the selected symbol or interval.")
    else:
        st.error("Could not find a valid stock symbol or company name. Please try again.")
