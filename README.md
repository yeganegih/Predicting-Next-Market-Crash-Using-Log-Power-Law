# Detecting Stock-Market Bubbles with LPPLS

This repository demonstrates how to apply the **Log-Periodic Power Law Singularity (LPPLS)** model to the NASDAQ Composite index to look for signs of a financial bubble.

---

## 🧩  What is LPPL/LPPLS?

When markets get caught up in **herding behaviour**, prices can rise **faster than exponentially**.  
The LPPL model, developed by Didier Sornette and collaborators, describes such phases:

\[
\ln p(t) = A + B (t_c - t)^m + C (t_c - t)^m
           \cos\!\bigl[\omega \ln (t_c - t) - \phi \bigr]
\]

* **A, B, C** – constants describing the baseline and strength of the bubble.  
* **m** – how sharply the bubble accelerates (`0.1 < m < 0.9` for a classic bubble).  
* **ω (omega)** – frequency of the characteristic “wobbles” as the market approaches a critical time.  
* **t_c** – the model’s predicted “critical time”: when the bubble is expected to end (not necessarily a crash, but often a sharp regime change).

The **LPPLS** variant adds **filters**:
* enough oscillations between the start and end of the window (typically 2–10),
* reasonable relationship between the parameters,
* B negative (indicating super-exponential growth).

These filters reduce false alarms.

---

## 📊  Data

We used daily **NASDAQ Composite** data (adjusted close) from 2010–2025.

---

## 🧮  Method

* Three windows were analysed: **2-year**, **3-year**, and **4-year** trailing windows.
* For each window we ran a **multi-start bounded non-linear least squares** fit:
  * `0.1 < m < 0.9`
  * `6.5 ≤ ω ≤ 12.5`
  * `B < 0`
  * `t_c` at least slightly beyond the window end.

* We then applied the LPPLS filters (oscillation count and amplitude sanity checks).

---

## 🔎  Results

| Window | t_c estimate | Oscillations N | LPPLS Pass? |
|-------:|------------:|--------------:|:-----------:|
| 2-year | 2027-xx-xx  | < 2 | ❌ |
| 3-year | 2027-xx-xx  | < 2 | ❌ |
| 4-year | 2026-xx-xx  | < 2 | ❌ |

*(Replace “xx-xx” with the exact dates from your CSV results.)*

* Critical times were **10–18 months** after the last data point.
* Oscillation counts were **below 2**, so the **LPPLS filter failed** on all windows.

### ➡️  Interpretation

The model **did not detect a classic bubble signature**:
* The predicted “critical times” are far away.
* The market’s log-periodic oscillations are too weak for a reliable bubble signal.

In short: **no actionable early-warning** from LPPLS in this dataset.

---

## ▶️  How to reproduce

1. Install dependencies:
   ```bash
# Detecting Stock-Market Bubbles with LPPLS

This repository demonstrates how to apply the **Log-Periodic Power Law Singularity (LPPLS)** model to the NASDAQ Composite index to look for signs of a financial bubble.

---

## 🧩  What is LPPL/LPPLS?

When markets get caught up in **herding behaviour**, prices can rise **faster than exponentially**.  
The LPPL model, developed by Didier Sornette and collaborators, describes such phases:

\[
\ln p(t) = A + B (t_c - t)^m + C (t_c - t)^m
           \cos\!\bigl[\omega \ln (t_c - t) - \phi \bigr]
\]

* **A, B, C** – constants describing the baseline and strength of the bubble.  
* **m** – how sharply the bubble accelerates (`0.1 < m < 0.9` for a classic bubble).  
* **ω (omega)** – frequency of the characteristic “wobbles” as the market approaches a critical time.  
* **t_c** – the model’s predicted “critical time”: when the bubble is expected to end (not necessarily a crash, but often a sharp regime change).

The **LPPLS** variant adds **filters**:
* enough oscillations between the start and end of the window (typically 2–10),
* reasonable relationship between the parameters,
* B negative (indicating super-exponential growth).

These filters reduce false alarms.

---

## 📊  Data

We used daily **NASDAQ Composite** data (adjusted close) from 2010–2025.

---

## 🧮  Method

* Three windows were analysed: **2-year**, **3-year**, and **4-year** trailing windows.
* For each window we ran a **multi-start bounded non-linear least squares** fit:
  * `0.1 < m < 0.9`
  * `6.5 ≤ ω ≤ 12.5`
  * `B < 0`
  * `t_c` at least slightly beyond the window end.

* We then applied the LPPLS filters (oscillation count and amplitude sanity checks).

---

## 🔎  Results

| Window | t_c estimate | Oscillations N | LPPLS Pass? |
|-------:|------------:|--------------:|:-----------:|
| 2-year | 2027-xx-xx  | < 2 | ❌ |
| 3-year | 2027-xx-xx  | < 2 | ❌ |
| 4-year | 2026-xx-xx  | < 2 | ❌ |

*(Replace “xx-xx” with the exact dates from your CSV results.)*

* Critical times were **10–18 months** after the last data point.
* Oscillation counts were **below 2**, so the **LPPLS filter failed** on all windows.

### ➡️  Interpretation

The model **did not detect a classic bubble signature**:
* The predicted “critical times” are far away.
* The market’s log-periodic oscillations are too weak for a reliable bubble signal.

In short: **no actionable early-warning** from LPPLS in this dataset.

---

## ▶️  How to reproduce

1. Install dependencies:
   ```bash
   pip install numpy pandas matplotlib scipy
2. Download NASDAQ Composite daily prices (NASDAQ Composite Historical Data.csv)
and place it in the repository root.

Run:
Run:

python lppls_analysis.py


Plots for each window will be written into plots/.

## 📚 References

D. Sornette (2003). Why Stock Markets Crash: Critical Events in Complex Financial Systems.

Filimonov & Sornette (2013). "A stable and robust calibration scheme of the LPPL model."
