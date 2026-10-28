<p align="left">
  <img src="assets/logo.jpg" alt="Cronus Consultants Logo" width="180">
</p>

# Execution Environment Capability Manifest

**Generated Date**: 2026-10-28  
**Project Workspace**: `C:\Users\HP\.gemini\antigravity\scratch\bank-fraud-detection`  
**Operating System**: Windows (Microsoft Windows 10/11 x64, PowerShell host)

## Capability Inventory

| Capability | Classification | Details & Toolchain |
|---|---|---|
| **Filesystem Access** | VERIFIED AVAILABLE | Full read, write, create, edit in `C:\Users\HP\.gemini\antigravity\scratch\bank-fraud-detection` |
| **Terminal / Shell Execution** | VERIFIED AVAILABLE | PowerShell 5.1/7+ execution via `run_command` |
| **Python Runtime** | VERIFIED AVAILABLE | Python 3.11.6 in dedicated virtual environment (`.venv\Scripts\python.exe`) |
| **Package Manager** | VERIFIED AVAILABLE | `uv` 0.10.10 providing ultra-fast pip dependency resolution |
| **Data & Scientific Libraries** | VERIFIED AVAILABLE | `pandas` 3.1.0, `numpy` 2.4.6, `matplotlib` 3.11.2, `scikit-learn` 1.9.1, `scipy` 1.17.1 |
| **Testing Framework** | VERIFIED AVAILABLE | `pytest` 9.2.0, `pytest-cov` 7.1.0 |
| **Reporting Tools** | VERIFIED AVAILABLE | `tabulate` 0.10.0, Matplotlib image output (PNG/SVG) |
| **Git Version Control** | VERIFIED AVAILABLE | `git version 2.51.0.windows.1` |
| **Internet & Web Search** | VERIFIED AVAILABLE | `search_web`, `read_url_content` |
| **Browser Automation** | AVAILABLE WITH LIMITATIONS | Selenium installed, but headless local CLI & automated test suites are primary |
| **Background Tasks** | VERIFIED AVAILABLE | Asynchronous execution via `run_command` with task management |
| **External Deployment** | UNAVAILABLE (Local-First) | Local execution verified; cloud deployment not authorized without explicit user credentials |

## Rationale for Runtime Selection
Python 3.11 was selected over Python 3.14 for maximum ecosystem compatibility with current binary wheels for `numpy`, `scipy`, `pandas`, and `matplotlib`. A clean virtual environment (`.venv`) is configured and pinned.
