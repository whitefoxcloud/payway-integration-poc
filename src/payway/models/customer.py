from src.payway.models.payment import PaymentSetup


class PayWayCustomer(object):
    def __init__(
        self,
        custom_id=None,
        customer_name=None,
        email_address=None,
        send_email_receipts=None,
        phone_number=None,
        street=None,
        street2=None,
        city_name=None,
        state=None,
        postal_code=None,
        token=None,
        customer_number=None,
        payment_setup=None,
        notes=None,
        custom_field_1=None,
        custom_field_2=None,
        custom_field_3=None,
        custom_field_4=None,
    ):
        self.custom_id = custom_id
        self.customer_name = customer_name
        self.email_address = email_address
        self.send_email_receipts = send_email_receipts
        self.phone_number = phone_number
        self.street = street
        self.street2 = street2
        self.city_name = city_name
        self.state = state
        self.postal_code = postal_code
        self.token = token
        self.customer_number = customer_number
        self.payment_setup = payment_setup
        self.notes = notes
        self.customField1 = custom_field_1
        self.customField2 = custom_field_2
        self.customField3 = custom_field_3
        self.customField4 = custom_field_4

    def to_dict(self):
        customer = {
            "customerName": self.customer_name,
            "emailAddress": self.email_address,
            "sendEmailReceipts": "true" if self.send_email_receipts else "false",
            "phoneNumber": self.phone_number,
            "street1": self.street,
            "street2": self.street2,
            "cityName": self.city_name,
            "state": self.state,
            "postalCode": self.postal_code,
            "notes": self.notes,
            "customField1": self.customField1,
            "customField2": self.customField2,
            "customField3": self.customField3,
            "customField4": self.customField4,
        }
        if self.token:
            customer.update({"singleUseTokenId": self.token})
        return customer

    @staticmethod
    def from_dict(response):
        """
        Parse PayWay Customer response data
        :param response: dict    PayWay response dictionary
        :return:
        """
        customer = PayWayCustomer()
        contact = response.get("contact")
        customer.customer_name = contact.get("customerName")
        customer.email_address = contact.get("emailAddress")
        customer.send_email_receipts = contact.get("sendEmailReceipts")
        customer.phone_number = contact.get("phoneNumber")
        address = contact.get("address")
        customer.street = address.get("street1")
        customer.street2 = address.get("street2")
        customer.city_name = address.get("cityName")
        customer.state = address.get("state")
        customer.postal_code = address.get("postalCode")
        customer.customer_number = response.get("customerNumber")

        if response.get("paymentSetup") is not None:
            customer.payment_setup = PaymentSetup().from_dict(
                response.get("paymentSetup")
            )

        if response.get("customFields") is not None:
            custom_fields = response.get("customFields")
            for k, v in custom_fields.items():
                setattr(customer, k, v)

        if response.get("notes") is not None:
            customer.notes = response["notes"]

        return customer
