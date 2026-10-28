"""Script to ensure the Cronus Consultants logo is placed at the top left of all documentation pages."""

import os
import glob

LOGO_TAG = '<p align="left">\n  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">\n</p>\n\n'

def update_all_docs():
    target_files = ["README.md", "reports/FRAUD_MONITORING_MANAGEMENT_REPORT.md"] + glob.glob("docs/*.md")
    
    updated_count = 0
    for filepath in target_files:
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if "Cronus Consultants Logo" not in content:
            new_content = LOGO_TAG + content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            updated_count += 1
        else:
            print(f"Already present: {filepath}")

    print(f"\nDone! Updated {updated_count} documentation files.")

if __name__ == "__main__":
    update_all_docs()
