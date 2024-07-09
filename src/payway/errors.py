class PaywayError(Exception):
    _code = None
    _message = None

    def __init__(self, code, message, *args, **kwargs):
        super(PaywayError, self).__init__(*args, **kwargs)

        self._code = code
        self._message = "{}: {}".format(code, message).encode("utf-8")

    def __str__(self):
        return self._message


class PaymentError(object):
    field_name = None
    message = None
    field_value = None

    @staticmethod
    def from_dict(payway_response):
        """
        Returns a list of errors from PayWay
        :param: payway_response: dict PayWay response dictionary
        """
        errors = payway_response.get("data")
        payment_errors = []
        for error in errors:
            payway_error = PaymentError()
            payway_error.field_name = error.get("fieldName")
            payway_error.message = error.get("message")
            payway_error.field_value = error.get("fieldValue")
            payment_errors.append(payway_error)
        return payment_errors

    def to_message(self):
        return "Field: {} Message: {} Field Value: {}".format(
            self.field_name,
            self.message,
            self.field_value,
        )

    @staticmethod
    def list_to_message(payway_errors):
        """
        Convert list to readable string
        :param payway_errors:
        :return:
        """
        message = ""
        for error in payway_errors:
            message += error.to_message()
            if len(payway_errors) > 1:
                message += " | "
        return message


class ServerError(object):
    error_number = None
    trace_code = None

    @staticmethod
    def from_dict(response):
        """
        :param: response: dict PayWay response dictionary
        """
        payway_error = ServerError()
        payway_error.error_number = response.get("errorNumber")
        payway_error.trace_code = response.get("traceCode")
        return payway_error

    def to_message(self):
        return "Error number: {} Trace code: {}".format(
            self.error_number, self.trace_code
        )
