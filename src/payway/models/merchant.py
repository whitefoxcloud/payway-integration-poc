class Merchant(object):
    """
    merchantId 	Issued by us to uniquely identify a merchant facility
    merchantName
    settlementBsb 	The BSB of your settlement bank account
    settlementAccountNumber 	The account number of your settlement bank account
    surchargeBsb 	If surcharges are settled separately, the BSB for your surcharge settlement account
    surchargeAccountNumber 	If surcharges are settled separately, the account number for your surcharge settlement
                            account
    """

    merchant_id = None
    merchant_name = None
    settlement_bsb = None
    settlement_account_number = None
    surcharge_bsb = None
    surcharge_account_number = None

    def to_dict(self):
        return {
            "merchantId": self.merchant_id,
            "merchantName": self.merchant_name,
            "settlementBsb": self.settlement_bsb,
            "settlementAccountNumber": self.settlement_account_number,
            "surchargeBsb": self.surcharge_bsb,
            "surchargeAccountNumber": self.surcharge_account_number,
        }

    @staticmethod
    def from_dict(payway_obj):
        """
        :param: payway_obj: dict PayWay response dictionary
        """
        merchant = Merchant()
        merchant.merchant_id = payway_obj.get("merchantId")
        merchant.merchant_name = payway_obj.get("merchantName")
        merchant.settlement_bsb = payway_obj.get("settlementBsb")
        merchant.settlement_account_number = payway_obj.get("settlementAccountNumber")
        merchant.surcharge_bsb = payway_obj.get("surchargeBsb")
        merchant.surcharge_account_number = payway_obj.get("surchargeAccountNumber")
        return merchant
