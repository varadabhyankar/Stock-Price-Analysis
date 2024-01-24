# Raw Package
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
from plotly.offline import plot

# Market Data
import yfinance as yf

# Graphing/Visualization
import plotly.graph_objs as go
from plotly.subplots import make_subplots
yf.pdr_override()

input1 = 'NVDA'
input2 = 'withIndices'
stock = input1

def plotFunction(company_name, graph_type):
    
    plot_html =''
    input2 = graph_type
    stock = company_name
    # Function to calculate Bollinger Bands
    def calculate_bollinger_bands(data, window=20, num_std=2):
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return upper_band, lower_band

    # Function to calculate RSI
    def calculate_rsi(data, window=14):
        delta = data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Function to calculate moving averages
    def calculate_moving_averages(data):
        if(len(data.index)>151):MA_150 = data['Close'].rolling(window=150).mean()
        if(len(data.index)>51):MA_50 = data['Close'].rolling(window=50).mean()
        if(len(data.index)>31):MA_30 = data['Close'].rolling(window=30).mean()
        MA_15 = data['Close'].rolling(window=15).mean()
        if(len(data.index)>151):
            return MA_150, MA_50, MA_30, MA_15
        elif(len(data.index)>51):
            return MA_50, MA_30, MA_15
        elif(len(data.index)>31):
            return MA_30, MA_15
        else:
            return MA_15

    if input2 == "longTerm" or input2=="withIndices":
        # For Long scenario
        df = yf.download(tickers=stock, period='5y', interval='1d')
        if(input2 == "longTerm"):
            fig_long = go.Figure()
            fig_long.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Market Data', mode='lines'))
            fig_long.update_layout(
                title=str(stock) + ' Live Share Price:',
                yaxis_title='Stock Price (USD per Shares)')
            fig_long.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="5D", step="day", stepmode="backward"),
                        dict(count=30, label="1M", step="day", stepmode="backward"),
                        dict(count=180, label="6M", step="day", stepmode="backward"),
                        dict(count=365, label="1Y", step="day", stepmode="backward"),
                        dict(count=1095, label="3Y", step="day", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            plot_html = plot(fig_long, output_type='div')
        else:
            df['Upper_band'], df['Lower_band'] = calculate_bollinger_bands(df)
            df['RSI'] = calculate_rsi(df)
            if(len(df.index)>151):
                df['MA_150'], df['MA_50'], df['MA_30'], df['MA_15'] = calculate_moving_averages(df)
            elif(len(df.index)>51):
                df['MA_50'], df['MA_30'], df['MA_15'] = calculate_moving_averages(df)
            elif(len(df.index)>31):
                df['MA_30'], df['MA_15'] = calculate_moving_averages(df)
            elif(len(df.index)>16):
                df['MA_15'] = calculate_moving_averages(df)
            fig_analysis = go.Figure()
            fig_analysis = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=[f'{stock} Live Share Price', 'RSI'], row_heights=[0.67,0.33])
            fig_analysis.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Market Data', mode='lines'),row=1, col=1)
            fig_analysis.add_trace(go.Scatter(x=df.index, y=df['Upper_band'], name='Upper Bollinger Band', line=dict(color='red', width=1)),row=1, col=1)
            fig_analysis.add_trace(go.Scatter(x=df.index, y=df['Lower_band'], name='Lower Bollinger Band', line=dict(color='red', width=1)),row=1, col=1)
            if(len(df.index)>151):fig_analysis.add_trace(go.Scatter(x=df.index, y=df['MA_150'], name='150-day Moving Average', line=dict(color='green', width=1)),row=1, col=1)
            if(len(df.index)>51):fig_analysis.add_trace(go.Scatter(x=df.index, y=df['MA_50'], name='50-day Moving Average', line=dict(color='orange', width=1)),row=1, col=1)
            if(len(df.index)>31):fig_analysis.add_trace(go.Scatter(x=df.index, y=df['MA_30'], name='30-day Moving Average', line=dict(color='lime', width=1)),row=1, col=1)
            if(len(df.index)>16):fig_analysis.add_trace(go.Scatter(x=df.index, y=df['MA_15'], name='15-day Moving Average', line=dict(color='gray', width=1)),row=1, col=1)
            fig_analysis.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple', width=1)),row=2,col=1)
            
            fig_analysis.update_layout(
            title=f'{stock} Live Share Price and RSI',
            yaxis_title='Stock Price (USD per Share)',
            yaxis2_title='RSI',
            xaxis2=dict(title='Date')
            )

            fig_analysis.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="5D", step="day", stepmode="backward"),
                        dict(count=30, label="1M", step="day", stepmode="backward"),
                        dict(count=180, label="6M", step="day", stepmode="backward"),
                        dict(count=365, label="1Y", step="day", stepmode="backward"),
                        dict(count=1095, label="3Y", step="day", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            plot_html = plot(fig_analysis, output_type='div')

    elif input2 == 'shortTerm':
        # For Short scenario
        df = yf.download(tickers=stock, period='1d', interval='1m')
        fig_short = go.Figure()
        fig_short.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Market Data', mode='lines'))
        fig_short.update_layout(
            title=str(stock) + ' Live Share Price:',
            yaxis_title='Stock Price (USD per Shares)')
        fig_short.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        plot_html = plot(fig_short, output_type='div')

    return plot_html
        