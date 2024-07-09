class BankAccount(object):
    """
    account_name: str: 	Name used to open bank account.
    bsb: str: bank account BSB
    account_number: str: bank account number
    """

    def __init__(self, account_name, bsb, account_number):
        self.account_name = account_name
        self.bsb = bsb
        self.account_number = account_number

    def to_dict(self):
        return {
            "accountName": self.account_name,
            "bsb": self.bsb,
            "accountNumber": self.account_number,
        }
