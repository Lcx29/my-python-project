class FundBaseData(object):

    def __init__(self, fund_code, fund_name, initial_amount, holding_cost_price, available_shares):
        # 基金代码
        self._fund_code = fund_code
        # 基金名称
        self._fund_name = fund_name
        # 初始金额
        self._initial_amount = initial_amount
        # 持仓成本
        self._holding_cost_price = holding_cost_price
        # 可以份额
        self._available_shares = available_shares

    @property
    def fund_code(self):
        return self._fund_code

    @property
    def fund_name(self):
        return self._fund_name

    @property
    def initial_amount(self):
        return self._initial_amount

    @property
    def holding_cost_price(self):
        return self._holding_cost_price

    @property
    def available_shares(self):
        return self._available_shares
