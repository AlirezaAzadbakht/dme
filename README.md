# DME — Dumbest Messenger Ever

Dumbest Messenger Ever is a deliberately simple, local-first, offline-friendly messenger built during internet blackouts.
It avoids complexity, servers, accounts, and telemetry, favoring explicit trust and simplicity over features.

> "Sometimes the internet is gone, but people still need to talk."

## Features
- Offline-first: works without internet or servers.
- Simple login using short secrets.
- Read receipts and timestamps.
- Minimal dependencies: only Python + Streamlit.

## Philosophy
DME embraces simplicity over cleverness.  
It is not perfect. It is not fancy. It is intentionally **the dumbest messenger ever** — small, auditable, and functional.

### ⚠️ Limitations
- Not secure against a compromised operating system.
- Does not protect against malware or keyloggers.
- No remote server sync (local-only).
- All users must trust the local machine or network.

## Getting Started
```bash
git clone https://github.com/AlirezaAzadbakht/dme.git
cd dme
pip install -r requirements.txt
streamlit run main.py
