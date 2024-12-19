class AssetNetworkResponse(object):

    def __init__(self, date, net_asset_value):
        # 资产日期
        self._date = date
        # 单位净值
        self._net_asset_value = net_asset_value

    @property
    def date(self):
        return self._date

    @property
    def net_asset_value(self):
        return self._net_asset_value


class AssetOverview:
    def __init__(self, code, name, initial_amount, available_shares, current_amount, preview_day_diff_amount,
                 date_detail_list):
        # 代码
        self._code = code
        # 名称
        self._name = name
        # 初始金额
        self._initial_amount = initial_amount
        # 可用份额
        self._available_shares = available_shares
        # 当前的金额
        self._current_amount = current_amount
        # 最新的一天和前一天的差额
        self._preview_day_diff_amount = preview_day_diff_amount
        # 每天的详情列表
        self._date_detail_list = date_detail_list

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def initial_amount(self):
        return self._initial_amount

    @property
    def available_shares(self):
        return self._available_shares

    @property
    def current_amount(self):
        return self._current_amount

    # current_amount 需要提供设置方法, 因为需要后面赋值
    @current_amount.setter
    def current_amount(self, current_amount):
        self._current_amount = current_amount

    @property
    def preview_day_diff_amount(self):
        return self._preview_day_diff_amount

    @preview_day_diff_amount.setter
    def preview_day_diff_amount(self, preview_day_diff_amount):
        self._preview_day_diff_amount = preview_day_diff_amount

    @property
    def date_detail_list(self):
        return self._date_detail_list

    # 盈亏情况
    def profit_loss_situation(self):
        return round(self._current_amount - self.initial_amount, 2)
