# PayWay POC

This repository contains proof of concept (POC) code for integrating PayWay for credit card payments and direct debit payments. PayWay is a secure and reliable online payment solution provided by Westpac.

## Scenarios

- Credit Card Payments: Process credit card transactions securely using PayWay.
- Direct Debit Payments: Set up and manage direct debit payments with ease.

## Getting Started

### Prerequisites
Before you begin, ensure you have met the following requirements:

- You have a PayWay account. If not, sign up at [PayWay](https://www.payway.com.au/sign-in) for a sandbox account.
- You have [Python](https://www.python.org/downloads/) installed on your machine.
- You have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your machine.

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/realthinhit/payway-poc.git
   cd payway-poc
   ```
   
2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
   
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Rename .env.example to .env (if .env.example is not present, create a .env file):
   ```
   mv .env.example .env
   ```

2. Add your PayWay credentials and other configuration settings to the .env file:
   ```
   PAYWAY_API_BASE_URL=https://api.payway.com.au/rest/v1
   PAYWAY_MERCHANT_ID=TEST
   PAYWAY_BANK_ACCOUNT_ID=0000000A
   PAYWAY_PUBLISHABLE_API_KEY=
   PAYWAY_SECRET_API_KEY=
   ```

## Running the Scenarios

Run the application using the following command:

```
python src/app/credit_card_poc.py  # for credit card payments
python src/app/direct_debit_poc.py  # for direct debit payments
```

## Project Structure
``` 
payway-poc/
│
├── .gitignore
├── .idea/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── credit_card_poc.py
│   │   └── direct_debit_poc.py
│   ├── config.py
│   ├── __init__.py
│   ├── payway/
│   │   ├── __init__.py
│   │   ├── client/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── client.py
│   │   │   ├── customer.py
│   │   │   ├── payment.py
│   │   │   └── transaction.py
│   │   ├── consts.py
│   │   ├── errors.py
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── bank.py
│   │       ├── customer.py
│   │       ├── merchant.py
│   │       └── payment.py
│   └── utils.py
└── requirements.txt
```