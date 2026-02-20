"""
Mainnet order placement smoke test.
Places a GTC limit BUY for 0.001 BTC at 10% below mid, then cancels it.
Requires explicit Y confirmation before placing.
"""
import logging
import math
import time
from decimal import Decimal

from client import get_info, get_exchange

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

COIN = "BTC"
SIZE = Decimal("0.001")
DISCOUNT = Decimal("0.90")  # 10% below mid


def main() -> None:
    info = get_info()
    exchange = get_exchange()

    # 1. Fetch mid price
    mids = info.all_mids()
    mid_price = Decimal(mids[COIN])
    logger.info(f"BTC mid price: ${mid_price:,.2f}")

    # 2. Limit price: 10% below mid, rounded to Hyperliquid tick size.
    # HL enforces 5 significant figures for perp prices. At BTC ~$60-70k
    # that means whole dollars (tick = $1).
    raw_price = mid_price * DISCOUNT
    magnitude = math.floor(math.log10(float(raw_price)))
    tick = Decimal(10 ** (magnitude - 4))  # 5 sig figs → 10^(mag-4)
    limit_price = (raw_price / tick).quantize(Decimal("1")) * tick

    # 3. Print order details and require confirmation
    print()
    print("┌─── ORDER DETAILS ───────────────────────────────┐")
    print(f"│  Asset  : {COIN}-PERP (MAINNET)                    │")
    print(f"│  Side   : BUY (limit, GTC)                      │")
    print(f"│  Size   : {SIZE} BTC                             │")
    print(f"│  Price  : ${limit_price:>10,.0f}  (10% below mid ${mid_price:,.1f})  │")
    print("└─────────────────────────────────────────────────┘")
    print()

    confirm = input("Place this order on MAINNET? [y/N] ").strip().lower()
    if confirm != "y":
        logger.info("Aborted — no order placed.")
        return

    # 4. Place order
    logger.info("Placing order...")
    result = exchange.order(
        COIN,
        is_buy=True,
        sz=float(SIZE),
        limit_px=float(limit_price),
        order_type={"limit": {"tif": "Gtc"}},
    )
    logger.info(f"Order response: {result}")

    # 5. Extract oid from resting status
    try:
        status = result["response"]["data"]["statuses"][0]
        if "resting" not in status:
            logger.error(f"Unexpected order status (not resting): {status}")
            logger.error("Manual cancellation may be required — check your open orders.")
            return
        oid: int = status["resting"]["oid"]
    except (KeyError, IndexError, TypeError) as exc:
        logger.error(f"Could not parse order ID from response: {exc}")
        logger.error("Manual cancellation may be required — check your open orders.")
        return

    logger.info(f"Order resting. OID: {oid}")

    # 6. Wait before cancelling
    logger.info("Waiting 5 seconds...")
    time.sleep(5)

    # 7. Cancel
    logger.info(f"Cancelling OID {oid}...")
    cancel_result = exchange.cancel(COIN, oid)
    logger.info(f"Cancellation response: {cancel_result}")

    # 8. Confirm cancellation
    try:
        cancel_status = cancel_result["response"]["data"]["statuses"][0]
        if cancel_status == "success":
            logger.info("Order cancelled successfully.")
        else:
            logger.warning(f"Unexpected cancellation status: {cancel_status}")
    except (KeyError, IndexError, TypeError) as exc:
        logger.warning(f"Could not parse cancellation status: {exc}")


if __name__ == "__main__":
    main()
