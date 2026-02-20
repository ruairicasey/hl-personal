import os
from dotenv import load_dotenv
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants

load_dotenv()


def get_info() -> Info:
    api_url = os.getenv("HL_API_URL", constants.MAINNET_API_URL)
    return Info(api_url, skip_ws=True)


def get_exchange() -> Exchange:
    private_key = os.getenv("HL_PRIVATE_KEY")
    wallet_address = os.getenv("HL_WALLET_ADDRESS")
    api_url = os.getenv("HL_API_URL", constants.MAINNET_API_URL)
    return Exchange(private_key, api_url, account_address=wallet_address)
