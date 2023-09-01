import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def sharpe_ratio(asset_returns: float, rfr: float): 
    """
    returns the sharpe ratio for an asset
    
    parameters:
        asset_returns (float): vector of daily asset returns
        rfr (float): scalar value of risk free rate
    returns:
        sharpe_ratio (float): sharpe ratio of asset
    """
    
    excess_rets = asset_returns - (rfr / 252)
    sigma = excess_rets.std()
    return np.sqrt(252) * (excess_rets.mean() / sigma)

    

def beta(index_returns: float, asset_returns: float):
    """
    returns the beta for an asset
    
    parameters:
        index_returns (float): vector of daily index returns
        asset_returns (float): vector of daily asset returns
    returns:
        beta (float): beta for an asset
    """
    
    covariance = np.cov(index_returns, asset_returns)[0][1]
    return covariance / np.var(index_returns)



def asset_drawdown(asset: str, start_time: str, end_time: str=None, plot: bool=False):
    """
    returns drawdown information for a given asset
    
    parameters:
        asset: asset ticker
        start_time: time to start analysis from
        end_time: optional time to end analysis data
        plot: optional bool to plot the information as opposed to receiving values
    returns:
        daily_drawdown (float, vector): vector of daily drawdowns
        max_daily_drawdowns (float, vector): vector of the maximum daily drawdown over a 252 day window 
    """
    
    data = yf.download(asset, start=start_time, end=end_time)["Adj Close"]
    window = 252
    
    rolling_max = data.rolling(window, min_periods=1).max()
    daily_drawdown = data / rolling_max - 1
    max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()
    
    print(f"Maximum Drawdown: {daily_drawdown.min() * 100:.2f}% on {daily_drawdown.idxmin().strftime('%d-%m-%Y')}")
    print(f"Recent {window} Day Maximum Drawdown: {max_daily_drawdown[-1] * 100:.2f}% on {max_daily_drawdown.loc[max_daily_drawdown == max_daily_drawdown[-1]].index[0].strftime('%d-%m-%Y')}")
    
    if plot:
        fig, ax = plt.subplots(2, 1, figsize=(18, 6), sharex=False)
        
        fig.suptitle(f"Drawdown Information for {asset}")

        ax[0].set_title("Drawdowns")
        ax[0].plot(daily_drawdown * 100, label="Daily Drawdown")
        ax[0].plot(max_daily_drawdown * 100, label=f"Rolling {window} Day Drawdown")
        ax[0].set_ylabel("% Change")
        ax[0].legend()

        ax[1].set_title(f"{asset} Price")
        ax[1].plot(data, label="Stock Price")
        ax[1].set_ylabel("Asset Price ($)")
        ax[1].legend()
    else:
        return daily_drawdown, max_daily_drawdown
    
    
    