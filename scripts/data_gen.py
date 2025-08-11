#!/usr/bin/env python3
"""
Generates synthetic CRM/ticketing data to match the reference dashboard.
Only uses numpy and pandas.
"""
import numpy as np
import pandas as pd

def gen_kpis(path="../data/metrics.csv", seed=1):
    np.random.seed(seed)
    metrics = [
        ("Avg First Reply Time (h)", 30.25, -2.1, "", "h"),
        ("Avg Full Resolve Time (h)", 22.67, 1.4, "", "h"),
        ("Messages (7d)", 820, -0.2, "", ""),
        ("Emails (7d)", 1330, 0.33, "", ""),
    ]
    pd.DataFrame(metrics, columns=["metric","value","delta","prefix","suffix"]).to_csv(path, index=False)

def gen_timeseries(path="../data/tickets_timeseries.csv", seed=2):
    np.random.seed(seed)
    dates = pd.date_range("2024-01-01","2024-07-31", freq="D")
    created = np.clip(40 + 15*np.sin(np.linspace(0,3.2,len(dates))) + np.random.normal(0,6,len(dates)), 5, None).round()
    solved  = np.clip(created - np.random.normal(2,3,len(dates)), 3, None).round()
    pd.DataFrame({"date":dates,"tickets_created":created,"tickets_solved":solved}).to_csv(path, index=False)

def gen_by_type(path="../data/tickets_by_type.csv", seed=3):
    np.random.seed(seed)
    types = ["Sales","Setup","Bug","Features"]
    counts = np.random.randint(200, 1000, len(types))
    pd.DataFrame({"type":types,"count":counts}).to_csv(path, index=False)

def gen_new_vs_returned(path="../data/new_vs_returned.csv", seed=4):
    np.random.seed(seed)
    new = np.random.randint(700, 1400)
    returned = np.random.randint(200, 600)
    pd.DataFrame({"label":["New Tickets","Returned Tickets"],"count":[new, returned]}).to_csv(path, index=False)

def gen_weekday(path="../data/tickets_by_weekday.csv", seed=5):
    np.random.seed(seed)
    days = ["Mon","Tue","Wed","Thu","Fri","Sat"]
    vals = np.random.randint(20, 110, len(days))
    pd.DataFrame({"weekday":days,"count":vals}).to_csv(path, index=False)

def main():
    gen_kpis()
    gen_timeseries()
    gen_by_type()
    gen_new_vs_returned()
    gen_weekday()

if __name__ == "__main__":
    main()
