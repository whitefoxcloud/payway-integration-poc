import os

from dotenv import load_dotenv

load_dotenv()

class PayWayConfig:
    PAYWAY_API_BASE_URL = os.getenv("PAYWAY_API_BASE_URL")
    PAYWAY_MERCHANT_ID = os.getenv("PAYWAY_MERCHANT_ID")
    PAYWAY_BANK_ACCOUNT_ID = os.getenv("PAYWAY_BANK_ACCOUNT_ID")
    PAYWAY_PUBLISHABLE_API_KEY = os.getenv("PAYWAY_PUBLISHABLE_API_KEY")
    PAYWAY_SECRET_API_KEY = os.getenv("PAYWAY_SECRET_API_KEY")


PAYWAY_CONFIG = PayWayConfig()
