# Example PayWay SDK

This simple SDK was developed as an example SDK client that abstracts away the complexities of direct API calls to PayWay. Using SDK client, you can enjoy several benefits:
- **Ease of Use**: The SDK provides intuitive functions that simplify interactions with the PayWay API, reducing boilerplate code and making your codebase cleaner.
- **Improved Reliability**: Our SDK handles many common issues such as retries, error handling, and response parsing, ensuring more reliable and robust communication with the PayWay API.
- **Enhanced Security**: By managing authentication and secure data transmission within the SDK, we minimize potential security vulnerabilities in your application.

You can integrate this SDK into your project. The repository includes comprehensive examples to help you get started quickly.


### SDK Usage Example: Credit Card Payment

Here's an example of how you can use our example PayWay SDK to process a credit card payment. 

Please note that this is for demonstration purposes only, and not an official SDK from PayWay, hence you should adapt it to your specific requirements and security standards.

Create a PayWay client instance:
```python
payway_client = PayWayClient(
    api_base_url="https://api.payway.com.au/rest/v1",
    merchant_id="TEST",
    bank_account_id="0000000A",
    publishable_api_key="YOUR_PUBLISHABLE_API_KEY",
    secret_api_key="YOUR_SECRET_API_KEY",
)
```

Obtain a single use token for a credit card:
```python
# Create a card instance
card = PayWayCard(
    card_number="4715142376126536",
    cvn="218",
    card_holder_name="Filippa Padovano",
    expiry_date_month="04",
    expiry_date_year="29"
)

# Create card token and create customer
token_response, errors = payway_client.create_card_token(card)
if errors:
    for error in errors:
        print(error.to_message())
        return
token = token_response.token

# Log card token
print("Created card token:", token)
```

Create a customer and store the card token:
```python
# Create a customer instance
customer = PayWayCustomer(
    custom_id="[YOUR_CUSTOMER_ID]",
    customer_name="John Doe",
    email_address="johndoe@whitefox.cloud",
    send_email_receipts=False,
    phone_number="0343232323",
    street="1 Test Street",
    street2="2 Test Street",
    city_name="Melbourne",
    state="VIC",
    postal_code="3000",
    token=token,
)

# Store the customer information with the card
payway_customer, errors = payway_client.create_customer(customer)
if errors:
    for error in errors:
        print(error.to_message())
        return
    
# Log customer creation information
print("Created customer:", payway_customer.customer_number)
```

Process a transaction:
```python
# Create a transaction instance
payment = PayWayPayment(
    customer_number=payway_customer.customer_number,
    transaction_type="payment",
    amount="YOUR_AMOUNT",
    currency="aud",
    order_number="YOUR_ORDER_NUMBER",
    ip_address=""
)

# Process the payment transaction
transaction, errors = payway_client.process_payment(payment)
if errors:
    for error in errors:
        print(error.to_message())
        return
    
# Log transaction information
print("Processed transaction:", transaction.transaction_id)
print("Transaction status:", transaction.status)
```

## Disclaimer

The code introduced in this repo is for demonstration purposes only, and not an official code or SDK from PayWay, hence you should adapt it to your specific requirements and security standards.

We will not be responsible for any misuse or damage caused. Use it at your own risk.
