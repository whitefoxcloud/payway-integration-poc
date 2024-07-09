import json

import requests

from src.payway.errors import PaywayError, PaymentError, ServerError


CUSTOMER_ENDPOINT_PATH = "/customers"
TRANSACTION_ENDPOINT_PATH = "/transactions"
TOKEN_ENDPOINT_PATH = "/single-use-tokens-redirect"
OWN_BANK_ACCOUNTS_ENDPOINT_PATH = "/your-bank-accounts"
TOKEN_NO_REDIRECT_ENDPOINT_PATH = "/single-use-tokens"


class BaseClient(object):
    session = requests.Session()
    session_no_headers = requests.Session()

    payway_api_base_url = ""
    merchant_id = ""
    bank_account_id = ""
    secret_api_key = ""
    publishable_api_key = ""

    def _validate_response(self, response):
        """
        Validates all responses from PayWay to catch documented PayWay errors.
        :param response: requests response object
        """
        if response.status_code in [
            400,
            401,
            403,
            405,
            406,
            407,
            409,
            410,
            415,
            429,
            501,
            503,
        ]:
            http_error_msg = "%s Client Error: %s for url: %s" % (
                response.status_code,
                response.reason,
                response.url,
            )
            raise PaywayError(code=response.status_code, message=http_error_msg)

        elif response.status_code in [404, 422]:  # Documented PayWay errors in JSON
            # parse error message
            errors = response.json()
            payway_errors = PaymentError().from_dict(errors)
            # instead of raising an exception, return the specific PayWay errors as a list
            return payway_errors

        elif response.status_code == 500:
            try:
                errors = response.json()
            except json.JSONDecodeError:
                raise PaywayError(
                    code=response.status_code, message="Internal server error"
                )
            # Documented PayWay server errors in JSON
            payway_error = ServerError().from_dict(errors)
            message = payway_error.to_message()
            raise PaywayError(code=response.status_code, message=message)

        else:
            return None

    def get_request(self, endpoint):
        return requests.get(
            url=self.payway_api_base_url + endpoint,
            auth=(self.secret_api_key, "")
        )

    def post_request(self, endpoint, data, auth=None, idempotency_key=None):
        """
        Supply an idempotency_key to avoid duplicate POSTs
        https://www.payway.com.au/docs/rest.html#avoiding-duplicate-posts
        """
        if not auth:
            auth = (self.secret_api_key, "")
        headers = {"content-type": "application/x-www-form-urlencoded"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return requests.post(
            url=self.payway_api_base_url + endpoint,
            auth=auth,
            data=data,
            headers=headers
        )

    def put_request(self, endpoint, data):
        headers = {"content-type": "application/x-www-form-urlencoded"}
        return requests.put(
            url=self.payway_api_base_url + endpoint,
            auth=(self.secret_api_key, ""),
            data=data,
            headers=headers
        )
