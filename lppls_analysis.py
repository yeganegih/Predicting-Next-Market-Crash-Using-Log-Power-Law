
---

## lppls_analysis.py  (simplified script)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from datetime import timedelta

def lppl(t, A, B, C, m, w, phi, tc):
    dt = np.maximum(tc - t, 1e-10)
    return A + B*(dt**m) + C*(dt**m)*np.cos(w*np.log(dt) - phi)

def fit_lppl_bounded(t, prices, n_starts=150, rng_seed=42):
    y = np.log(prices); tmax = t.max()
    def resid(theta): return lppl(t,*theta)-y
    lower = [-np.inf, -np.inf, -np.inf, 0.1, 6.5, -10*np.pi, tmax+0.01]
    upper = [ np.inf, -1e-12,  np.inf, 0.9, 12.5,  10*np.pi, tmax+2.0]
    rng = np.random.default_rng(rng_seed)
    best, cost = None, np.inf
    for _ in range(n_starts):
        x0 = [np.median(y),
              -abs(rng.uniform(0.01,0.5)),
              rng.uniform(-0.1,0.1),
              rng.uniform(0.15,0.85),
              rng.uniform(6.6,12.4),
              rng.uniform(-np.pi,np.pi),
              tmax + rng.uniform(0.05,1.5)]
        res = least_squares(resid, x0, bounds=(lower,upper), method='trf')
        if res.success and res.cost < cost:
            best, cost = res.x, res.cost
    return best

def analyse_window(df, years):
    end = df.index.max()
    start = end - pd.DateOffset(years=years)
    w = df.loc[start:end]
    t = (w.index - w.index[0]).days.values/365.25
    p = w['Close'].values
    pars = fit_lppl_bounded(t,p)
    tc_date = w.index[0] + pd.Timedelta(days=float(pars[6])*365.25)
    t_fit = np.linspace(t.min(), min(pars[6]-1e-3, t.max()+0.25), 800)
    y_fit = lppl(t_fit,*pars)
    p_fit = np.exp(y_fit)
    fit_dates = [w.index[0] + pd.Timedelta(days=float(tt)*365.25) for tt in t_fit]
    plt.figure(figsize=(10,6))
    plt.plot(w.index, w['Close'], label='NASDAQ Close')
    plt.plot(fit_dates, p_fit, label='LPPL fit')
    plt.axvline(tc_date, linestyle='--', alpha=0.6, label=f"t_c ≈ {tc_date.date()}")
    plt.title(f"LPPL fit — {years}-year window")
    plt.xlabel("Date"); plt.ylabel("Index Level")
    plt.legend(); plt.tight_layout()
    plt.savefig(f"plots/lppls_{years}y.png")
    plt.close()
    print(f"{years}-year window: t_c ≈ {tc_date.date()}")

if __name__ == "__main__":
    df = pd.read_csv("NASDAQ Composite Historical Data.csv")
    df = df.iloc[:, :2]
    df.columns = ["Date","Close"]
    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"].astype(str).str.replace(",",""))
    df = df.dropna().sort_values("Date").set_index("Date")
    for y in [2,3,4]:
        analyse_window(df, y)
