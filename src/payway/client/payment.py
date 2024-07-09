from logging import getLogger

from .base import TOKEN_NO_REDIRECT_ENDPOINT_PATH, TRANSACTION_ENDPOINT_PATH, CUSTOMER_ENDPOINT_PATH
from ..consts import CREDIT_CARD_PAYMENT_CHOICE, BANK_ACCOUNT_PAYMENT_CHOICE, VALID_PAYMENT_METHOD_CHOICES
from ..errors import PaywayError
from ..models import TokenResponse, PayWayTransaction, PaymentSetup
from ..client.client import (
    BaseClient
)

logger = getLogger(__name__)


class PaymentRequest(BaseClient):
    def create_token(self, payway_obj, payment_method, idempotency_key=None):
        """
        Creates a single use token for a Customer's payment setup (credit card or bank account)
        :param payway_obj:   object: one of model.PayWayCard or model.BankAccount object
        :param payment_method:   str: one of `card` or `direct_debit`
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        """
        data = payway_obj.to_dict()
        if payment_method == "card":
            payway_payment_method = CREDIT_CARD_PAYMENT_CHOICE
        elif payment_method == "direct_debit":
            payway_payment_method = BANK_ACCOUNT_PAYMENT_CHOICE
        else:
            raise PaywayError(
                message="Invalid payment method. Must be one of %s"
                % ", ".join(VALID_PAYMENT_METHOD_CHOICES),
                code="INVALID_PAYMENT_METHOD",
            )
        data.update(
            {
                "paymentMethod": payway_payment_method,
            }
        )
        logger.info("Sending Create Token request to PayWay.")
        response = self.post_request(
            TOKEN_NO_REDIRECT_ENDPOINT_PATH,
            data,
            auth=(self.publishable_api_key, ""),
            idempotency_key=idempotency_key,
        )
        logger.info("Response from server: %s" % response)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            token_response = TokenResponse().from_dict(response.json())
            return token_response, errors

    def create_card_token(self, card, idempotency_key=None):
        """
        :param card:    PayWayCard object represents a customer's credit card details
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        See model.PayWayCard
        """
        return self.create_token(card, "card", idempotency_key=idempotency_key)

    def create_bank_account_token(self, bank_account, idempotency_key=None):
        """
        :param bank_account:    BankAccount object represents a customer's bank account
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        See model.BankAccount
        """
        return self.create_token(
            bank_account, "direct_debit", idempotency_key=idempotency_key
        )

    def process_payment(self, payment, idempotency_key=None):
        """
        Process an individual payment against a Customer with active Recurring Billing setup.
        :param payment: PayWayPayment object (see model.PayWayPayment)
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        """
        data = payment.to_dict()
        logger.info("Sending Process Payment request to PayWay.")
        response = self.post_request(TRANSACTION_ENDPOINT_PATH, data, idempotency_key=idempotency_key)
        logger.info("Response from server: %s" % response)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            # convert response to PayWayTransaction object
            transaction = PayWayTransaction.from_dict(response.json())
        return transaction, errors

    def update_payment_setup(self, token, customer_id):
        """
        Updates the Customer's Payment Setup with a new Credit Card or Bank Account.
        :param token: PayWay credit card or bank account token
        :param customer_id: PayWay customer ID
        """
        endpoint = "%s/%s/payment-setup" % (CUSTOMER_ENDPOINT_PATH, str(customer_id))
        data = {
            "singleUseTokenId": token,
            "merchantId": self.merchant_id,
            "bankAccountId": self.bank_account_id,
        }
        response = self.put_request(endpoint, data)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            ps = PaymentSetup.from_dict(response.json())
        return ps, errors
