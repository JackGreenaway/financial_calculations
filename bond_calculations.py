"""
This file contains calculation functions to aid in bond analysis
"""


def bond_price(nominal, coupon, ytm, maturity, freq=2):
    """
    calculates the price of a bond
    
    parameters:
        nominal (float): the nominal value the bond
        coupon (float): the coupon rate of the bond (example: 0.06 (6%))
        ytm (float): the yield to maturity (example: 0.06 (6%))
        maturity (int): the number of years to maturity
    returns:
        bond_price (float): the price of the bond
    """
    
    total_payments = maturity * freq
    
    coupon_payment = (nominal * coupon) / freq
    
    discount_rate = ytm / freq 
    
    present_coupon_value = 0
    for t in range(1, total_payments + 1):
        present_coupon_value += coupon_payment / (1 + discount_rate) ** t
        
    present_nominal_value = nominal / (1 + discount_rate) ** total_payments
    
    bond_price = present_coupon_value + present_nominal_value
    
    return bond_price



def bond_duration(nominal, coupon, ytm, maturity, freq=2):
    """
    calculates the duration of a bond using the Macaulay equation
    
    parameters:
        nominal (float): the nominal value the bond
        coupon (float): the coupon rate of the bond (example: 0.06 (6%))
        ytm (float): the yield to maturity (example: 0.06 (6%))
        maturity (int): the number of years to maturity
        freq (int): the number of payments in a year
    returns:
        duration (float): the duration of the bond
        mod_duration (float): the modified version 
    """
    
    price = bond_price(nominal, coupon, ytm, maturity, freq=2)
    
    coupon_payment = (nominal * coupon) / freq
    total_periods = freq * maturity
    period_yield = ytm / freq
    
    numerator = 0
    for t in range(1, total_periods + 1):
        if t != total_periods:
            numerator += (t * coupon_payment) / (1 + period_yield) ** t

        else: 
            numerator += (total_periods * (nominal + coupon_payment)) / (1 + period_yield) ** total_periods

    duration = (numerator / price) / freq
    
    mod_duration = duration / (1 + (ytm / freq))
    
    return duration, mod_duration



def bond_convexity(nominal, coupon, ytm, maturity, freq=2):
    """
    estimates the convexity of a bond
    
    parameters:
        nominal (float): the nominal value the bond
        coupon (float): the coupon rate of the bond (example: 0.06 (6%))
        ytm (float): the yield to maturity (example: 0.06 (6%))
        maturity (int): the number of years to maturity
        freq (int): the number of payments in a year
    returns:
        convexity (float): returns the convexity of the bond
    """
    
    dy = 0.01
    
    ytm_minus = ytm - dy
    price_minus = bond_price(nominal, coupon, ytm_minus, maturity, freq=2)
    
    ytm_plus = ytm + dy
    price_plus = bond_price(nominal, coupon, ytm_plus, maturity, freq=2)
    
    price = bond_price(nominal, coupon, ytm, maturity, freq=2)

    convexity = (price_plus + price_minus - 2 * price) / (price * dy ** 2)
    
    return convexity



def bond_ytm(nominal, market_price, coupon, maturity):
    """
    estimates the yield to maturity of a bond
    
    parameters:
        nominal (float): the nominal value the bond
        market_price (float): current market price for the bond
        coupon (float): the coupon rate of the bond (example: 0.06 (6%))
        maturity (int): the number of years to maturity
    returns:
        ytm (float): returns the annual ytm of the bond
    """
    
    coupon_payment = nominal * coupon
    
    numerator = coupon_payment + ((nominal - market_price) / maturity)
    denominator = (nominal + market_price) / 2
    
    ytm = numerator / denominator
    
    return ytm



