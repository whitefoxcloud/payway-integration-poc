import requests

PAYWAY_API_URL = "https://api.payway.com.au/rest/v1/transactions"
PAYWAY_SINGLE_USE_TOKEN_API_URL = "https://api.payway.com.au/rest/v1/single-use-tokens"
PAYWAY_PUBLISHABLE_API_KEY = ""  <-- This should be your publishable key
PAYWAY_SECRET_API_KEY = ""  <-- This should be your secret key


def process_credit_card_payment(amount, card_number, card_holder_name, expiry_month, expiry_year, cvn, merchant_id="TEST"):
    # Tokenize card information
    # Should be using payway.js with trusted frame to tokenize card information
    # or calling the single use token endpoint directly from your frontend using publishable key
    card_info_data = {
        "paymentMethod": "creditCard",
        "cardNumber": card_number,
        "cardholderName": card_holder_name,
        "cvn": cvn,
        "expiryDateMonth": expiry_month,
        "expiryDateYear": expiry_year,
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

    # Process payment
    payment_data = {
        "transactionType": "payment",
        "singleUseTokenId": token,
        "customerNumber": "your_customer_number",
        "principalAmount": amount,
        "currency": "aud",
        "merchantId": merchant_id,
    }

    response = requests.post(
        PAYWAY_API_URL,
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
response = process_credit_card_payment(1000, "4111111111111111", "John Doe", "12", "25", "123")
print(response)
