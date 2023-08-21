"""
This file contains calculation functions to aid in bond analysis
"""
import numpy as np


def bond_price(nominal: float, coupon: float, ytm: float, maturity: int, freq=2):
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



def bond_duration(nominal: float, coupon: float, ytm: float, maturity: int, freq: int=2):
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



def bond_convexity(nominal: float, coupon: float, ytm: float, maturity: int, freq: int=2):
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



def bond_ytm(nominal: float, market_price: float, coupon: float, maturity: int):
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



def adjusted_bond_price(nominal: float, coupon: float, ytm: float, maturity: int, freq: int=2, yield_changes: list=[-0.15, 0.15, 0.0001], return_yields=False):
    """
    returns the list of adjusted bond prices with use of duration and convexity
    
    parameters:
        nominal (float): the nominal value the bond
        coupon (float): the coupon rate of the bond (example: 0.06 (6%))
        ytm (float): the yield to maturity (example: 0.06 (6%))
        maturity (int): the number of years to maturity
        freq (int): the number of payments in a year
        yield_changes (list): the range of rate changes to test with the step
        return_yields (bool): returns the list of yields for aid in plotting
    returns:
        bond_prices (list): vector of bond_prices corresponding to rate
        yield_change_range (list)
    """
    
    yield_change_range = np.arange(yield_changes[0], yield_changes[1], yield_changes[2])
    
    duration = bond_duration(nominal=nominal, coupon=coupon, ytm=ytm, maturity=maturity, freq=2)[1]
    conv = bond_convexity(nominal=nominal, coupon=coupon, ytm=ytm, maturity=maturity, freq=2)
    price = bond_price(nominal=nominal, coupon=coupon, ytm=ytm, maturity=maturity, freq=2)

    bond_prices = []
    # Δ bond price = -duration * Δy * 1/2 * conv * (Δy) ** 2
    for i in yield_change_range:
        one = -duration * i
        two = 1/2 * conv * (i ** 2)
        three = (one + two) + 1 # the 1 is added so you can just multiply by this value (e.g, 0.09 vs 1.09 for a 9% increase)
        
        bond_prices.append(three * price)
        
    if return_yields:
        return bond_prices, yield_change_range
    else:
        return bond_prices



