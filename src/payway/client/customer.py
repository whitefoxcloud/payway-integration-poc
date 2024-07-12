from logging import getLogger

from .base import CUSTOMER_ENDPOINT_PATH
from .client import BaseClient
from ..models import PayWayCustomer

logger = getLogger(__name__)


class CustomerRequest(BaseClient):
    def create_customer(self, customer, idempotency_key=None):
        """
        Create a customer in PayWay system

        POST /customers to have PayWay generate the customer number
        PUT /customers/{customerNumber} to use your own customer number

        :param customer:    PayWayCustomer object represents a customer in PayWay
        :param idempotency_key:   str: unique value to avoid duplicate POSTs
        See model.PayWayCustomer
        :return:
        """

        data = customer.to_dict()
        data.update(
            {"merchantId": self.merchant_id, "bankAccountId": self.bank_account_id}
        )

        logger.info("Sending Create Customer request to PayWay.")

        if customer.custom_id:
            endpoint = "{}/{}".format(CUSTOMER_ENDPOINT_PATH, customer.custom_id)
            response = self.put_request(endpoint, data)
        else:
            endpoint = "{}".format(CUSTOMER_ENDPOINT_PATH)
            response = self.post_request(
                endpoint, data, idempotency_key=idempotency_key
            )

        logger.info("Response from server: %s" % response)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            customer = PayWayCustomer().from_dict(response.json())
            return customer, errors

    def get_customer(self, customer_id):
        """
        Returns a PayWay Customer's Payment Setup, [Payment] Schedule, Contact Details, Custom Fields and Notes
        :param customer_id  str PayWay customer ID in PayWay system
        """
        endpoint = "%s/%s" % (CUSTOMER_ENDPOINT_PATH, str(customer_id))
        response = self.get_request(endpoint)
        errors = self._validate_response(response)
        if errors:
            return None, errors
        else:
            customer = PayWayCustomer.from_dict(response.json())
        return customer, errors
