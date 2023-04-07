import numpy as np

def absorption(f = 1000, t=10, rh=80, ps=1.01325e5):
    """ 
        Input:
        f: frequency in Hz
        t: temperature in °C
        rh: relative humidity in %
        ps: atmospheric pressure in Pa
        
        Output:
        alpha: attenuation coefficient

    """
    ps0 = ps
    T = t + 273.15
    T0 = 293.15
    T01 = 273.16
    
    Csat = -6.8346 * (T01/T)**1.261 + 4.6151
    rhosat = 10**Csat
    H = rhosat * rh * ps0 / ps
    frn = (ps / ps0) * (T0/T)**0.5 * (9 + 280 * H * np.exp(-4.17 * ((T0/T)**(1/3) - 1)))
    fro = (ps / ps0) * (24.0 + 4.04e4 * H * (0.02 + H) / (0.391 + H))
    alpha = 20/np.log(10) * f**2 * (1.84e-11 / ( (T0/T)**0.5 * ps / ps0 )+ (T/T0)**(-2.5)* (0.10680 * np.exp(-3352 / T) * frn / (f**2 + frn * frn)+ 0.01278 * np.exp(-2239.1 / T) * fro / (f**2 + fro * fro)))

    return alpha