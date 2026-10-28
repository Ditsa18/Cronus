"""Synthetic banking transaction dataset generator.

Generates realistic, anonymized banking transaction records conforming to Section 6
and Section 7 of the project specification. Incorporates realistic diurnal transaction
patterns, log-normal amount distributions, balance tracking, and intentional anomalous
bursts for fraud screening evaluation.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "Transaction_ID",
    "Account_ID",
    "Transaction_Date",
    "Transaction_Time",
    "Amount",
    "Transaction_Type",
    "Channel",
    "Merchant_Category",
    "Location",
    "Device_ID",
    "Balance_Before",
    "Balance_After",
    "Fraud_Label",
]

TRANSACTION_TYPES = ["Transfer", "Payment", "Withdrawal", "Deposit"]
CHANNELS = ["Online", "Mobile App", "ATM", "Branch"]
MERCHANT_CATEGORIES = [
    "Electronics",
    "Grocery",
    "Jewelry",
    "Entertainment",
    "Utilities",
    "Travel",
    "Healthcare",
    "Dining",
]
LOCATIONS = [
    "Kolkata",
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Hyderabad",
    "Pune",
]


def generate_synthetic_transactions(
    n: int = 10000,
    n_accounts: int = 500,
    fraud_rate: float = 0.04,
    start_date: str = "2026-09-01",
    seed: int = 42,
) -> pd.DataFrame:
    """Generate a synthetic DataFrame of banking transactions.

    Args:
        n: Total number of transactions to generate.
        n_accounts: Number of distinct customer accounts.
        fraud_rate: Approximate proportion of transactions with historical fraud.
        start_date: Start date for the transaction log.
        seed: Random seed for reproducibility.

    Returns:
        pd.DataFrame containing synthetic transactions matching REQUIRED_COLUMNS.
    """
    rng = np.random.default_rng(seed)

    # 1. Accounts and Devices Pool
    accounts = [f"ACC{1000 + i}" for i in range(n_accounts)]
    devices = [f"DEV{100 + i}" for i in range(n_accounts * 2)]
    account_primary_device = {
        acc: rng.choice(devices) for acc in accounts
    }
    account_balances = {
        acc: float(rng.uniform(15000, 350000)) for acc in accounts
    }

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    records = []
    txn_counter = 100000

    # Determine fraud vs legitimate counts
    n_fraud = int(n * fraud_rate)
    n_normal = n - n_fraud

    # Generate Normal Transactions
    for _ in range(n_normal):
        txn_counter += 1
        txn_id = f"TX{txn_counter}"
        acc_id = rng.choice(accounts)

        # Dates within 30 days
        day_offset = int(rng.integers(0, 30))
        txn_date = start_dt + timedelta(days=day_offset)

        # Diurnal distribution: mostly daytime (06:00 to 22:59)
        if rng.random() < 0.94:
            hour = int(rng.integers(6, 23))
        else:
            # Occasional legitimate night owl
            hour = int(rng.choice([23, 0, 1, 2, 3, 4, 5]))
        minute = int(rng.integers(0, 60))
        second = int(rng.integers(0, 60))

        # Legitimate amount: log-normal distribution (median ~1,800, mean ~3,500)
        raw_amt = float(rng.lognormal(mean=7.5, sigma=0.9))
        amount = round(max(50.0, min(raw_amt, 45000.0)), 2)

        txn_type = rng.choice(TRANSACTION_TYPES, p=[0.35, 0.40, 0.15, 0.10])
        channel = rng.choice(CHANNELS, p=[0.45, 0.40, 0.10, 0.05])
        merchant = rng.choice(MERCHANT_CATEGORIES)
        loc = rng.choice(LOCATIONS)
        device = account_primary_device[acc_id]

        bal_before = round(account_balances[acc_id], 2)
        if txn_type == "Deposit":
            bal_after = round(bal_before + amount, 2)
            account_balances[acc_id] = bal_after
        else:
            bal_after = round(max(0.0, bal_before - amount), 2)
            account_balances[acc_id] = bal_after

        records.append({
            "Transaction_ID": txn_id,
            "Account_ID": acc_id,
            "Transaction_Date": txn_date.strftime("%Y-%m-%d"),
            "Transaction_Time": f"{hour:02d}:{minute:02d}",
            "Amount": amount,
            "Transaction_Type": txn_type,
            "Channel": channel,
            "Merchant_Category": merchant,
            "Location": loc,
            "Device_ID": device,
            "Balance_Before": bal_before,
            "Balance_After": bal_after,
            "Fraud_Label": 0,
            "_datetime_sort": datetime(txn_date.year, txn_date.month, txn_date.day, hour, minute, second),
        })

    # Generate Fraud Anomalies
    # We create 3 types of fraud:
    # 1. High Amount Outlier at Late Night (Score 2 or 3)
    # 2. High-Frequency Bursts (rapid sequence of 5-8 transactions in 30 mins)
    # 3. High-Value Sudden Drain
    fraud_accounts = rng.choice(accounts, size=max(5, n_fraud // 5), replace=False)
    
    fraud_generated = 0
    while fraud_generated < n_fraud:
        acc_id = rng.choice(fraud_accounts)
        day_offset = int(rng.integers(0, 30))
        txn_date = start_dt + timedelta(days=day_offset)
        fraud_scenario = rng.choice(["late_high", "burst", "extreme_amount"])

        if fraud_scenario == "burst" and (n_fraud - fraud_generated) >= 5:
            # Inject burst of 5-7 transactions in 35 minutes
            burst_len = min(int(rng.integers(5, 8)), n_fraud - fraud_generated)
            base_hour = int(rng.choice([23, 1, 2, 3, 14, 19]))
            base_minute = int(rng.integers(0, 20))
            device = f"DEV{rng.integers(800, 999)}"  # suspicious new device
            loc = rng.choice(LOCATIONS)

            for b in range(burst_len):
                txn_counter += 1
                b_min = base_minute + (b * 4)
                b_hour = base_hour + (b_min // 60)
                b_min = b_min % 60
                b_hour = b_hour % 24
                b_amt = round(float(rng.uniform(8000, 48000)), 2)
                bal_before = round(account_balances[acc_id], 2)
                bal_after = round(max(0.0, bal_before - b_amt), 2)
                account_balances[acc_id] = bal_after

                records.append({
                    "Transaction_ID": f"TX{txn_counter}",
                    "Account_ID": acc_id,
                    "Transaction_Date": txn_date.strftime("%Y-%m-%d"),
                    "Transaction_Time": f"{b_hour:02d}:{b_min:02d}",
                    "Amount": b_amt,
                    "Transaction_Type": "Transfer",
                    "Channel": "Online",
                    "Merchant_Category": "Electronics",
                    "Location": loc,
                    "Device_ID": device,
                    "Balance_Before": bal_before,
                    "Balance_After": bal_after,
                    "Fraud_Label": 1,
                    "_datetime_sort": datetime(txn_date.year, txn_date.month, txn_date.day, b_hour, b_min, 10 + b),
                })
                fraud_generated += 1

        elif fraud_scenario == "late_high":
            txn_counter += 1
            hour = int(rng.choice([23, 0, 1, 2, 3, 4]))
            minute = int(rng.integers(0, 60))
            amount = round(float(rng.uniform(65000, 145000)), 2)  # Well above 99th percentile
            bal_before = round(account_balances[acc_id] + amount + 10000, 2)
            bal_after = round(bal_before - amount, 2)
            account_balances[acc_id] = bal_after

            records.append({
                "Transaction_ID": f"TX{txn_counter}",
                "Account_ID": acc_id,
                "Transaction_Date": txn_date.strftime("%Y-%m-%d"),
                "Transaction_Time": f"{hour:02d}:{minute:02d}",
                "Amount": amount,
                "Transaction_Type": "Transfer",
                "Channel": "Online",
                "Merchant_Category": "Jewelry",
                "Location": rng.choice(LOCATIONS),
                "Device_ID": f"DEV{rng.integers(800, 999)}",
                "Balance_Before": bal_before,
                "Balance_After": bal_after,
                "Fraud_Label": 1,
                "_datetime_sort": datetime(txn_date.year, txn_date.month, txn_date.day, hour, minute, 15),
            })
            fraud_generated += 1

        else:  # extreme_amount
            txn_counter += 1
            hour = int(rng.integers(9, 21))
            minute = int(rng.integers(0, 60))
            amount = round(float(rng.uniform(90000, 220000)), 2)
            bal_before = round(account_balances[acc_id] + amount + 5000, 2)
            bal_after = round(bal_before - amount, 2)
            account_balances[acc_id] = bal_after

            records.append({
                "Transaction_ID": f"TX{txn_counter}",
                "Account_ID": acc_id,
                "Transaction_Date": txn_date.strftime("%Y-%m-%d"),
                "Transaction_Time": f"{hour:02d}:{minute:02d}",
                "Amount": amount,
                "Transaction_Type": "Transfer",
                "Channel": "Online",
                "Merchant_Category": "Electronics",
                "Location": rng.choice(LOCATIONS),
                "Device_ID": account_primary_device[acc_id],
                "Balance_Before": bal_before,
                "Balance_After": bal_after,
                "Fraud_Label": 1,
                "_datetime_sort": datetime(txn_date.year, txn_date.month, txn_date.day, hour, minute, 45),
            })
            fraud_generated += 1

    df = pd.DataFrame(records)
    # Sort chronologically
    df = df.sort_values(by="_datetime_sort").reset_index(drop=True)
    df = df.drop(columns=["_datetime_sort"])
    # Re-slice to exact requested row count
    df = df.head(n).copy()

    return df[REQUIRED_COLUMNS]


def save_synthetic_dataset(filepath: str, n: int = 10000, seed: int = 42) -> pd.DataFrame:
    """Generate and save the synthetic dataset to CSV."""
    df = generate_synthetic_transactions(n=n, seed=seed)
    df.to_csv(filepath, index=False)
    return df
