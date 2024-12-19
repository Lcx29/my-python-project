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
