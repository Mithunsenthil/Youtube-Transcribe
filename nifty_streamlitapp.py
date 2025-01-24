import streamlit as st
import yfinance as yf
import pandas as pd
import time
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns






import streamlit as st





nav_option = st.sidebar.radio("Navigation", ["About", "Stock Info", "Volatility of Stock", "Portfolio Index"])


if nav_option == "Portfolio Index":
    st.title("Equal Weight Stock Portfolio Creator")

    amount = st.number_input("Enter Portfolio Amount:", min_value=10000.0, max_value=1000000000.0, value=10000.0, step=100.0)

    nifty50_tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS",
        "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ITC.NS",
        "ASIANPAINT.NS", "HCLTECH.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS",
        "NESTLEIND.NS", "TITAN.NS", "TECHM.NS", "WIPRO.NS", "HDFCLIFE.NS", "ADANIENT.NS",
        "TATASTEEL.NS", "ONGC.NS", "BAJAJFINSV.NS", "POWERGRID.NS", "INDUSINDBK.NS", "ADANIGREEN.NS",
        "JSWSTEEL.NS", "CIPLA.NS", "GRASIM.NS", "DIVISLAB.NS", "DRREDDY.NS", "NTPC.NS",
        "M&M.NS", "BPCL.NS", "SHREECEM.NS", "SBILIFE.NS", "EICHERMOT.NS", "COALINDIA.NS",
        "TATAMOTORS.NS", "HEROMOTOCO.NS", "BRITANNIA.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "DABUR.NS",
        "BAJAJ-AUTO.NS", "HINDALCO.NS"
    ]

    df_tickers = pd.DataFrame(nifty50_tickers, columns=["Ticker"])
    csv_file_name = "nifty50_tickers.csv"
    df_tickers.to_csv(csv_file_name, index=False)

    dt_tickers = pd.read_csv("nifty50_tickers.csv")

    st.write(f"You entered: {amount}")

    if st.button("Create My Equal Weight Stock Portfolio"):
        lst = []
        for i in range(len(dt_tickers)):
            tickerLst = []
            investmentAmt = amount / len(nifty50_tickers) 
            ticker_symbol = dt_tickers.iloc[i]['Ticker']

            try:
                data = yf.download(ticker_symbol, period="1d")
                if data.empty or 'Adj Close' not in data.columns:
                    raise ValueError(f"No data returned for {ticker_symbol}")
                tickerAmt = data['Adj Close'].iloc[0]
                tickerLst.append(ticker_symbol)
                tickerLst.append(f'Rs {tickerAmt}')
                tickerLst.append(investmentAmt / tickerAmt) 
                lst.append(tickerLst)
            except Exception as e:
                st.write(f"Failed to retrieve data for {ticker_symbol}: {e}")
            
            time.sleep(1)

        portfolio_df = pd.DataFrame(lst, columns=["Ticker", "Price", "Shares"])

        st.write("Here is your equal weight stock portfolio:")
        st.dataframe(portfolio_df, height=500, width=800)

   
        fig = px.pie(portfolio_df, names='Ticker', values='Shares', title='Proportion of Shares per Stock')
        st.plotly_chart(fig)


        fig = px.bar(portfolio_df, x='Ticker', y='Price', title='Stock Price per Ticker', width = 1500, height = 400 )
        st.plotly_chart(fig)


    
elif nav_option == "Stock Info":

    option = st.selectbox(
        "Select a Stock you want to know about?",
        (
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
            "HINDUNILVR.NS", "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "BAJFINANCE.NS",
            "BHARTIARTL.NS", "ITC.NS", "ASIANPAINT.NS", "HCLTECH.NS", "AXISBANK.NS",
            "MARUTI.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "TITAN.NS",
            "TECHM.NS", "WIPRO.NS", "HDFCLIFE.NS", "ADANIENT.NS", "TATASTEEL.NS",
            "ONGC.NS", "BAJAJFINSV.NS", "POWERGRID.NS", "INDUSINDBK.NS", "ADANIGREEN.NS",
            "JSWSTEEL.NS", "CIPLA.NS", "GRASIM.NS", "DIVISLAB.NS", "DRREDDY.NS",
            "NTPC.NS", "M&M.NS", "BPCL.NS", "SHREECEM.NS", "SBILIFE.NS",
            "EICHERMOT.NS", "COALINDIA.NS", "TATAMOTORS.NS", "HEROMOTOCO.NS",
            "BRITANNIA.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "DABUR.NS",
            "BAJAJ-AUTO.NS", "HINDALCO.NS"
        ),
    )


    ticker = yf.Ticker(option)
    info = ticker.info


    data_points = {
        "Phone": info.get('phone', 'N/A'),
        "Fax": info.get('fax', 'N/A'),
        "Website": info.get('website', 'N/A'),
        "Industry": info.get('industry', 'N/A'),
        "Sector": info.get('sector', 'N/A'),
        "Market Cap": info.get('marketCap', 'N/A'),
        "Enterprise Value": info.get('enterpriseValue', 'N/A'),
        "Revenue Per Share": info.get('revenuePerShare', 'N/A'),
        "EBITDA": info.get('ebitda', 'N/A'),
        "Total Revenue": info.get('totalRevenue', 'N/A'),
        "Total Debt": info.get('totalDebt', 'N/A'),
        "Debt to Equity": info.get('debtToEquity', 'N/A'),
        "Current Price": info.get('currentPrice', 'N/A'),
        "52-Week High": info.get('fiftyTwoWeekHigh', 'N/A'),
        "52-Week Low": info.get('fiftyTwoWeekLow', 'N/A'),
        "Dividend Rate": info.get('dividendRate', 'N/A'),
        "Dividend Yield": info.get('dividendYield', 'N/A'),
        "Payout Ratio": info.get('payoutRatio', 'N/A'),
        "Beta": info.get('beta', 'N/A'),
        "Trailing P/E": info.get('trailingPE', 'N/A'),
        "Forward P/E": info.get('forwardPE', 'N/A'),
    }


    st.title(f"Information for {option}")


    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Company Details")
        st.write(f"**Phone:** {data_points['Phone']}")
        st.write(f"**Fax:** {data_points['Fax']}")
        st.write(f"**Website:** {data_points['Website']}")
        st.write(f"**Industry:** {data_points['Industry']}")
        st.write(f"**Sector:** {data_points['Sector']}")

    with col2:
        st.subheader("Financial Overview")
        st.metric(label="Market Cap", value=data_points['Market Cap'])
        st.metric(label="Enterprise Value", value=data_points['Enterprise Value'])
        st.metric(label="Revenue Per Share", value=data_points['Revenue Per Share'])
        st.metric(label="EBITDA", value=data_points['EBITDA'])
        st.metric(label="Total Revenue", value=data_points['Total Revenue'])
        st.metric(label="Total Debt", value=data_points['Total Debt'])
        st.metric(label="Debt to Equity", value=data_points['Debt to Equity'])


    with st.expander("Price and Dividend Information"):
        st.write(f"**Current Price:** {data_points['Current Price']}")
        st.write(f"**52-Week High:** {data_points['52-Week High']}")
        st.write(f"**52-Week Low:** {data_points['52-Week Low']}")
        st.write(f"**Dividend Rate:** {data_points['Dividend Rate']}")
        st.write(f"**Dividend Yield:** {data_points['Dividend Yield']}")
        st.write(f"**Payout Ratio:** {data_points['Payout Ratio']}")

 
    with st.expander("Additional Financial Ratios"):
        st.write(f"**Beta:** {data_points['Beta']}")
        st.write(f"**Trailing P/E:** {data_points['Trailing P/E']}")
        st.write(f"**Forward P/E:** {data_points['Forward P/E']}")

elif nav_option == "Volatility of Stock":
    st.title("Stock Volatility Heatmap")

    nifty50_tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS",
        "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ITC.NS",
        "ASIANPAINT.NS", "HCLTECH.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS",
        "NESTLEIND.NS", "TITAN.NS", "TECHM.NS", "WIPRO.NS", "HDFCLIFE.NS", "ADANIENT.NS",
        "TATASTEEL.NS", "ONGC.NS", "BAJAJFINSV.NS", "POWERGRID.NS", "INDUSINDBK.NS", "ADANIGREEN.NS",
        "JSWSTEEL.NS", "CIPLA.NS", "GRASIM.NS", "DIVISLAB.NS", "DRREDDY.NS", "NTPC.NS",
        "M&M.NS", "BPCL.NS", "SHREECEM.NS", "SBILIFE.NS", "EICHERMOT.NS", "COALINDIA.NS",
        "TATAMOTORS.NS", "HEROMOTOCO.NS", "BRITANNIA.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "DABUR.NS",
        "BAJAJ-AUTO.NS", "HINDALCO.NS"
    ]



    data = yf.download(nifty50_tickers, start="2023-01-01", end="2024-01-01")['Adj Close']


    returns = data.pct_change()


    volatility = returns.std()


    volatility_df = pd.DataFrame(volatility, columns=["Volatility"]).transpose()


    plt.figure(figsize=(54, 18))
    sns.heatmap(volatility_df, annot=True, cmap='Greens', cbar=True)
    plt.title('Stock Volatility Heatmap')
    plt.xlabel('Stock Tickers')
    plt.ylabel('Volatility')
    st.pyplot(plt)
    
elif nav_option == "About":
    st.header("About")
    st.write("This app is created to demonstrate a simple Streamlit navigation bar.")


