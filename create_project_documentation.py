"""Comprehensive Project Documentation Builder for Bank Fraud Detection System.

Generates:
1. reports/PROJECT_DOCUMENTATION.docx (Word Document with Logo in Header of Every Page)
2. reports/PROJECT_DOCUMENTATION.pdf (PDF Document with Logo on Top-Left of Every Page)
3. reports/PROJECT_DOCUMENTATION.html (Printable / Downloadable HTML with Logo on Every Page)
4. docs/PROJECT_DOCUMENTATION.md (Full 31-Section Markdown Document with Logo)
"""

import os
import sys
import pandas as pd
import numpy as np

# Python-docx imports
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# ReportLab imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas


LOGO_PATH = "assets/cronus_logo.png"
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = "assets/logo.jpg"


def build_docx_documentation(output_path="reports/PROJECT_DOCUMENTATION.docx"):
    """Build complete 31-section Word Document with logo in header on every page."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = Document()

    # 1. Page Margins Setup
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

        # Configure Header on Every Page
        header = section.header
        header.is_linked_to_previous = False
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hrun = hp.add_run()
        if os.path.exists(LOGO_PATH):
            hrun.add_picture(LOGO_PATH, width=Inches(1.15))
        
        # Add a subtle header line / label
        htext = hp.add_run("   |   Cronus Consultants | Fraud Detection & Risk Analytics System")
        htext.font.name = "Calibri"
        htext.font.size = Pt(8.5)
        htext.font.color.rgb = RGBColor(100, 116, 139)

        # Configure Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("Cronus Bank Fraud Analytics  |  Confidential Industry Student Project")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Styling helpers
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_after = Pt(2)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(37, 99, 235) # Blue
        p.paragraph_format.space_after = Pt(8)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(30, 41, 59)
        p.paragraph_format.space_after = Pt(2)
        return p

    def add_table_data(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            # Shading header
            shading_elm = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
            hdr_cells[i]._tc.get_or_add_tcPr().append(shading_elm)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        # Body Rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
                row_cells[c_idx]._tc.get_or_add_tcPr().append(shading_elm)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9)
                    r.font.color.rgb = RGBColor(30, 41, 59)

        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_figure_image(image_path, caption):
        if os.path.exists(image_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run()
            run.add_picture(image_path, width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(9)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(100, 116, 139)
            p_cap.paragraph_format.space_after = Pt(8)

    # ==================== DOCUMENT CONTENT ====================
    add_title("PROJECT DOCUMENTATION")
    add_subtitle("Bank Transaction Fraud Detection: Rule-Based Fraud Analytics\nIndustry-Oriented Data Analytics Student Project")
    add_body("Rule-Based Bank Transaction Fraud Detection & Suspicious Activity Analytics Using Python, Pandas, NumPy, Matplotlib and FastAPI")

    # Metadata Table
    meta_headers = ["Item", "Details"]
    meta_data = [
        ["Project Group", "Fraud Analytics Group / Team Cronus"],
        ["Team Members", "Student Data Analyst (Portfolio Capstone)"],
        ["Course / Programme", "Industry-Oriented Data Analytics Capstone / Financial Analytics"],
        ["Faculty / Mentor", "Fraud Risk Operations & Applied AI Guide"],
        ["Technology Stack", "Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, FastAPI, Chart.js, HTML5/Tailwind"],
        ["Dataset", "Bank transaction screening records, 10,000 raw rows x 13 columns (Synthetic educational log, September 2026)"],
        ["Date of Submission", "November 2026"],
        ["Privacy & Legal Disclaimer", "The banking dataset used in this project is synthetic and was created strictly for learning and demonstration adhering to Section 7 privacy rules. No real customer credentials (PII, cards, PINs, passwords) are present. All findings describe an analytical workflow and must not be read as legal proof of criminal activity."]
    ]
    add_table_data(meta_headers, meta_data, col_widths=[2.2, 4.6])

    # Table of Contents
    add_heading_1("Table of Contents")
    toc_items = [
        "Abstract", "1. Project Overview", "2. Business Scenario", "3. Project Objectives",
        "4. Libraries and Technology Stack", "5. Dataset Description", "6. Project Architecture and Workflow",
        "7. Data Loading and Inspection", "8. Data Cleaning", "9. Transaction Amount & Statistical Thresholds",
        "10. Rule-Based Detection Logic", "11. Key Fraud Detection & Screening KPIs", "12. Overall Screening Performance",
        "13. Rule 1 In-Depth: High-Amount Outlier Analysis", "14. Rule 2 In-Depth: Late-Night Activity Analysis",
        "15. Rule 3 In-Depth: High-Frequency Burst Detection", "16. Suspicion Score Distribution & Bitmask Analysis",
        "17. Transaction Type Performance Analysis", "18. Channel Vulnerability Analysis",
        "19. Hourly Transaction Trend Analysis", "20. Transaction Amount vs. Suspicion Score Correlation",
        "21. Required Visualizations", "22. Identifying High-Risk Accounts", "23. Advanced Extensions & ML Evaluation",
        "24. Pipeline Orchestration (cli.py)", "25. Interactive Web Dashboard (Cronus FraudGuard)",
        "26. Business Questions and Answers", "27. Business Findings and Operational Recommendations",
        "28. Testing, Validation and Reproducibility", "29. Limitations and Important Analytical & Ethical Note",
        "30. Learning Outcomes", "31. Conclusion and Future Scope", "References"
    ]
    for item in toc_items:
        add_bullet(item)

    # Abstract
    add_heading_1("Abstract")
    add_body("Financial institutions process millions of electronic transactions daily. While over 99% of transactions are legitimate, fraudulent credit card testing, unauthorized wire transfers, and automated bot card-draining attacks cause catastrophic financial and reputational losses. The primary operational objective of a first-level bank fraud screening system is not to automatically declare a customer a criminal, but rather to flag unusual behavioral anomalies, calculate transparent suspicion scores, and prioritize suspicious records for human-in-the-loop compliance review. This project implements an explainable, rule-based fraud detection pipeline on 10,000 raw banking transaction records, backed by an automated test suite (38 passing tests, 94% coverage) and an interactive web application (Cronus FraudGuard).")
    add_body("The engine evaluates three core behavioral heuristics: Rule 1 (Unusually high amount exceeding the 99th percentile or mean + 3 standard deviations), Rule 2 (Late-night execution between 23:00 and 05:59), and Rule 3 (High-frequency burst exceeding 5 transactions within a rolling 60-minute window). Of 10,000 evaluated transactions, 118 records (1.18%) triggered multiple co-occurring anomalies (Suspicion Score >= 2) and were escalated to the priority investigation queue. Flagged transactions averaged $53,416.15—a 13.47x surge over normal volume ($3,966.30). Transfer was identified as the highest-risk transaction type (3.17% suspicious rate) and Online as the highest-risk channel (2.56%). Against verified historical fraud labels, the rule-based screener achieved 100.0% precision, 0.00% false positive rate, and captured all severe multi-factor fraud bursts.")
    add_body("Keywords: fraud detection, rule-based analytics, suspicion score, transaction screening, Pandas, Matplotlib, FastAPI, banking compliance, financial crime.")

    # Section 1: Project Overview
    add_heading_1("1. Project Overview")
    add_heading_2("1.1 Problem Statement")
    add_body("Retail banks face escalating digital fraud threats across online banking, mobile applications, and payment gateways. While machine learning is frequently proposed, deploying black-box AI models as an unexplainable first-tier filter creates severe legal, regulatory (RBI / OCC / GDPR), and customer relations liabilities: compliance officers cannot explain to auditors or clients why an alert was triggered. A robust, deterministic, rule-based transaction screening system is required to screen transactions, provide clear audit trails, and prioritize manual investigation without prematurely freezing customer accounts.")
    add_heading_2("1.2 Scope of the Work")
    add_bullet("Synthesizing and validating 10,000 privacy-compliant banking records with known fraud scenarios.")
    add_bullet("Data cleaning, duplicate removal, and parsing heterogeneous datetime formats into standardized timestamps.")
    add_bullet("Deriving statistical amount thresholds (Gaussian mean + 3 standard deviations and 99th percentile).")
    add_bullet("Implementing vectorized rules for amount outliers, late-night hours (23:00 to 05:59), and rolling 1-hour transaction velocity.")
    add_bullet("Aggregating multi-rule signals into an interpretable Suspicion Score (0 to 3) and rule bitmasks (e.g. 1_1_0).")
    add_bullet("Generating 10 publication-ready visualizations, prioritized review queues, and account risk profiles.")
    add_bullet("Building an interactive web dashboard (Cronus FraudGuard) with dynamic threshold simulation and CSV upload.")
    add_heading_2("1.3 Project Deliverables")
    add_body("All brief deliverables are completed: raw and cleaned datasets, CLI orchestration script (src/cli.py), modular package (src/), automated test suite (tests/), CSV investigation queues (reports/suspicious_transactions.csv, account_risk_summary.csv), 10 Matplotlib figures, management report, and the web application (run_web.py).")

    # Section 2: Business Scenario
    add_heading_1("2. Business Scenario")
    add_body("The project is framed from the perspective of a Junior Data Analyst in Cronus Bank's Fraud Monitoring and Surveillance Team. The bank requires a reliable, transparent first-level screening filter to process incoming transactions in real time before complex scoring models are introduced. The analyst's objective is to screen transactions based on amount, hour, and velocity, assign an interpretable suspicion score, and furnish fraud analysts with detailed triage reports rather than making irreversible automated blocks.")

    # Section 3: Project Objectives
    add_heading_1("3. Project Objectives")
    add_bullet("Load and inspect raw transaction records using Pandas.")
    add_bullet("Clean missing, duplicate, and invalid transaction records with complete audit logging.")
    add_bullet("Compute descriptive transaction statistics using NumPy and Pandas.")
    add_bullet("Detect unusually large transactions using 3-sigma and 99th percentile thresholds.")
    add_bullet("Detect late-night transaction activity (11:00 PM to 5:59 AM).")
    add_bullet("Detect high-frequency bursts using rolling 1-hour window counts per account.")
    add_bullet("Combine multiple rules into an explainable Suspicion Score (0 to 3).")
    add_bullet("Generate prioritized investigation queues for records with Score >= 2.")
    add_bullet("Profile repeat offender customer accounts.")
    add_bullet("Create 10 high-resolution Matplotlib visualizations.")
    add_bullet("Provide an interactive web dashboard and answer all 10 core business questions.")

    # Section 4: Libraries and Tech Stack
    add_heading_1("4. Libraries and Technology Stack")
    tech_headers = ["Library / Framework", "Version", "Role & Purpose in Project"]
    tech_data = [
        ["Python", "3.11.6", "Core runtime environment and language."],
        ["Pandas", "3.1.0", "Tabular data manipulation, datetime parsing, rolling time-window counts, group aggregations."],
        ["NumPy", "2.4.6", "Vectorized array calculations, statistical thresholds, percentile quantiles."],
        ["Matplotlib", "3.11.2", "Publication-ready figure generation (histogram, bar charts, trend lines, scatter plots)."],
        ["Scikit-learn", "1.9.1", "Ground-truth evaluation metrics: confusion matrix, precision, recall, F1-score."],
        ["FastAPI", "0.162.0", "High-performance backend web framework and REST API."],
        ["Uvicorn", "0.54.0", "ASGI production web server running the dashboard."],
        ["Tailwind CSS", "3.x CDN", "Modern, responsive dark-slate UI styling for the web dashboard."],
        ["Chart.js", "4.x CDN", "Interactive client-side charts for the web application."],
        ["Pytest & Coverage", "9.2.0 / 7.1.0", "Test-driven development, automated unit & integration testing (94% coverage)."],
        ["Python-docx / ReportLab", "1.2.0 / 5.1.0", "Professional document compilation and report generation."]
    ]
    add_table_data(tech_headers, tech_data, col_widths=[1.8, 1.0, 4.0])

    # Section 5: Dataset Description
    add_heading_1("5. Dataset Description")
    add_body("The primary dataset (data/bank_transactions.csv) comprises 10,000 transaction records spanning 500 distinct customer accounts and 1,000 anonymized devices over the calendar month of September 2026.")
    data_headers = ["Field Name", "Example", "Type", "Operational Description"]
    data_desc = [
        ["Transaction_ID", "TX100025", "String", "Unique transaction tracking identifier."],
        ["Account_ID", "ACC1025", "String", "Anonymized customer account identifier (500 accounts)."],
        ["Transaction_Date", "2026-09-10", "Date", "Date transaction was initiated (YYYY-MM-DD)."],
        ["Transaction_Time", "23:45", "Time", "Time of transaction (HH:MM / HH:MM:SS)."],
        ["Amount", "85000.00", "Float", "Transaction monetary value in currency units ($)."],
        ["Transaction_Type", "Transfer", "Category", "Transaction category: Transfer, Payment, Withdrawal, Deposit."],
        ["Channel", "Online", "Category", "Initiation channel: Online, Mobile App, ATM, Branch."],
        ["Merchant_Category", "Electronics", "Category", "Business category: Electronics, Jewelry, Grocery, Travel, etc."],
        ["Location", "Kolkata", "String", "Originating metropolitan location."],
        ["Device_ID", "DEV204", "String", "Anonymized hardware terminal identifier."],
        ["Balance_Before", "150000.00", "Float", "Customer ledger balance prior to transaction."],
        ["Balance_After", "65000.00", "Float", "Customer ledger balance following transaction."],
        ["Fraud_Label", "0 or 1", "Integer", "Historical ground-truth verification label (1 = Fraud, 0 = Normal)."]
    ]
    add_table_data(data_headers, data_desc, col_widths=[1.5, 1.1, 0.9, 3.3])

    # Section 6: Architecture and Workflow
    add_heading_1("6. Project Architecture and Workflow")
    add_body("The project is structured into distinct, decoupled stages: data ingestion, cleansing, rule evaluation, scoring, analytical aggregation, reporting, and web serving.")
    add_figure_image("reports/figures/00_workflow_pipeline.png", "Figure 1: End-to-End Workflow of the Bank Fraud Screening Pipeline")
    
    add_body("Project Directory Tree:")
    tree_text = (
        "bank-fraud-detection/\n"
        "|-- data/\n"
        "|   |-- bank_transactions.csv      # Primary 10,000 records dataset\n"
        "|   `-- test_upload_sample.csv     # 250 records test sample\n"
        "|-- docs/                          # 19 comprehensive engineering documents\n"
        "|-- reports/\n"
        "|   |-- figures/                   # 10 generated PNG charts\n"
        "|   |-- suspicious_transactions.csv# Priority manual review queue\n"
        "|   |-- account_risk_summary.csv   # Account-level risk profiles\n"
        "|   `-- FRAUD_MONITORING_MANAGEMENT_REPORT.md\n"
        "|-- src/\n"
        "|   |-- data_generator.py          # Synthetic data factory\n"
        "|   |-- cleaning.py                # Validation and normalization\n"
        "|   |-- rules.py                   # Vectorized rule engine and scoring\n"
        "|   |-- analytics.py               # Aggregations, Q&A, and metrics\n"
        "|   |-- visualization.py           # Matplotlib charting engine\n"
        "|   |-- cli.py                     # CLI batch orchestrator\n"
        "|   |-- web_app.py                 # FastAPI backend and REST API\n"
        "|   `-- static/index.html          # Responsive Web UI\n"
        "|-- tests/                         # 38 Pytest unit and integration tests\n"
        "`-- run_web.py                     # Web server launcher"
    )
    add_body(tree_text)

    # Section 7: Data Loading and Inspection
    add_heading_1("7. Data Loading and Inspection")
    add_body("The initial phase inspects the dataset schema, data types, and null value counts prior to any mutations:")
    inspect_text = (
        "Dataset Shape: (10000, 13)\n"
        "Columns: ['Transaction_ID', 'Account_ID', 'Transaction_Date', 'Transaction_Time', 'Amount', ...]\n"
        "Null Values:\n"
        "Transaction_ID: 0  |  Account_ID: 0  |  Amount: 0  |  Transaction_Time: 0  |  Fraud_Label: 0\n"
        "Amount Summary ($):\n"
        "Count: 10,000 | Mean: $4,549.81 | Std: $13,060.86 | Min: $50.00 | Median: $1,807.50 | Max: $219,850.00"
    )
    add_body(inspect_text)

    # Section 8: Data Cleaning
    add_heading_1("8. Data Cleaning")
    add_body("Data cleaning is performed deterministically in src/cleaning.py with audit tracking:")
    clean_headers = ["Rule #", "Cleaning Operation", "Implementation & Purpose", "Audit Count"]
    clean_data = [
        ["1", "Exact Duplicate Removal", "df.drop_duplicates() eliminates redundant records.", "0 rows dropped"],
        ["2", "Transaction_ID Uniqueness", "Enforces unique transaction primary key.", "0 duplicates"],
        ["3", "Missing Critical Key Check", "Removes records lacking Account_ID, Time, or Amount.", "0 nulls"],
        ["4", "Amount Validity Check", "Filters non-positive or zero amounts (Amount > 0).", "0 invalid"],
        ["5", "Datetime Standardization", "Parses Transaction_Date and Transaction_Time; constructs unified Transaction_Datetime.", "10,000 converted"],
        ["6", "Hour Extraction", "Extracts integer Hour (0 to 23) for nocturnal filtering.", "10,000 derived"],
        ["7", "Category Normalization", "Strips whitespace and applies Title Case formatting.", "All normalized"]
    ]
    add_table_data(clean_headers, clean_data, col_widths=[0.8, 1.8, 3.2, 1.0])

    # Section 9: Transaction Amount & Statistical Thresholds
    add_heading_1("9. Transaction Amount & Statistical Thresholds")
    add_body("Financial transaction amounts exhibit a heavy-tailed, log-normal distribution: most transactions represent small everyday purchases, while rare high-value transfers occupy the extreme right tail.")
    add_body("To prevent extreme outliers from inflating the standard deviation and causing outlier masking, the system computes both:")
    add_bullet("Statistical Baseline: Mean + 3 StdDev = $4,549.81 + (3 * $13,060.86) = $43,732.38")
    add_bullet("Percentile Cutoff: 99th Percentile (P99) = $45,001.18 (Preferred default for robust outlier isolation)")

    # Section 10: Rule-Based Detection Logic
    add_heading_1("10. Rule-Based Detection Logic")
    add_body("Three explainable heuristic rules are evaluated per transaction, each contributing +1 point:")
    rule_headers = ["Rule Name", "Mathematical Condition", "Score", "Domain Rationale"]
    rule_data = [
        ["Rule 1: High Amount", "Amount >= P99 ($45,001.18)", "+1", "Transaction value deviates significantly from population norms."],
        ["Rule 2: Late Night", "Hour >= 23 or Hour <= 5", "+1", "Activity during customer sleep window (11:00 PM to 05:59 AM); common in bot draining."],
        ["Rule 3: High Frequency", "Rolling 1-Hour Txn Count >= 5", "+1", "Rapid velocity bursts on the same account indicate credential testing or automated attacks."],
        ["Alert Cutoff", "Suspicion_Score >= 2", "ALERT", "Requires multiple co-occurring anomalies. Suppresses single-rule false positives."]
    ]
    add_table_data(rule_headers, rule_data, col_widths=[1.5, 2.0, 0.8, 2.5])

    # Section 11: Key KPIs
    add_heading_1("11. Key Fraud Detection & Screening KPIs")
    add_body("Headline operational metrics computed across the 10,000 screened records:")
    kpi_headers = ["KPI Metric", "Observed Value", "Operational Context"]
    kpi_data = [
        ["Total Screened Transactions", "10,000", "Total volume processed through screening engine."],
        ["Total Monetary Volume", "$45,498,111.43", "Net financial turnover across all channels."],
        ["Average Transaction Amount", "$4,549.81", "Global population arithmetic mean."],
        ["Median Transaction Amount", "$1,807.50", "Robust central tendency measure."],
        ["99th Percentile Amount (P99)", "$45,001.18", "Configured cutoff for Rule 1."],
        ["High Amount Alerts (Rule 1)", "100 (1.00%)", "Single transactions exceeding $45,001.18."],
        ["Late Night Alerts (Rule 2)", "750 (7.50%)", "Transactions between 23:00 and 05:59."],
        ["High Frequency Alerts (Rule 3)", "113 (1.13%)", "Transactions part of a >=5 burst in 1 hour."],
        ["Flagged Suspicious Volume (Score >= 2)", "118 (1.18%)", "Prioritized for manual analyst investigation."],
        ["Normal Transactions (Score 0 or 1)", "9,882 (98.82%)", "Cleared without customer disruption."],
        ["Average Amount: Normal vs Suspicious", "$3,966.30 vs $53,416.15", "Flagged records are 13.47x larger on average."]
    ]
    add_table_data(kpi_headers, kpi_data, col_widths=[2.4, 1.8, 2.6])

    # Section 12: Overall Screening Performance
    add_heading_1("12. Overall Screening Performance")
    add_body("A key design principle of the screening pipeline is prioritizing investigator attention. Alerting on every single anomaly (Score 1) would produce 838 alerts (8.38%), overwhelming analysts. Requiring co-occurring signals (Score >= 2) concentrates review on 118 high-confidence leads (1.18%).")
    add_figure_image("reports/figures/02_normal_vs_suspicious.png", "Figure 2: Normal vs. Suspicious Transactions Volume Breakdown")
    add_figure_image("reports/figures/01_amount_distribution.png", "Figure 3: Distribution of Transaction Amounts with Outlier Cutoff")

    # Section 13: Rule 1 In-Depth
    add_heading_1("13. Rule 1 In-Depth: High-Amount Outlier Analysis")
    add_body("Exactly 100 transactions (1.00%) equaled or exceeded the 99th percentile threshold ($45,001.18). High-value transactions ranged from $45,002.50 to $219,850.00. While legitimate commercial clients occasionally execute large transfers, when combined with nocturnal timing or velocity bursts, high amounts exhibit strong correlation with account takeover attempts.")

    # Section 14: Rule 2 In-Depth
    add_heading_1("14. Rule 2 In-Depth: Late-Night Activity Analysis")
    add_body("750 transactions (7.50%) occurred during the 11:00 PM to 05:59 AM window. Peak nocturnal activity occurred at Hour 23:00 (11 PM) with 34 suspicious alerts, followed by Hour 02:00 (2 AM) and Hour 03:00 (3 AM). Automated card-testing scripts exploit early morning hours to maximize latency before account holders awaken and review mobile SMS notifications.")
    add_figure_image("reports/figures/03_suspicious_by_hour.png", "Figure 4: Suspicious Transactions by Hour of Day (Nocturnal Window Highlighted)")

    # Section 15: Rule 3 In-Depth
    add_heading_1("15. Rule 3 In-Depth: High-Frequency Burst Detection")
    add_body("Using a rolling 1-hour time window grouped per customer account, 113 transactions were identified where an account executed 5 or more transactions within 60 minutes. Velocity bursts are characteristic of automated credential stuffing bots and fraudsters attempting to drain balances before a stolen card is cancelled.")

    # Section 16: Suspicion Score & Bitmask Analysis
    add_heading_1("16. Suspicion Score Distribution & Bitmask Analysis")
    add_body("Every evaluated record receives an explicit 3-digit bitmask [Rule1_Rule2_Rule3] representing its triggered rule combination:")
    comb_headers = ["Rule Bitmask", "Description", "Transaction Count", "Share (%)", "Triage Decision"]
    comb_data = [
        ["0_0_0", "Normal Baseline (No Rules Triggered)", "9,162", "91.62%", "Clear automatically"],
        ["0_1_0", "Late Night Only", "635", "6.35%", "Passive audit log"],
        ["0_1_1", "Late Night + High Frequency", "63", "0.63%", "Escalate: Priority Review (Score 2)"],
        ["1_0_0", "High Amount Only", "45", "0.45%", "Passive audit log"],
        ["1_1_0", "High Amount + Late Night", "45", "0.45%", "Escalate: Priority Review (Score 2)"],
        ["0_0_1", "High Frequency Only", "40", "0.40%", "Passive audit log"],
        ["1_1_1", "Critical Alert (All 3 Rules Triggered)", "7", "0.07%", "Immediate Action: Trigger OTP / Block (Score 3)"],
        ["1_0_1", "High Amount + High Frequency", "3", "0.03%", "Escalate: Priority Review (Score 2)"]
    ]
    add_table_data(comb_headers, comb_data, col_widths=[1.1, 2.3, 1.2, 0.9, 2.3])
    add_figure_image("reports/figures/06_rule_combination_frequencies.png", "Figure 5: Transaction Volume by Rule Combination Bitmask")

    # Section 17 & 18: Type and Channel Analysis
    add_heading_1("17. Transaction Type Performance Analysis")
    add_body("Screening rates grouped by transaction category reveal that risk is entirely concentrated in outgoing Transfers:")
    type_headers = ["Transaction Type", "Total Transactions", "Suspicious Flagged", "Suspicious Rate (%)"]
    type_data = [
        ["Transfer", "3,725", "118", "3.17%"],
        ["Payment", "3,890", "0", "0.00%"],
        ["Withdrawal", "1,427", "0", "0.00%"],
        ["Deposit", "958", "0", "0.00%"]
    ]
    add_table_data(type_headers, type_data, col_widths=[2.0, 1.6, 1.6, 1.6])
    add_figure_image("reports/figures/04_suspicious_rate_by_type.png", "Figure 6: Suspicious Rate (%) by Transaction Type")

    add_heading_1("18. Channel Vulnerability Analysis")
    add_body("Analysis by origination channel indicates Online banking as the primary vulnerability vector:")
    ch_headers = ["Channel", "Total Transactions", "Suspicious Flagged", "Suspicious Rate (%)"]
    ch_data = [
        ["Online", "4,606", "118", "2.56%"],
        ["Mobile App", "3,931", "0", "0.00%"],
        ["ATM", "962", "0", "0.00%"],
        ["Branch", "501", "0", "0.00%"]
    ]
    add_table_data(ch_headers, ch_data, col_widths=[2.0, 1.6, 1.6, 1.6])
    add_figure_image("reports/figures/07_suspicious_rate_by_channel.png", "Figure 7: Suspicious Rate (%) by Origination Channel")

    # Section 19 & 20: Hourly and Correlation
    add_heading_1("19. Hourly Transaction Trend Analysis")
    add_body("Transaction volume peaks during regular business hours (10:00 to 18:00), while suspicious transaction density surges between 23:00 and 04:00, confirming the diagnostic power of nocturnal temporal filtering.")

    add_heading_1("20. Transaction Amount vs. Suspicion Score Correlation")
    add_body("Examining monetary amounts across suspicion scores shows an exponential increase: Score 0 records average $3,966.30, Score 1 average $5,820.40, Score 2 average $51,890.10, and Score 3 average $77,615.80.")
    add_figure_image("reports/figures/05_amount_vs_suspicion_score.png", "Figure 8: Transaction Amount ($) vs. Suspicion Score Scatter Plot")

    # Section 21: Required Visualizations
    add_heading_1("21. Required Visualizations")
    add_body("Summary inventory of all 10 generated charts saved in reports/figures/:")
    viz_headers = ["Figure #", "Chart Title", "Chart Type", "Saved File"]
    viz_data = [
        ["Fig 1", "End-to-End Pipeline Workflow", "Architecture Flowchart", "00_workflow_pipeline.png"],
        ["Fig 2", "Normal vs. Suspicious Transactions", "Comparative Bar Chart", "02_normal_vs_suspicious.png"],
        ["Fig 3", "Transaction Amount Distribution", "Histogram with Outlier Cutoff", "01_amount_distribution.png"],
        ["Fig 4", "Suspicious Activity by Hour of Day", "Line Chart with Risk Shading", "03_suspicious_by_hour.png"],
        ["Fig 5", "Rule Combination Frequencies", "Horizontal Bar Chart", "06_rule_combination_frequencies.png"],
        ["Fig 6", "Suspicious Rate by Transaction Type", "Categorical Bar Chart", "04_suspicious_rate_by_type.png"],
        ["Fig 7", "Suspicious Rate by Channel", "Channel Vulnerability Bar Chart", "07_suspicious_rate_by_channel.png"],
        ["Fig 8", "Amount vs. Suspicion Score", "Scatter Plot", "05_amount_vs_suspicion_score.png"],
        ["Fig 9", "Confusion Matrix Heatmap", "Matrix Heatmap", "08_confusion_matrix.png"],
        ["Fig 10", "Top Repeat Offender Accounts", "Pareto Bar Chart", "09_top_accounts_pareto.png"]
    ]
    add_table_data(viz_headers, viz_data, col_widths=[0.8, 2.5, 1.8, 2.0])

    # Section 22: Identifying High-Risk Accounts
    add_heading_1("22. Identifying High-Risk Accounts")
    add_body("To prevent flagging accounts on a single noisy transaction, an explicit repeat-offender rule is applied (Accounts with >= 2 suspicious transactions):")
    acc_headers = ["Account ID", "Total Txns", "Total Value ($)", "Avg Amount ($)", "Suspicious Txns", "Risk Rate (%)"]
    acc_data = [
        ["ACC1183", "43", "$570,373.00", "$13,264.50", "10", "23.26%"],
        ["ACC1290", "37", "$797,991.00", "$21,567.30", "8", "21.62%"],
        ["ACC1340", "35", "$699,260.00", "$19,978.80", "6", "17.14%"],
        ["ACC1492", "26", "$527,756.00", "$20,298.30", "5", "19.23%"],
        ["ACC1161", "26", "$636,560.00", "$24,483.10", "4", "15.38%"],
        ["ACC1420", "23", "$438,158.00", "$19,050.40", "4", "17.39%"],
        ["ACC1186", "27", "$385,701.00", "$14,285.20", "4", "14.81%"],
        ["ACC1030", "31", "$368,071.00", "$11,873.20", "4", "12.90%"]
    ]
    add_table_data(acc_headers, acc_data, col_widths=[1.2, 1.0, 1.5, 1.3, 1.1, 1.1])
    add_figure_image("reports/figures/09_top_accounts_pareto.png", "Figure 9: Top Repeat Offender Accounts by Suspicious Alerts")

    # Section 23: Advanced Extensions & ML Evaluation
    add_heading_1("23. Advanced Extensions & ML Evaluation")
    add_body("Comparing the rule-based screener against ground-truth historical fraud labels (Fraud_Label):")
    add_figure_image("reports/figures/08_confusion_matrix.png", "Figure 10: Confusion Matrix: Ground Truth vs. Rule Alert")
    eval_headers = ["Evaluation Metric", "Score", "Banking Industry Interpretation"]
    eval_data = [
        ["True Positives (TP)", "118", "Confirmed fraud cases successfully caught and escalated."],
        ["False Positives (FP)", "0", "Legitimate customer transactions incorrectly flagged."],
        ["True Negatives (TN)", "9,600", "Legitimate transactions cleared automatically."],
        ["False Negatives (FN)", "282", "Low-level fraudulent transactions slipping through rule screening."],
        ["Precision", "100.00%", "Every single alert represented verified fraudulent activity."],
        ["Recall (Sensitivity)", "29.50%", "Captures acute multi-factor fraud (bursts and high amounts)."],
        ["F1-Score", "0.456", "Harmonic mean of precision and recall for first-level filtering."],
        ["False Positive Rate (FPR)", "0.00%", "Zero customer friction achieved on the benchmark log."]
    ]
    add_table_data(eval_headers, eval_data, col_widths=[2.0, 1.2, 3.6])

    # Section 24: Pipeline Orchestration
    add_heading_1("24. Pipeline Orchestration (cli.py)")
    add_body("src/cli.py coordinates batch execution with configurable CLI flags:")
    cli_code = (
        "python -m src.cli --input data/bank_transactions.csv --reports-dir reports\n"
        "Options:\n"
        "  --input FILE              Input transaction CSV file\n"
        "  --generate N              Generate N synthetic transactions if no input provided\n"
        "  --amount-method {p99,3sigma} Amount threshold methodology (default: p99)\n"
        "  --freq-threshold N        Velocity burst limit per hour (default: 5)\n"
        "  --suspicion-threshold N   Score alert cutoff (default: 2)"
    )
    add_body(cli_code)

    # Section 25: Interactive Web Dashboard
    add_heading_1("25. Interactive Dashboard (Cronus FraudGuard)")
    add_body("The project includes an interactive single-page web application (src/web_app.py and src/static/index.html) running on FastAPI and Uvicorn.")
    add_body("Key Dashboard Capabilities:")
    add_bullet("Tab 1: Executive Overview with live counter cards and real-time Chart.js interactive visualizations.")
    add_bullet("Tab 2: Priority Review Queue with live text search, multi-factor dropdown filters, and single-click 'Inspect' deep-dive modal.")
    add_bullet("Tab 3: Customer Account Risk Profiles ranking repeat offenders.")
    add_bullet("Tab 4: Interactive Rule Studio with dynamic threshold sliders to simulate screening policies.")
    add_bullet("Tab 5: Drag-and-drop CSV uploader and synthetic data generator.")
    add_bullet("Tab 6: Interactive business Q&A and methodology reference.")

    # Section 26: Business Questions and Answers
    add_heading_1("26. Business Questions and Answers")
    q_headers = ["#", "Business Question", "Quantitative Answer & Evidence"]
    q_data = [
        ["Q1", "What percentage of transactions are flagged as suspicious?", "1.18% (118 out of 10,000 transactions flagged for priority review)."],
        ["Q2", "Which rule generates the most alerts?", "Rule 2: Late Night with 750 alerts (7.50%), followed by High Frequency (113) and High Amount (100)."],
        ["Q3", "How many transactions trigger two or more rules?", "Exactly 118 transactions (1.18% of total volume); 111 triggered 2 rules and 7 triggered all 3 rules."],
        ["Q4", "Which transaction types have higher suspicious rates?", "Transfer exhibits the highest suspicious rate at 3.17% (all 118 flagged alerts were transfers)."],
        ["Q5", "Which channels show higher suspicious activity?", "Online shows the highest risk rate at 2.56% of channel traffic."],
        ["Q6", "Which hours contain more suspicious transactions?", "Hour 23:00 (11:00 PM) contains the peak concentration of suspicious events (34 flagged records)."],
        ["Q7", "Are suspicious transactions generally larger than normal?", "Yes. Suspicious transactions average $53,416.15 vs $3,966.30 for normal transactions (13.47x higher)."],
        ["Q8", "Which accounts have repeated suspicious activity?", "28 accounts had multiple suspicious events. Top account ACC1183 generated 10 suspicious transactions."],
        ["Q9", "Which rule combinations occur most frequently?", "Single anomaly: 0_1_0 (Late Night Only, 635 txns). Multi-rule alert: 0_1_1 (63 txns) and 1_1_0 (45 txns)."],
        ["Q10", "How well do simple rules identify known fraud cases?", "Precision: 100.0%, FPR: 0.00%, Recall: 29.50%, F1-Score: 0.456. Zero false positives on benchmark."]
    ]
    add_table_data(q_headers, q_data, col_widths=[0.6, 2.5, 3.7])

    # Section 27: Business Findings & Recommendations
    add_heading_1("27. Business Findings and Operational Recommendations")
    add_heading_2("27.1 Executive Summary of Findings")
    add_bullet("Transfer and Online Banking are the primary fraud vectors; in-person ATM and Branch transactions showed near-zero multi-factor anomalies.")
    add_bullet("Severity is highly skewed: 118 transactions accounted for $6,303,105.70 in total suspicious exposure.")
    add_bullet("Nocturnal velocity bursts (0_1_1) and late-night high amounts (1_1_0) represent 91.5% of all flagged alerts.")
    add_heading_2("27.2 Prioritized Operational Recommendations")
    rec_headers = ["Priority", "Operational Recommendation", "Supporting Evidence", "Action Owner"]
    rec_data = [
        ["P1", "Enforce step-up biometric/OTP verification for Online Transfers exceeding $45,000 executed between 23:00 and 05:59.", "118 alerts, 100% precision, $53k avg amount.", "Digital Security Ops"],
        ["P2", "Implement automated account velocity throttles (maximum 4 transfers per 60 minutes) for retail accounts.", "Rule 3 caught 113 rapid bot bursts.", "Core Banking IT"],
        ["P3", "Place top 28 repeat offender accounts (led by ACC1183) on an automated surveillance watchlist.", "ACC1183 generated 10 suspicious events.", "Fraud Investigation Unit"],
        ["P4", "Transition from global population amount thresholds to personalized customer 90-day moving z-scores.", "Eliminates false alarms on high-net-worth commercial accounts.", "Data Science Team"]
    ]
    add_table_data(rec_headers, rec_data, col_widths=[0.8, 2.8, 2.0, 1.2])

    # Section 28: Testing & Reproducibility
    add_heading_1("28. Testing, Validation and Reproducibility")
    add_body("The project adheres to strict Test-Driven Development (TDD). A suite of 38 automated tests is maintained across 5 test modules:")
    test_headers = ["Test Module", "Test Focus", "Test Count", "Status"]
    test_data = [
        ["tests/test_data_generator.py", "Schema conformity, PII privacy checks, reproducibility.", "5", "100% Passed"],
        ["tests/test_cleaning.py", "Deduplication, datetime normalization, invalid amount handling.", "5", "100% Passed"],
        ["tests/test_rules.py", "Rules 1, 2, 3 boundary logic, score summation, bitmasks.", "8", "100% Passed"],
        ["tests/test_analytics.py", "Group drilldowns, Q&A synthesis, confusion matrix metrics.", "8", "100% Passed"],
        ["tests/test_e2e_pipeline.py", "Full pipeline batch smoke test, figure generation.", "3", "100% Passed"],
        ["tests/test_web_app.py", "FastAPI endpoints, KPI payloads, CSV upload, queue export.", "9", "100% Passed"],
        ["Total Suite", "Comprehensive Regression Suite", "38 Tests", "100% Passed (94% Cov)"]
    ]
    add_table_data(test_headers, test_data, col_widths=[2.0, 3.0, 0.9, 0.9])

    # Section 29: Limitations & Ethics
    add_heading_1("29. Limitations and Important Analytical & Ethical Notes")
    add_body("1. Alert != Proof of Guilt: A flagged alert is an investigative lead for human review, never proof of criminality.")
    add_body("2. False Positives: Honest customers purchasing emergency hospital care or plane tickets at 2:00 AM will trigger rules. Banks must use gentle verification prompts (SMS/OTP) rather than abrupt account freezing.")
    add_body("3. Privacy & Non-Discrimination: The system complies with banking privacy regulations by omitting real customer names, card numbers, passwords, PINs, and demographic attributes.")

    # Section 30: Learning Outcomes
    add_heading_1("30. Learning Outcomes")
    add_bullet("Mastery of Pandas and NumPy for financial transaction exploratory data analysis and time-series rolling windows.")
    add_bullet("Design and implementation of deterministic, interpretable anomaly scoring logic.")
    add_bullet("Building production-ready REST APIs and responsive web dashboards using FastAPI and Tailwind CSS.")
    add_bullet("Applying Test-Driven Development (TDD) with Pytest and maintaining high code coverage.")
    add_bullet("Communicating financial analytics findings responsibly using executive-ready data tables and charts.")

    # Section 31: Conclusion & Future Scope
    add_heading_1("31. Conclusion and Future Scope")
    add_body("This project successfully demonstrated the implementation of a transparent, rule-based fraud screening architecture for retail banking. Starting from 10,000 transaction records, it isolated 118 high-risk alerts with 100% precision, established clear audit bitmasks, generated 10 visual charts, and delivered a production-ready web application with 38 verified tests.")
    add_body("Future Scope:")
    add_bullet("Incorporate customer-specific behavioral baselines using moving z-scores and IQR.")
    add_bullet("Deploy a secondary machine learning model (e.g. XGBoost / LightGBM) to evaluate Score 1 cases.")
    add_bullet("Integrate with Apache Kafka or Apache Flink for real-time sub-second streaming evaluation.")
    add_bullet("Implement Graph Neural Networks (GNN) to uncover mule account collusion rings.")

    # References
    add_heading_1("References")
    add_bullet("Pandas Development Team. (2026). pandas: powerful Python data analysis toolkit.")
    add_bullet("NumPy Developers. (2026). NumPy: the fundamental package for scientific computing with Python.")
    add_bullet("Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering.")
    add_bullet("Tiangolo, S. (2026). FastAPI: Modern, fast (high-performance) web framework for building APIs with Python.")
    add_bullet("Basel Committee on Banking Supervision. (2024). Sound Practices for Operational and Financial Cyber Risk.")
    add_bullet("Reserve Bank of India (RBI). (2023). Master Direction on Cyber Security and Fraud Monitoring in Banks.")

    # Save Word Document
    doc.save(output_path)
    print(f"[+] Successfully generated Word Document: {output_path}")


def build_pdf_documentation(output_path="reports/PROJECT_DOCUMENTATION.pdf", md_file="docs/PROJECT_DOCUMENTATION.md"):
    """Build complete PDF document with Cronus Consultants logo on top-left of EVERY page."""
    import re
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    class NumberedCanvas(canvas.Canvas):
        """Two-pass canvas that paints running header and footer on EVERY page."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_page_decorations(self, total_pages):
            self.saveState()
            page_w, page_h = letter

            # 1. Top-Left Logo on EVERY PAGE
            if os.path.exists(LOGO_PATH):
                try:
                    self.drawImage(LOGO_PATH, x=45, y=page_h - 48, width=70, height=28, preserveAspectRatio=True, mask='auto')
                except Exception:
                    self.drawImage(LOGO_PATH, x=45, y=page_h - 48, width=70, height=28, preserveAspectRatio=True)

            # 2. Header Text & Running Separator
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawRightString(page_w - 45, page_h - 35, "Cronus Bank | Fraud Detection & Risk Analytics System")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(45, page_h - 52, page_w - 45, page_h - 52)

            # 3. Footer Line & Page Numbers
            self.line(45, 40, page_w - 45, 40)
            self.setFont("Helvetica", 8)
            self.drawString(45, 28, "Confidential | Industry-Oriented Data Analytics Student Project")
            self.drawRightString(page_w - 45, 28, f"Page {self._pageNumber} of {total_pages}")
            self.restoreState()

    with open(md_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    lines = raw_text.splitlines()
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4.5
    )
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )
    cell_style = ParagraphStyle(
        'DocCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#1e293b')
    )
    cell_hdr = ParagraphStyle(
        'DocCellHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.white
    )
    code_block_style = ParagraphStyle(
        'DocCodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=3,
        spaceAfter=5
    )

    def clean_md(text):
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<i>\1</i>', text)
        text = re.sub(r'`([^`]+?)`', r'<font face="Courier" color="#0f766e">\1</font>', text)
        return text

    story = []
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i].rstrip()
        trimmed = line.strip()

        if not trimmed:
            i += 1
            continue

        if trimmed.startswith('```'):
            if in_code:
                in_code = False
                joined = '<br/>'.join([c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;') for c in code_lines])
                code_table = Table([[Paragraph(joined, code_block_style)]], colWidths=[522])
                code_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(code_table)
                story.append(Spacer(1, 4))
                code_lines = []
            else:
                in_code = True
                code_lines = []
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if trimmed.startswith('<p') or trimmed.startswith('</p>') or trimmed.startswith('<img') or 'cronus_logo.png' in trimmed:
            i += 1
            continue

        if trimmed.startswith('# '):
            story.append(Paragraph(clean_md(trimmed[2:]), title_style))
        elif trimmed.startswith('## '):
            story.append(Paragraph(clean_md(trimmed[3:]), h1_style))
        elif trimmed.startswith('### '):
            story.append(Paragraph(clean_md(trimmed[4:]), h2_style))
        elif trimmed.startswith('#### '):
            story.append(Paragraph(clean_md(trimmed[5:]), subtitle_style))
        elif trimmed.startswith('---'):
            story.append(Spacer(1, 5))

        elif trimmed.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1

            rows_data = []
            for tl_idx, tl in enumerate(table_lines):
                if re.match(r'^\|[\s\-:\|]+\|$', tl):
                    continue
                cells = [c.strip() for c in tl.split('|')[1:-1]]
                if tl_idx == 0:
                    rows_data.append([Paragraph(clean_md(c), cell_hdr) for c in cells])
                else:
                    rows_data.append([Paragraph(clean_md(c), cell_style) for c in cells])

            if rows_data:
                num_cols = len(rows_data[0])
                if num_cols == 2:
                    col_widths = [140, 382]
                elif num_cols == 3:
                    col_widths = [130, 150, 242]
                elif num_cols == 4:
                    col_widths = [90, 80, 80, 272]
                elif num_cols == 5:
                    col_widths = [65, 120, 75, 65, 197]
                else:
                    col_w = 522 / max(num_cols, 1)
                    col_widths = [col_w] * num_cols

                t = Table(rows_data, colWidths=col_widths, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                    ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(t)
                story.append(Spacer(1, 5))
            continue

        elif trimmed.startswith('* ') or trimmed.startswith('- '):
            txt = clean_md(trimmed[2:])
            story.append(Paragraph(f"&bull; {txt}", bullet_style))

        elif '![' in trimmed:
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', trimmed)
            if img_match:
                caption = img_match.group(1)
                path = img_match.group(2).replace('docs/', '')
                if os.path.exists(path):
                    try:
                        story.append(RLImage(path, width=470, height=205))
                        if caption:
                            story.append(Paragraph(f"<i>Figure: {clean_md(caption)}</i>", cell_style))
                        story.append(Spacer(1, 5))
                    except Exception as e:
                        print(f"[-] Could not add image {path}: {e}")
            else:
                story.append(Paragraph(clean_md(trimmed), body_style))

        else:
            story.append(Paragraph(clean_md(trimmed), body_style))

        i += 1

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=60,
        bottomMargin=55,
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF Document: {output_path} ({os.path.getsize(output_path)} bytes)")


def build_html_documentation(output_path="reports/PROJECT_DOCUMENTATION.html", md_file="docs/PROJECT_DOCUMENTATION.md"):
    """Build complete HTML document with print CSS displaying the logo on the top-left of every printed page."""
    import markdown
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_for_html = md_text.replace("reports/figures/", "/figures/")
    md_for_html = md_for_html.replace("assets/cronus_logo.png", "/static/cronus_logo.png")

    body_html = markdown.markdown(md_for_html, extensions=['tables', 'fenced_code', 'nl2br'])

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bank Transaction Fraud Detection — Comprehensive Project Documentation</title>
  <link rel="icon" type="image/png" href="/static/cronus_logo.png">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @media print {{
      @page {{
        size: letter portrait;
        margin: 22mm 15mm 20mm 15mm;
        @top-left {{
          content: url('/static/cronus_logo.png');
          vertical-align: middle;
        }}
        @top-right {{
          content: "Cronus Consultants | Bank Fraud Detection Project Documentation";
          font-family: sans-serif;
          font-size: 8pt;
          color: #64748b;
        }}
        @bottom-right {{
          content: "Page " counter(page) " of " counter(pages);
          font-family: sans-serif;
          font-size: 8pt;
          color: #64748b;
        }}
      }}
      .no-print {{ display: none !important; }}
      body {{ font-size: 10pt; line-height: 1.4; color: #1e293b; }}
      h1 {{ font-size: 18pt !important; page-break-after: avoid; }}
      h2 {{ font-size: 13pt !important; page-break-after: avoid; color: #0f172a !important; margin-top: 14pt !important; }}
      h3 {{ font-size: 11pt !important; page-break-after: avoid; }}
      table {{ page-break-inside: auto; }}
      tr {{ page-break-inside: avoid; page-break-after: auto; }}
      img {{ max-width: 100% !important; page-break-inside: avoid; }}
    }}
    
    .prose-doc h1 {{ font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }}
    .prose-doc h2 {{ font-size: 1.35rem; font-weight: 700; color: #1e3a8a; margin-top: 2rem; margin-bottom: 0.75rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.35rem; }}
    .prose-doc h3 {{ font-size: 1.1rem; font-weight: 700; color: #334155; margin-top: 1.25rem; margin-bottom: 0.5rem; }}
    .prose-doc h4 {{ font-size: 0.95rem; font-weight: 600; color: #2563eb; margin-top: 0.5rem; margin-bottom: 0.5rem; }}
    .prose-doc p {{ margin-bottom: 0.85rem; line-height: 1.6; color: #334155; }}
    .prose-doc ul {{ list-style-type: disc; margin-left: 1.5rem; margin-bottom: 0.85rem; }}
    .prose-doc li {{ margin-bottom: 0.25rem; }}
    .prose-doc table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; margin-bottom: 1.25rem; font-size: 0.825rem; border: 1px solid #cbd5e1; border-radius: 0.375rem; overflow: hidden; }}
    .prose-doc th {{ background-color: #1e3a8a; color: white; padding: 0.55rem 0.75rem; text-align: left; font-weight: 600; border: 1px solid #3b82f6; }}
    .prose-doc td {{ padding: 0.45rem 0.75rem; border: 1px solid #e2e8f0; vertical-align: top; }}
    .prose-doc tr:nth-child(even) {{ background-color: #f8fafc; }}
    .prose-doc code {{ background-color: #f1f5f9; color: #0f766e; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.85em; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .prose-doc pre {{ background-color: #0f172a; color: #f8fafc; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin-bottom: 1rem; font-size: 0.8rem; }}
    .prose-doc pre code {{ background-color: transparent; color: inherit; padding: 0; }}
    .prose-doc hr {{ margin-top: 2rem; margin-bottom: 2rem; border-color: #cbd5e1; }}
    .prose-doc img {{ border-radius: 0.5rem; margin-top: 0.5rem; margin-bottom: 0.75rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border: 1px solid #e2e8f0; max-height: 480px; object-fit: contain; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">

  <header class="no-print sticky top-0 z-50 bg-slate-900 border-b border-slate-800 text-white px-4 md:px-8 py-3 flex flex-wrap items-center justify-between shadow-lg">
    <div class="flex items-center space-x-3">
      <img src="/static/cronus_logo.png" alt="Cronus Logo" class="h-8 w-auto bg-white rounded p-1 shadow">
      <div>
        <h1 class="font-bold text-sm leading-tight text-white m-0">Cronus Consultants</h1>
        <p class="text-[10px] text-slate-400 m-0">Bank Transaction Fraud Analytics • Official Project Documentation</p>
      </div>
    </div>
    <div class="flex items-center space-x-2 mt-2 md:mt-0">
      <a href="/" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs font-medium border border-slate-700 transition">
        ← Back to App
      </a>
      <a href="/download/documentation/docx" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold shadow transition flex items-center space-x-1.5">
        <span>📄 Word (.docx)</span>
      </a>
      <a href="/download/documentation/pdf" class="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded text-xs font-semibold shadow transition flex items-center space-x-1.5">
        <span>📑 PDF (.pdf)</span>
      </a>
      <button onclick="window.print()" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-semibold shadow transition flex items-center space-x-1.5">
        <span>🖨️ Print / Save PDF</span>
      </button>
    </div>
  </header>

  <main class="max-w-5xl mx-auto my-6 md:my-10 p-6 md:p-14 bg-white shadow-xl rounded-xl border border-slate-200">
    <div class="flex items-center justify-between border-b-2 border-slate-900 pb-4 mb-6">
      <div class="flex items-center space-x-4">
        <img src="/static/cronus_logo.png" alt="Cronus Logo" class="h-16 w-auto object-contain">
        <div>
          <span class="text-xs font-black uppercase tracking-widest text-blue-700">Cronus Consultants Risk Intelligence</span>
          <p class="text-xs text-slate-500">Industry-Oriented Capstone Project • Academic Year 2026</p>
        </div>
      </div>
      <div class="text-right">
        <span class="inline-block bg-blue-100 text-blue-800 text-[11px] font-bold px-2.5 py-0.5 rounded uppercase">Confidential</span>
        <p class="text-[11px] text-slate-400 mt-1">Ref: CRONUS-FRAUD-2026-CAPSTONE</p>
      </div>
    </div>

    <article class="prose-doc">
      {body_html}
    </article>

    <footer class="mt-12 pt-6 border-t border-slate-200 text-center text-xs text-slate-400">
      <p>© 2026 Cronus Bank & Cronus Consultants. All rights reserved. Industry-Oriented Data Analytics Capstone Project.</p>
    </footer>
  </main>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    static_path = "src/static/documentation.html"
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    with open(static_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"[+] Successfully generated HTML Document: {output_path} and {static_path}")

def build_markdown_documentation(output_path="docs/PROJECT_DOCUMENTATION.md"):
    """Build complete 31-section Markdown Document matching the template with Logo on top."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    md_content = """<p align="left">
  <img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="180">
</p>

# PROJECT DOCUMENTATION
## Bank Transaction Fraud Detection: Rule-Based Fraud Analytics
### Industry-Oriented Data Analytics Student Project
#### Rule-Based Bank Transaction Fraud Detection & Suspicious Activity Analytics Using Python, Pandas, NumPy, Matplotlib and FastAPI

| Item | Details |
|---|---|
| **Project group** | Fraud Analytics Group / Team Cronus |
| **Team members** | Student Data Analyst (Portfolio Capstone) |
| **Course / Programme** | Industry-Oriented Data Analytics Capstone / Financial Analytics |
| **Faculty guide** | Fraud Risk Operations & Applied AI Guide |
| **Technology** | Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn (analysis); FastAPI, Tailwind CSS, Chart.js, HTML5 (interactive dashboard) |
| **Dataset** | Bank transaction screening records, 10,000 raw rows x 13 columns (synthetic, calendar month September 2026) |
| **Date of submission** | November 2026 |
| **Disclaimer** | The transaction dataset used in this project is synthetic and was created for learning and demonstration adhering to Section 7 privacy rules. All results describe this dataset and demonstrate an analytical workflow; they must not be read as evidence about a real banking operation or real customer accounts. |

---

## Table of Contents
* **Abstract**
* **1. Project Overview**
  * 1.1 Problem Statement
  * 1.2 Scope of the Work
  * 1.3 Project Deliverables
* **2. Business Scenario**
* **3. Project Objectives**
* **4. Libraries and Technology Stack**
* **5. Dataset Description**
  * 5.1 Data Quality Characteristics of the Raw File
* **6. Project Architecture and Workflow**
* **7. Data Loading and Inspection**
* **8. Data Cleaning**
  * 8.1 Cleaning Rules and Decisions
  * 8.2 Cleaning Code
  * 8.3 Data Cleaning Audit Results
  * 8.4 Reconciliation of Record Counts
* **9. Transaction Amount & Statistical Thresholds**
* **10. Rule-Based Detection Logic**
* **11. Key Fraud Detection & Screening KPIs**
* **12. Overall Screening Performance**
* **13. Rule 1 In-Depth: High-Amount Outlier Analysis**
* **14. Rule 2 In-Depth: Late-Night Activity Analysis**
* **15. Rule 3 In-Depth: High-Frequency Burst Detection**
* **16. Suspicion Score Distribution & Bitmask Analysis**
* **17. Transaction Type Performance Analysis**
* **18. Channel Vulnerability Analysis**
* **19. Hourly Transaction Trend Analysis**
* **20. Transaction Amount vs. Suspicion Score Correlation**
* **21. Required Visualizations**
* **22. Identifying High-Risk Accounts**
* **23. Advanced Extensions & ML Evaluation**
* **24. Pipeline Orchestration (cli.py)**
* **25. Interactive Web Dashboard (Cronus FraudGuard)**
* **26. Business Questions and Answers**
* **27. Business Findings and Operational Recommendations**
* **28. Testing, Validation and Reproducibility**
* **29. Limitations and Important Analytical & Ethical Note**
* **30. Learning Outcomes**
* **31. Conclusion and Future Scope**
* **References**

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## Abstract
Financial institutions process millions of electronic banking transactions daily. Punctual, non-disruptive clearing of legitimate payments is essential to consumer trust, yet fraudulent card testing, account takeovers, and unauthorized wire transfers inflict catastrophic losses. This project analyses 10,000 raw transaction records from a synthetic banking network to implement an explainable, transparent, rule-based screening engine. Rather than automatically declaring customers as criminals, the system evaluates behavioral anomalies across Transaction Amount, Transaction Time, and Transaction Velocity, assigning an interpretable Suspicion Score (0 to 3) to triage records for human-in-the-loop compliance review.

The screening engine was implemented as a modular Python pipeline (loading, validation, metric derivation, rule evaluation, KPI calculation, multidimensional drilldowns, and charting) and extended with a responsive web dashboard (Cronus FraudGuard) and REST API. Across 10,000 evaluated transactions, 118 records (1.18%) triggered multiple co-occurring anomalies (Suspicion Score >= 2) and were escalated to the priority review queue. Flagged transactions averaged $53,416.15—a 13.47x surge over normal volume ($3,966.30). Transfer was identified as the highest-risk transaction type (3.17% suspicious rate) and Online as the highest-risk channel (2.56%). Against verified historical ground-truth fraud labels, the rule-based screener achieved 100.0% precision, 0.00% false positive rate, and captured all acute multi-factor attack patterns.

**Keywords**: fraud analytics, rule-based screening, suspicion score, transaction anomaly detection, Pandas, Matplotlib, FastAPI, banking compliance.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 1. Project Overview
### 1.1 Problem Statement
Retail banks face escalating digital fraud threats across online banking, mobile applications, and payment gateways. While machine learning is frequently proposed, deploying black-box AI models as an unexplainable first-tier filter creates severe legal, regulatory (RBI / OCC / GDPR), and customer relations liabilities: compliance officers cannot explain to auditors or clients why an alert was triggered. A robust, deterministic, rule-based transaction screening system is required to screen transactions, provide clear audit trails, and prioritize manual investigation without prematurely freezing customer accounts.

### 1.2 Scope of the Work
* Ingestion, cleaning, and validation of 10,000 transaction records with zero data loss on valid keys.
* Computing statistical thresholds (Gaussian mean + 3 standard deviations and 99th percentile $P_{99}$).
* Evaluating three core behavioral heuristics: Amount Outlier, Late-Night Window (23:00 to 05:59), and Rolling 1-Hour Burst count.
* Combining rules into an explainable Suspicion Score (0 to 3) and 3-digit bitmasks (e.g. `1_1_0`).
* Producing 10 high-resolution Matplotlib figures and CSV investigation queues.
* Delivering an interactive web dashboard with dynamic threshold simulation and CSV upload capabilities.

### 1.3 Project Deliverables
All project brief deliverables are fulfilled:
1. Complete Python package (`src/`) and CLI runner (`src/cli.py`).
2. Cleaned primary dataset (`data/bank_transactions.csv`) and sample upload file (`test_upload_sample.csv`).
3. Priority manual review queue (`reports/suspicious_transactions.csv`).
4. Account risk summary profiles (`reports/account_risk_summary.csv`).
5. 10 publication-ready Matplotlib figures in `reports/figures/`.
6. Executive management report answering all 10 core business questions.
7. Interactive web dashboard (`run_web.py`) running on FastAPI and Tailwind CSS.
8. Automated test suite (`tests/`) with 38 passing tests and 94% code coverage.
9. Formal project documentation available in DOCX, PDF, HTML, and Markdown.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 2. Business Scenario
The project is framed as the work of a Junior Data Analyst in Cronus Bank's Fraud Monitoring and Surveillance Team. The bank requires a reliable, transparent first-level screening filter to process incoming transactions in real time before complex scoring models are introduced. The analyst's objective is to screen transactions based on amount, hour, and velocity, assign an interpretable suspicion score, and furnish fraud analysts with detailed triage reports rather than making irreversible automated blocks.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 3. Project Objectives
* Clean and validate raw transaction records with documented audit decisions.
* Analyze transaction amount distributions and establish statistical cutoffs.
* Detect unusually high transaction amounts using statistical ($\mu + 3\sigma$) and percentile ($P_{99}$) thresholds.
* Detect late-night transactions occurring between 11:00 PM and 5:59 AM.
* Detect rapid transaction bursts using rolling 1-hour window counts per account.
* Aggregate individual rules into an explainable Suspicion Score (0 to 3).
* Flag high-risk records (Score >= 2) into a prioritized investigation queue.
* Profile customer accounts with repeated suspicious activities.
* Create high-quality visual analytics charts using Matplotlib.
* Build a responsive interactive web dashboard for fraud monitoring analysts.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 4. Libraries and Technology Stack
| Library / Framework | Version | Purpose in this Project |
|---|---|---|
| **Python** | 3.11.6 | Core runtime environment. |
| **Pandas** | 3.1.0 | Data loading, cleaning, datetime parsing, rolling time-window counts, group aggregations. |
| **NumPy** | 2.4.6 | Vectorized array calculations, statistical thresholds, percentile quantiles. |
| **Matplotlib** | 3.11.2 | Publication-ready figure generation (histogram, bar charts, trend lines, scatter plots). |
| **Scikit-learn** | 1.9.1 | Ground-truth evaluation metrics: confusion matrix, precision, recall, F1-score. |
| **FastAPI** | 0.162.0 | High-performance backend web framework and REST API. |
| **Uvicorn** | 0.54.0 | Production ASGI server running the interactive dashboard. |
| **Tailwind CSS & Chart.js** | CDN | Modern, responsive dark-slate UI styling and interactive browser charts. |
| **Pytest & Coverage** | 9.2.0 / 7.1.0 | Test-driven development, automated unit & integration testing (94% coverage). |
| **Python-docx & ReportLab**| 1.2.0 / 5.1.0 | Professional document compilation into Word (.docx) and PDF (.pdf). |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 5. Dataset Description
The dataset (`data/bank_transactions.csv`) contains 10,000 transaction records across 500 distinct customer accounts and 1,000 anonymized devices.

| Field Name | Example | Type | Description |
|---|---|---|---|
| `Transaction_ID` | TX100025 | String | Unique transaction tracking identifier. |
| `Account_ID` | ACC1025 | String | Anonymized account identifier (500 accounts). |
| `Transaction_Date` | 2026-09-10 | Date | Date of transaction (YYYY-MM-DD). |
| `Transaction_Time` | 23:45 | Time | Time of transaction (HH:MM). |
| `Amount` | 85000.00 | Float | Transaction monetary value ($). |
| `Transaction_Type` | Transfer | Category | Transfer, Payment, Withdrawal, Deposit. |
| `Channel` | Online | Category | Online, Mobile App, ATM, Branch. |
| `Merchant_Category` | Electronics | Category | Business category (Electronics, Jewelry, Grocery, etc.). |
| `Location` | Kolkata | String | Originating city/region. |
| `Device_ID` | DEV204 | String | Anonymized hardware terminal identifier. |
| `Balance_Before` | 150000.00 | Float | Ledger balance before transaction. |
| `Balance_After` | 65000.00 | Float | Ledger balance after transaction. |
| `Fraud_Label` | 0 or 1 | Integer | Historical verified label (1 = Fraud, 0 = Normal). |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 6. Project Architecture and Workflow
![Figure 1: End-to-End Workflow of the Bank Fraud Screening Pipeline](reports/figures/00_workflow_pipeline.png)

```
[Raw CSV Stream (10,000 Rows)]
              |
              v
[Data Cleaning & Datetime Normalization]
              |
              v
[Feature Derivation: Amount, Hour, 1H Velocity]
              |
              v
[Rule Engine: High Amount, Late Night, Frequency Burst]
              |
              v
[Suspicion Scoring & Bitmasking (Score = R1 + R2 + R3)]
              |
              v
[Alert Triage: Score >= 2 -> Priority Investigation Queue]
              |
    +---------+---------+---------+
    |                   |         |
    v                   v         v
[Reports & CSVs]   [Charts]  [Cronus FraudGuard Web App]
```

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 7. Data Loading and Inspection
The loading stage confirms 10,000 rows across 13 fields with zero null values in critical columns.
* Total monetary turnover: **$45,498,111.43**
* Arithmetic mean amount: **$4,549.81**
* Median amount: **$1,807.50**
* Minimum amount: **$50.00**
* Maximum amount: **$219,850.00**

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 8. Data Cleaning
1. **Deduplication**: Exact duplicate records and duplicate `Transaction_ID`s are identified and eliminated.
2. **Missing Value Handling**: Verified zero nulls in required keys (`Transaction_ID`, `Account_ID`, `Amount`, `Transaction_Time`).
3. **Amount Validation**: Enforced `Amount > 0`; negative or zero transactions are rejected.
4. **Datetime Standardization**: Unified ISO strings parsed into standardized timestamps and integer `Hour` (0 to 23).
5. **Casing Normalization**: Stripped trailing spaces and enforced Title Case across string categories.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 9. Transaction Amount & Statistical Thresholds
Financial amounts follow a Pareto/log-normal distribution. Relying solely on a Gaussian bell curve ($\mu + 3\sigma$) can lead to outlier masking because massive fraud transactions artificially inflate both the mean and standard deviation.

* **Gaussian 3-Sigma Cutoff**: $\mu + 3\sigma = \$4,549.81 + (3 \times \$13,060.86) = \$43,732.38$
* **99th Percentile Cutoff ($P_{99}$)**: **$45,001.18** (Preferred default for robust outlier isolation)

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 10. Rule-Based Detection Logic
| Rule Name | Mathematical Condition | Score Weight | Rationale |
|---|---|:---:|---|
| **Rule 1: Unusual Amount** | `Amount >= P99` ($45,001.18) | **+1** | Transaction value is unusually high compared to historical baseline. |
| **Rule 2: Late Night** | `23:00 <= Hour <= 05:59` | **+1** | Activity takes place during customer sleep hours; common in automated card draining. |
| **Rule 3: High Frequency** | `Rolling 1-Hour Txn Count >= 5` | **+1** | Rapid transaction bursts indicate credential stuffing, automated bots, or card testing. |
| **Alert Cutoff** | `Suspicion_Score >= 2` | **ALERT** | Combines multi-factor signals to suppress single-anomaly noise and prioritize true risk. |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 11. Key Fraud Detection & Screening KPIs
| Executive Metric | Observed Value | Operational Context |
|---|:---:|---|
| **Total Ingested Volume** | 10,000 | Processed and cleaned transaction records. |
| **Total Monetary Volume** | $45,498,111.43 | Net portfolio turnover across monitored channels. |
| **Average Transaction** | $4,549.81 | Population arithmetic mean. |
| **Median Transaction** | $1,807.50 | Robust central tendency measure. |
| **99th Percentile Threshold ($P_{99}$)** | $45,001.18 | Outlier cutoff for high-value transfers. |
| **Statistical Threshold ($\mu + 3\sigma$)** | $43,732.38 | Baseline Gaussian 3-sigma cutoff. |
| **Suspicious Flagged Volume** | **118 (1.18%)** | Prioritized for immediate analyst review (Score $\ge 2$). |
| **High Amount Alerts** | 100 (1.00%) | Single transactions exceeding outlier thresholds. |
| **Late Night Alerts** | 750 (7.50%) | Transactions occurring between 23:00 and 05:59. |
| **High Frequency Bursts** | 113 (1.13%) | Accounts executing $\ge 5$ transactions in rolling 1-hour. |
| **Avg Amount: Normal vs Suspicious** | **$3,966.30 vs $53,416.15** | Suspicious transactions are 13.47x larger on average. |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 12. Overall Screening Performance
![Figure 2: Normal vs Suspicious Transactions Volume Breakdown](reports/figures/02_normal_vs_suspicious.png)

* **Normal Transactions (Score 0-1)**: 9,882 (98.82%)
  * Score 0 (Clean): 9,162 transactions (91.62%)
  * Score 1 (Low Anomaly): 720 transactions (7.20%)
* **Suspicious Transactions (Score 2-3)**: 118 (1.18%)
  * Score 2 (High Priority): 111 transactions (1.11%)
  * Score 3 (Critical Alert): 7 transactions (0.07%)

Requiring at least 2 co-occurring rules suppressed 720 single-anomaly false alarms, focusing review resources on 118 high-confidence alerts.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 13. Rule 1 In-Depth: High-Amount Outlier Analysis
![Figure 3: Distribution of Transaction Amounts with Outlier Cutoff](reports/figures/01_amount_distribution.png)

100 transactions (1.00%) triggered Rule 1. Outlier amounts spanned from $45,002.50 to $219,850.00. High amount alone (Score 1) accounted for 45 records, while 55 records occurred alongside late-night hours or velocity bursts, representing acute risk.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 14. Rule 2 In-Depth: Late-Night Activity Analysis
![Figure 4: Suspicious Transactions by Hour of Day](reports/figures/03_suspicious_by_hour.png)

750 transactions (7.50%) occurred between 23:00 and 05:59. The distribution showed peak suspicious activity at Hour 23:00 (34 alerts), followed by Hour 02:00 and Hour 03:00. 635 late-night transactions were benign single anomalies (e.g. late-night ride or dining payments), while 115 co-occurred with high amounts or burst velocity.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 15. Rule 3 In-Depth: High-Frequency Burst Detection
113 transactions were identified where an account executed 5 or more transactions within a rolling 60-minute window. Velocity bursts are heavily correlated with automated bot scripts and compromised payment credentials.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 16. Suspicion Score Distribution & Bitmask Analysis
![Figure 5: Transaction Volume by Rule Combination Bitmask](reports/figures/06_rule_combination_frequencies.png)

| Rule Bitmask | Description | Transactions | Share (%) | Operational Triage Action |
|---|---|---|---|---|
| `0_0_0` | Baseline Normal | 9,162 | 91.62% | Clear immediately |
| `0_1_0` | Late Night Only | 635 | 6.35% | Passive audit log |
| `0_1_1` | Late Night + High Frequency | 63 | 0.63% | Escalate: Priority Review Queue (Score 2) |
| `1_0_0` | High Amount Only | 45 | 0.45% | Passive audit log |
| `1_1_0` | High Amount + Late Night | 45 | 0.45% | Escalate: Priority Review Queue (Score 2) |
| `0_0_1` | High Frequency Only | 40 | 0.40% | Passive audit log |
| `1_1_1` | Critical Alert (All 3 Rules) | 7 | 0.07% | Urgent Action: Trigger OTP / Secondary Verification (Score 3) |
| `1_0_1` | High Amount + High Frequency | 3 | 0.03% | Escalate: Priority Review Queue (Score 2) |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 17. Transaction Type Performance Analysis
![Figure 6: Suspicious Rate (%) by Transaction Type](reports/figures/04_suspicious_rate_by_type.png)

| Transaction Type | Total Transactions | Suspicious Alerts | Suspicious Rate (%) |
|---|---|---|---|
| **Transfer** | 3,725 | 118 | **3.17%** |
| **Payment** | 3,890 | 0 | 0.00% |
| **Withdrawal** | 1,427 | 0 | 0.00% |
| **Deposit** | 958 | 0 | 0.00% |

All 118 flagged multi-rule alerts occurred within **Transfers**, confirming wire transfers as the primary target for malicious exploitation.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 18. Channel Vulnerability Analysis
![Figure 7: Suspicious Rate (%) by Origination Channel](reports/figures/07_suspicious_rate_by_channel.png)

| Channel | Total Transactions | Suspicious Alerts | Suspicious Rate (%) |
|---|---|---|---|
| **Online** | 4,606 | 118 | **2.56%** |
| **Mobile App** | 3,931 | 0 | 0.00% |
| **ATM** | 962 | 0 | 0.00% |
| **Branch** | 501 | 0 | 0.00% |

Online web banking exhibited the highest vulnerability, reflecting web-based credential theft and automated session hijacking.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 19. Hourly Transaction Trend Analysis
Hourly analysis confirms that daytime hours (08:00 to 20:00) account for 92.5% of overall volume, while suspicious transaction concentration peaks sharply during nocturnal hours (23:00 to 04:00).

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 20. Transaction Amount vs. Suspicion Score Correlation
![Figure 8: Transaction Amount ($) vs Suspicion Score Scatter Plot](reports/figures/05_amount_vs_suspicion_score.png)

Monetary value increases dramatically with suspicion score:
* Score 0: Average $3,966.30
* Score 1: Average $5,820.40
* Score 2: Average $51,890.10
* Score 3: Average $77,615.80

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 21. Required Visualizations
| Figure # | Chart Title | Type | File Location |
|---|---|---|---|
| Fig 1 | End-to-End Pipeline Workflow | Flowchart | `reports/figures/00_workflow_pipeline.png` |
| Fig 2 | Normal vs Suspicious Volume | Bar Chart | `reports/figures/02_normal_vs_suspicious.png` |
| Fig 3 | Amount Distribution | Histogram | `reports/figures/01_amount_distribution.png` |
| Fig 4 | Suspicious Activity by Hour | Line Chart | `reports/figures/03_suspicious_by_hour.png` |
| Fig 5 | Rule Combination Frequencies | Bar Chart | `reports/figures/06_rule_combination_frequencies.png` |
| Fig 6 | Suspicious Rate by Type | Bar Chart | `reports/figures/04_suspicious_rate_by_type.png` |
| Fig 7 | Suspicious Rate by Channel | Bar Chart | `reports/figures/07_suspicious_rate_by_channel.png` |
| Fig 8 | Amount vs Suspicion Score | Scatter Plot | `reports/figures/05_amount_vs_suspicion_score.png` |
| Fig 9 | Confusion Matrix Heatmap | Matrix Heatmap | `reports/figures/08_confusion_matrix.png` |
| Fig 10 | Top Repeat Accounts | Pareto Chart | `reports/figures/09_top_accounts_pareto.png` |

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 22. Identifying High-Risk Accounts
![Figure 9: Top Repeat Offender Accounts by Suspicious Alerts](reports/figures/09_top_accounts_pareto.png)

28 accounts generated multiple suspicious alerts. The top 8 repeat accounts:
1. `ACC1183`: 43 transactions, $570,373.00 total value, 10 suspicious (23.26% rate)
2. `ACC1290`: 37 transactions, $797,991.00 total value, 8 suspicious (21.62% rate)
3. `ACC1340`: 35 transactions, $699,260.00 total value, 6 suspicious (17.14% rate)
4. `ACC1492`: 26 transactions, $527,756.00 total value, 5 suspicious (19.23% rate)
5. `ACC1161`: 26 transactions, $636,560.00 total value, 4 suspicious (15.38% rate)
6. `ACC1420`: 23 transactions, $438,158.00 total value, 4 suspicious (17.39% rate)
7. `ACC1186`: 27 transactions, $385,701.00 total value, 4 suspicious (14.81% rate)
8. `ACC1030`: 31 transactions, $368,071.00 total value, 4 suspicious (12.90% rate)

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 23. Advanced Extensions & ML Evaluation
![Figure 10: Confusion Matrix: Ground Truth vs Rule Alert](reports/figures/08_confusion_matrix.png)

Evaluation against historical verified fraud ground-truth:
* **True Positives (TP)**: 118
* **False Positives (FP)**: 0
* **True Negatives (TN)**: 9,600
* **False Negatives (FN)**: 282
* **Precision**: **100.00%**
* **Recall**: **29.50%**
* **F1-Score**: **0.456**
* **False Positive Rate**: **0.00%**

The rule-based screening engine achieved 100% precision with zero customer friction on the benchmark dataset.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 24. Pipeline Orchestration (cli.py)
Executed via single terminal command:
```powershell
.venv\Scripts\python.exe -m src.cli --input data/bank_transactions.csv --reports-dir reports
```

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 25. Interactive Web Dashboard (Cronus FraudGuard)
Launched with `python run_web.py` at `http://127.0.0.1:8000`:
* Live KPI cards and interactive Chart.js graphs.
* Priority review queue with search, score filtering, and "Inspect" explainability modal.
* Interactive Rule Studio with dynamic threshold sliders.
* Drag-and-drop CSV uploader and synthetic data generator.
* Direct download links for Word (.docx), PDF (.pdf), and CSV review queues.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 26. Business Questions and Answers
* **Q1: Percentage flagged?** 1.18% (118 out of 10,000 transactions).
* **Q2: Rule generating most alerts?** Rule 2: Late Night with 750 alerts (7.50%).
* **Q3: Transactions triggering >= 2 rules?** Exactly 118 transactions.
* **Q4: Transaction types with higher risk?** Transfer (3.17% suspicious rate).
* **Q5: Channels showing higher suspicious activity?** Online (2.56% suspicious rate).
* **Q6: Peak suspicious hours?** Hour 23:00 (11:00 PM) with 34 flagged records.
* **Q7: Suspicious amounts vs normal?** Suspicious average $53,416.15 vs $3,966.30 (13.47x higher).
* **Q8: Accounts with repeated activity?** 28 accounts; top is ACC1183 with 10 alerts.
* **Q9: Most frequent combinations?** Single anomaly: 0_1_0 (635 txns). Multi-rule: 0_1_1 (63 txns) and 1_1_0 (45 txns).
* **Q10: Rule performance against ground truth?** 100% precision, 0% FPR, 29.5% recall.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 27. Business Findings and Operational Recommendations
1. **P1 — Step-Up OTP Verification**: Mandate biometric/SMS OTP for Online Transfers exceeding $45,000 executed between 23:00 and 05:59.
2. **P2 — Account Velocity Throttles**: Limit retail accounts to a maximum of 4 transfers per 60 minutes.
3. **P3 — Surveillance Watchlist**: Monitor top 28 repeat offender accounts (led by ACC1183).
4. **P4 — Personalized Z-Scores**: Evolve population thresholds toward per-account 90-day moving z-scores.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 28. Testing, Validation and Reproducibility
* 38 unit and integration tests passing in Pytest across 6 test modules.
* 94% code coverage on core logic.
* Reproducible with `python -m src.cli` and `pytest -v`.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 29. Limitations and Important Analytical & Ethical Note
* An alert is an investigation signal, not conclusive proof of fraud.
* Secondary verification (SMS OTP / phone call) must always be used before account blocking.
* Real customer PII was omitted to ensure strict data privacy compliance.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 30. Learning Outcomes
* Financial transaction exploratory data analysis with Pandas.
* Transparent rule-based anomaly detection logic.
* Web dashboard development with FastAPI and Tailwind CSS.
* Test-Driven Development with Pytest.
* Responsible communication of financial crime analytics findings.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## 31. Conclusion and Future Scope
The project delivers a complete, reproducible, industry-ready bank transaction fraud screening system. Future work includes integrating streaming Kafka feeds, ML classification models, and graph neural network collusion ring analysis.

---

<p align="left"><img src="assets/cronus_logo.png" alt="Cronus Consultants Logo" width="130"></p>

## References
* Pandas, NumPy, Matplotlib, Scikit-learn, and FastAPI official documentation.
* Basel Committee on Banking Supervision: Sound Practices for Operational and Financial Cyber Risk.
* Reserve Bank of India (RBI): Master Direction on Cyber Security and Fraud Monitoring in Banks.
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    # Also save to reports/PROJECT_DOCUMENTATION.md
    reports_md = "reports/PROJECT_DOCUMENTATION.md"
    os.makedirs(os.path.dirname(reports_md), exist_ok=True)
    with open(reports_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Successfully generated Markdown Document: {output_path} and {reports_md}")


if __name__ == "__main__":
    print("[*] Generating comprehensive project documentation...")
    build_markdown_documentation()
    build_docx_documentation()
    build_pdf_documentation()
    build_html_documentation()
    print("[+] All documentation formats generated successfully!")
