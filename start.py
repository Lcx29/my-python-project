import function.fund.tian_tian_fund as tian_tian_fund
from function.fund.fund_base_data import FundBaseData

MY_FUND_DATA = [
    {}
]


def build_found_base_data_class(init_data):
    return FundBaseData(
        init_data["fundCode"],
        init_data["fundName"],
        init_data["initialAmount"],
        init_data["holdingCostRrice"],
        init_data["availableShares"]
    )


if __name__ == '__main__':
    for init_fund_data in MY_FUND_DATA:
        tian_tian_fund.cal_my_fund_profit_situation(build_found_base_data_class(init_fund_data))
