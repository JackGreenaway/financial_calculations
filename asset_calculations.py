

def sharpe_ratio(asset_returns, rfr): 
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
    
    

def beta(index_returns, asset_returns):
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
    
    