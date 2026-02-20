# Changelog

## 2026-02-20 — Project bootstrap

### Added
- **uv project setup** — `pyproject.toml`, `uv.lock`, `.python-version` (Python 3.13.2)
- **Core dependencies** — `hyperliquid-python-sdk==0.22.0`, `python-dotenv==1.2.1`
- **`src/client.py`** — Hyperliquid client factory (`get_info`, `get_exchange`); reads `HL_API_URL`, `HL_PRIVATE_KEY`, `HL_WALLET_ADDRESS` from `.env`
- **`main.py`** — smoke test entry point; confirmed mainnet connection (229 assets)
- **`claude.md`** — project conventions, architecture layout, workflow rules, safety rules, naming standards

### Updated
- **`claude.md`** — added: error handling policy, WebSocket reconnection convention, `src/config.py` and `src/backtest/` to architecture, `MAX_POSITIONS` safety rule, testnet toggle note, config validation convention; fixed changelog path reference
