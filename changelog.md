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

## 2026-02-20 — Order placement smoke test

### Added
- **`src/test_order.py`** — mainnet order smoke test: fetches BTC mid price, places 0.001 BTC GTC limit buy at 10% below mid, requires explicit Y/N confirmation before placing, waits 5s, then cancels; uses `Decimal` for all prices/sizes, correct Hyperliquid tick size rounding, formatted box display of order details, structured logging with timestamps; confirmed working on mainnet

### Fixed
- **`src/client.py`** — `get_exchange()` now creates `eth_account.Account` from private key and passes the wallet object to `Exchange` (previously passed raw key string)
