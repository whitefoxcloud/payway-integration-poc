from datetime import datetime

import requests

PAYWAY_API_URL = "https://api.payway.com.au/rest/v1/transactions"
PAYWAY_SINGLE_USE_TOKEN_API_URL = "https://api.payway.com.au/rest/v1/single-use-tokens"
PAYWAY_CUSTOMER_API_URL = "https://api.payway.com.au/rest/v1/customers/{customer_id}"
PAYWAY_REGULAR_PAYMENT_API_URL = "https://api.payway.com.au/rest/v1/customers/{customer_id}/schedule"
BANK_ID = "0000000A"
PAYWAY_PUBLISHABLE_API_KEY = ""  <-- This should be your publishable key
PAYWAY_SECRET_API_KEY = ""  <-- This should be your secret key


def process_direct_debit_payment(amount, frequency, bsb, account_number, account_name, customer_id, merchant_id="TEST"):
    # Tokenize card information
    # Should be using payway.js with trusted frame to tokenize card information
    # or calling the single use token endpoint directly from your frontend using publishable key
    card_info_data = {
        "paymentMethod": "bankAccount",
        "bsb": bsb,
        "accountNumber": account_number,
        "accountName": account_name,
    }
    tokenizing_response = requests.post(
        PAYWAY_SINGLE_USE_TOKEN_API_URL,
        data=card_info_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        auth=(PAYWAY_PUBLISHABLE_API_KEY, "")
    )
    token = tokenizing_response.json()["singleUseTokenId"]

    # Store the bank account to customer
    customer_data = {
        "singleUseTokenId": token,
        "merchantId": merchant_id,
        "bankAccountId": BANK_ID
    }
    customer_response = requests.put(
        PAYWAY_CUSTOMER_API_URL.format(customer_id=customer_id),
        data=customer_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        auth=(PAYWAY_SECRET_API_KEY, "")
    )


    # Set a schedule payment for the stored customer
    payment_data = {
        "frequency": frequency,
        "nextPaymentDate": datetime.today().strftime('%d %b %Y'),
        "regularPrincipalAmount": amount,
    }

    response = requests.put(
        PAYWAY_REGULAR_PAYMENT_API_URL.format(customer_id=customer_id),
        data=payment_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        auth=(PAYWAY_SECRET_API_KEY, "")
    )

    if response.status_code != 200:
        raise Exception("the payment was not successful")

    return response.json()


# Example usage
response = process_direct_debit_payment(1000, "weekly", "012003", "456789", "John Doe", "your_customer_number")
print(response)
