from logging import getLogger

from .base import TRANSACTION_ENDPOINT_PATH
from .client import BaseClient
from ..models import PayWayTransaction

logger = getLogger(__name__)


class TransactionRequest(BaseClient):
    def get_transaction(self, transaction_id):
        """
        Lookup and return a transaction if found in PayWay
        :param transaction_id: str  A PayWay transaction ID
        """
        endpoint = "%s/%s" % (TRANSACTION_ENDPOINT_PATH, str(transaction_id))
        response = self.get_request(endpoint)
        logger.info("Response from server: %s" % response)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            transaction = PayWayTransaction.from_dict(response.json())
        return transaction, errors

    def void_transaction(self, transaction_id, idempotency_key=None):
        """
        Void a transaction in PayWay
        :param transaction_id: str  A PayWay transaction ID
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        """
        endpoint = "%s/%s/void" % (TRANSACTION_ENDPOINT_PATH, transaction_id)
        response = self.post_request(endpoint, data={}, idempotency_key=idempotency_key)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            transaction = PayWayTransaction.from_dict(response.json())
        return transaction, errors

    def refund_transaction(
        self,
        transaction_id,
        amount,
        order_id=None,
        ip_address=None,
        idempotency_key=None,
    ):
        """
        Refund a transaction in PayWay
        :param transaction_id: str  A PayWay transaction ID
        :param amount:  str  amount to refund
        :param order_id:  str  optional reference number
        :param ip_address:  str  optional IP address
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        """
        endpoint = TRANSACTION_ENDPOINT_PATH
        data = {
            "transactionType": "refund",
            "parentTransactionId": transaction_id,
            "principalAmount": amount,
        }
        if order_id:
            data["orderNumber"] = order_id
        if ip_address:
            data["customerIpAddress"] = ip_address
        response = self.post_request(endpoint, data, idempotency_key=idempotency_key)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            transaction = PayWayTransaction.from_dict(response.json())
        return transaction, errors
