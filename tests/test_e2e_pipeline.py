"""End-to-end integration and smoke tests for the complete fraud detection pipeline."""

import os
import pytest
import pandas as pd
from src.data_generator import generate_synthetic_transactions
from src.cleaning import clean_transaction_data
from src.rules import apply_all_rules_and_score
from src.visualization import generate_all_visualizations
from src.cli import run_fraud_pipeline


def test_visualization_generation(tmp_path):
    """Verify all 7 Matplotlib charts are rendered as non-empty PNG files."""
    raw = generate_synthetic_transactions(n=100, seed=42)
    cleaned, _ = clean_transaction_data(raw)
    scored, _ = apply_all_rules_and_score(cleaned)
    
    fig_dir = str(tmp_path / "figures")
    files = generate_all_visualizations(scored, output_dir=fig_dir)
    assert len(files) == 7
    for f in files:
        assert os.path.exists(f)
        assert os.path.getsize(f) > 5000, f"Chart file {f} is suspiciously small."


def test_run_fraud_pipeline_e2e(tmp_path):
    """Verify run_fraud_pipeline executes from raw generation to report export."""
    data_path = str(tmp_path / "bank_txns.csv")
    out_dir = str(tmp_path / "reports")
    
    result = run_fraud_pipeline(
        input_csv=None,
        generate_n=300,
        output_csv=data_path,
        reports_dir=out_dir,
        seed=42,
    )

    assert result["total_transactions"] == 300
    assert result["suspicious_count"] > 0
    assert os.path.exists(result["suspicious_csv_path"])
    assert os.path.exists(result["account_risk_csv_path"])
    assert os.path.exists(result["management_report_path"])
    assert len(result["figure_paths"]) == 7
    assert os.path.getsize(result["management_report_path"]) > 500


def test_cli_main_invocation(tmp_path, monkeypatch, capsys):
    """Verify that calling main() via CLI args functions properly."""
    import sys
    from src.cli import main
    
    out_dir = str(tmp_path / "cli_reports")
    data_path = str(tmp_path / "cli_data.csv")
    test_args = [
        "cli.py",
        "--generate", "150",
        "--output-csv", data_path,
        "--reports-dir", out_dir,
        "--seed", "99",
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    main()
    captured = capsys.readouterr()
    assert "BANK TRANSACTION FRAUD DETECTION" in captured.out
    assert "Processing Complete!" in captured.out
    assert os.path.exists(os.path.join(out_dir, "FRAUD_MONITORING_MANAGEMENT_REPORT.md"))

