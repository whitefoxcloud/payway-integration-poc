from src.config import PAYWAY_CONFIG
from src.payway.client.client import PayWayClient
from src.payway.models import BankAccount, PayWayCustomer, PayWayPayment
from src.utils import generate_random_string


def run_direct_debit_poc():
    # Create a PayWay client
    payway_client = PayWayClient(
        api_base_url=PAYWAY_CONFIG.PAYWAY_API_BASE_URL,
        merchant_id=PAYWAY_CONFIG.PAYWAY_MERCHANT_ID,
        bank_account_id=PAYWAY_CONFIG.PAYWAY_BANK_ACCOUNT_ID,
        publishable_api_key=PAYWAY_CONFIG.PAYWAY_PUBLISHABLE_API_KEY,
        secret_api_key=PAYWAY_CONFIG.PAYWAY_SECRET_API_KEY,
    )

    # Prepare a customer
    customer_id = generate_random_string(10)
    customer = PayWayCustomer(
        custom_id=customer_id,
        customer_name="John Doe",
        email_address="johndoe@whitefox.cloud",
        send_email_receipts=False,
        phone_number="0343232323",
        street="1 Test Street",
        street2="2 Test Street",
        city_name="Melbourne",
        state="VIC",
        postal_code="3000"
    )

    # Create a bank account
    bank_account = BankAccount(
        account_name='Test',
        bsb='000-000',
        account_number=123456
    )
    token_response, errors = payway_client.create_bank_account_token(bank_account)
    if errors:
        for error in errors:
            print(error.to_message())
            return
    token = token_response.token
    print("Created direct debit token:", token)

    # Assign token to customer
    customer.token = token
    payway_customer, errors = payway_client.create_customer(customer)
    if errors:
        for error in errors:
            print(error.to_message())
            return
    print("Created customer:", payway_customer.customer_number)

    # Process a transaction
    order_number = generate_random_string(10)
    customer_number = payway_customer.customer_number
    payment = PayWayPayment(
        customer_number=customer_number,
        transaction_type="payment",
        amount="100.00",
        currency="aud",
        order_number=order_number,
        ip_address=""
    )
    transaction, errors = payway_client.process_payment(payment)
    if errors:
        for error in errors:
            print(error.to_message())
            return
    print("Processed transaction:", transaction.transaction_id)
    print("Transaction status:", transaction.status)


if __name__ == "__main__":
    run_direct_debit_poc()
