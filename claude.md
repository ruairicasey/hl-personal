# CLAUDE.md

## Project
Algorithmic trading bot for Hyperliquid DEX (perpetual futures). Python, uv.
MAINNET — all code touches real money. Safety is non-negotiable.

## Plan Mode
- Make plans extremely concise. Sacrifice grammar for concision.
- End each plan with unresolved questions, if any.

## Workflow Rules
1. **Plan First:** Analyze request, explore codebase, present step-by-step plan before writing code.
2. **Execute Small Chunks:** Break tasks into smallest functional units.
3. **Test/Verify:** Run tests if they exist. Otherwise, verify changes work.
4. **Fix & Verify:** If issues found, fix and re-verify until working.
5. **Commit Atomically:** Logical commits with clear messages after verification.
6. **Review:** Self-review for security issues, edge cases, consistency.
7. *Update Changelog:* Before pushing to GitHub, add a concise entry to changelog.md summarizing the changes. Group related commits into one entry.

## Architecture
- `src/config.py` — validates and exposes all env vars; single source of truth for config
- `src/client.py` — Hyperliquid client factory (get_info, get_exchange)
- `src/data/` — Market data collection, WebSocket streams, storage
- `src/indicators/` — VWAP, volume profile, order flow metrics
- `src/strategy/` — Signal generation, confluence scoring
- `src/execution/` — Order placement, position management
- `src/risk/` — Position sizing, drawdown limits, circuit breakers
- `src/backtest/` — Backtesting harness, historical simulation
- `tests/` — Unit tests for each module

## Conventions
- Config from .env via python-dotenv. Never hardcode keys or addresses.
- All env vars parsed and validated at import time in `src/config.py`. Never call `os.getenv()` outside config.
- Type hints on all function signatures.
- Dataclasses or Pydantic for structured data (trades, candles, signals).
- Async for all WebSocket/streaming code.
- Sync for one-shot scripts and backtesting.
- Logging via `logging` module, not print(). Include timestamps.
- All prices/sizes as Decimal, never float, for financial calculations.
- Raise on unexpected API errors; never swallow exceptions in execution/risk paths.
- Retry transient network errors (max 3x, exponential backoff) in data/streaming code only.
- On unrecoverable error: cancel all open orders, log reason, exit cleanly.
- All WebSocket streams must implement reconnection with exponential backoff; disconnect is non-fatal.
- Testnet available but currently unreliable; dev with mainnet + minimum sizing. When stable, `HL_TESTNET=true` in `.env` should switch `client.py` to `constants.TESTNET_API_URL`.

## Safety Rules (CRITICAL)
- Never place market orders in test scripts.
- All order scripts must print order details BEFORE placing and require confirmation.
- Default position sizes to minimum (0.001 BTC or equivalent).
- Risk checks must run before every order — no bypass path.
- Never commit .env or any file containing private keys.
- If unsure about an order parameter, ask — don't guess.
- `MAX_POSITIONS` env var caps concurrent open positions; risk module enforces before any entry.

## Naming
- Files: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE
- Indicators return dataclasses, not raw dicts or tuples