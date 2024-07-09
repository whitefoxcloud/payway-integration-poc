import json
from logging import getLogger
import requests

from .base import BaseClient
from .payment import PaymentRequest
from ..errors import PaywayError
from .customer import CustomerRequest
from .transaction import TransactionRequest


logger = getLogger(__name__)


class PayWayClient(CustomerRequest, TransactionRequest, PaymentRequest, BaseClient):
    """
    PayWay Client to connect to PayWay and perform methods given credentials
    """

    def __init__(
        self, api_base_url, merchant_id, bank_account_id, secret_api_key, publishable_api_key
    ):
        """
        :param api_base_url : str                       = PayWay API Base URL
        :param merchant_id        : str                 = PayWay Merchant ID
        :param bank_account_id   : str                  = PayWay Bank Account ID
        :param secret_api_key   : str                   = PayWay Secret APi Key
        :param publishable_api_key   : str              = PayWay Publishable API Key
        """
        self._validate_credentials(
            merchant_id, bank_account_id, secret_api_key, publishable_api_key
        )
        self.payway_api_base_url = api_base_url
        self.merchant_id = merchant_id
        self.bank_account_id = bank_account_id
        self.secret_api_key = secret_api_key
        self.publishable_api_key = publishable_api_key

        session = requests.Session()
        session.auth = (self.secret_api_key, "")
        headers = {"content-type": "application/x-www-form-urlencoded"}
        session.headers = headers
        self.session = session
        session_no_headers = requests.Session()
        session_no_headers.auth = session.auth
        self.session_no_headers = session_no_headers

    def _validate_credentials(
        self, merchant_id, bank_account_id, secret_api_key, publishable_api_key
    ):
        if (
            not merchant_id
            or not bank_account_id
            or not secret_api_key
            or not publishable_api_key
        ):
            if not secret_api_key or not publishable_api_key:
                logger.error("PayWay API keys not found")
                raise PaywayError(
                    message="PayWay API keys not found", code="INVALID_API_KEYS"
                )
            logger.error(
                "Merchant ID, bank account ID, secret API key, publishable API key are "
                "invalid"
            )
            raise PaywayError(
                message="Invalid credentials", code="INVALID_API_CREDENTIALS"
            )
