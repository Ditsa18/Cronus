"""Visualization suite using Matplotlib.

Implements Sections 26 through 30 and Section 35 of the project specification:
1. Chart 1: Distribution of Transaction Amounts (Histogram + Log scale / KDE)
2. Chart 2: Normal vs Suspicious Transactions (Comparative Bar Chart)
3. Chart 3: Suspicious Transactions by Hour of Day (Trend Line Chart)
4. Chart 4: Suspicious Rate by Transaction Type (Bar Chart)
5. Chart 5: Transaction Amount vs Suspicion Score (Scatter Plot)
6. Chart 6: Rule Combination Frequencies (Horizontal Bar Chart)
7. Chart 7: Suspicious Rate by Channel (Vulnerability Bar Chart)
"""

import os
from typing import Dict, Any, List
import matplotlib
matplotlib.use("Agg")  # Force non-interactive headless backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.analytics import (
    get_type_analysis,
    get_channel_analysis,
    get_hour_analysis,
    get_rule_combination_analysis,
)


def generate_all_visualizations(df: pd.DataFrame, output_dir: str = "reports/figures") -> List[str]:
    """Generate and save all 7 publication-ready charts to output_dir.

    Args:
        df: Scored transaction DataFrame.
        output_dir: Directory where PNG charts will be saved.

    Returns:
        List of generated image file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []

    # Chart 1: Amount Distribution (Sec 26)
    path_1 = os.path.join(output_dir, "01_amount_distribution.png")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["Amount"].dropna(), bins=40, color="#1f77b4", edgecolor="black", alpha=0.75)
    ax.set_title("Distribution of Transaction Amounts", fontsize=14, fontweight="bold")
    ax.set_xlabel("Transaction Amount ($)", fontsize=11)
    ax.set_ylabel("Number of Transactions", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(path_1, dpi=200)
    plt.close(fig)
    generated_files.append(path_1)

    # Chart 2: Normal vs Suspicious (Sec 27)
    path_2 = os.path.join(output_dir, "02_normal_vs_suspicious.png")
    counts = df["Suspicious"].value_counts().sort_index()
    labels = ["Normal (Score 0-1)", "Suspicious (Score 2-3)"]
    vals = [counts.get(0, 0), counts.get(1, 0)]
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, vals, color=["#2ca02c", "#d62728"], edgecolor="black", width=0.55)
    ax.set_title("Normal vs Suspicious Transactions", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Transactions", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,} ({h/len(df)*100:.1f}%)",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    fig.savefig(path_2, dpi=200)
    plt.close(fig)
    generated_files.append(path_2)

    # Chart 3: Suspicious by Hour (Sec 28)
    path_3 = os.path.join(output_dir, "03_suspicious_by_hour.png")
    hour_df = get_hour_analysis(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hour_df["Hour"], hour_df["Suspicious"], marker="o", color="#d62728", linewidth=2.2, markersize=6)
    # Highlight late-night window
    ax.axvspan(-0.5, 5.5, color="#ff7f0e", alpha=0.15, label="Late-Night Window (23:00 - 05:59)")
    ax.axvspan(22.5, 23.5, color="#ff7f0e", alpha=0.15)
    ax.set_title("Suspicious Transactions by Hour of Day", fontsize=14, fontweight="bold")
    ax.set_xlabel("Hour of Day (0 - 23)", fontsize=11)
    ax.set_ylabel("Suspicious Transactions", fontsize=11)
    ax.set_xticks(range(24))
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")
    plt.tight_layout()
    fig.savefig(path_3, dpi=200)
    plt.close(fig)
    generated_files.append(path_3)

    # Chart 4: Suspicious Rate by Type (Sec 29)
    path_4 = os.path.join(output_dir, "04_suspicious_rate_by_type.png")
    type_df = get_type_analysis(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(type_df["Transaction_Type"], type_df["Suspicious_Rate"], color="#9467bd", edgecolor="black", width=0.5)
    ax.set_title("Suspicious Rate by Transaction Type", fontsize=14, fontweight="bold")
    ax.set_xlabel("Transaction Type", fontsize=11)
    ax.set_ylabel("Suspicious Rate (%)", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    fig.savefig(path_4, dpi=200)
    plt.close(fig)
    generated_files.append(path_4)

    # Chart 5: Amount vs Suspicion Score (Sec 30)
    path_5 = os.path.join(output_dir, "05_amount_vs_suspicion_score.png")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Suspicion_Score"], df["Amount"], color="#e377c2", alpha=0.45, edgecolors="none")
    ax.set_title("Transaction Amount vs Suspicion Score", fontsize=14, fontweight="bold")
    ax.set_xlabel("Suspicion Score (0 to 3)", fontsize=11)
    ax.set_ylabel("Transaction Amount ($)", fontsize=11)
    ax.set_xticks([0, 1, 2, 3])
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(path_5, dpi=200)
    plt.close(fig)
    generated_files.append(path_5)

    # Chart 6: Rule Combination Frequencies (Sec 32 & 35)
    path_6 = os.path.join(output_dir, "06_rule_combination_frequencies.png")
    comb_df = get_rule_combination_analysis(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(comb_df["Rule_Combination"] + " (" + comb_df["Description"].str.slice(0, 22) + ")",
                   comb_df["Transactions"], color="#8c564b", edgecolor="black")
    ax.invert_yaxis()
    ax.set_title("Transactions by Rule Combination Bitmask", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Transactions", fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:,}",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    fig.savefig(path_6, dpi=200)
    plt.close(fig)
    generated_files.append(path_6)

    # Chart 7: Suspicious Rate by Channel (Sec 22 & 35)
    path_7 = os.path.join(output_dir, "07_suspicious_rate_by_channel.png")
    ch_df = get_channel_analysis(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(ch_df["Channel"], ch_df["Suspicious_Rate"], color="#17becf", edgecolor="black", width=0.5)
    ax.set_title("Suspicious Rate by Transaction Channel", fontsize=14, fontweight="bold")
    ax.set_xlabel("Channel", fontsize=11)
    ax.set_ylabel("Suspicious Rate (%)", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    fig.savefig(path_7, dpi=200)
    plt.close(fig)
    generated_files.append(path_7)

    return generated_files
