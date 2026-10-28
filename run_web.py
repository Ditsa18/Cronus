"""Web Application Runner for Bank Fraud Detection Dashboard.

Usage:
    python run_web.py
    python run_web.py --port 8080 --host 0.0.0.0
"""

import sys
import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Start the Bank Fraud Detection Web Dashboard.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000).")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on code changes.")
    args = parser.parse_args()

    print("\n" + "="*75)
    print("  BANK FRAUD DETECTION & SCREENING — WEB DASHBOARD")
    print("="*75)
    print(f"  Access the dashboard in your web browser at:")
    print(f"  --> http://{args.host}:{args.port}")
    print("="*75 + "\n")

    uvicorn.run("src.web_app:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
