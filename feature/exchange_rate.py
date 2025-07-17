from decimal import Decimal

import requests

CNY_CODE = 'CNY'
USD_CODE = 'USD'
HKD_CODE = 'HKD'
MONEY_CODE_LIST = ['USD', 'CNY', 'HKD']
REQUEST_URL = f"https://api.exchangerate-api.com/v4/latest/{{code}}"


def exchange_rate(request_code):
    """
    获取指定货币的汇率数据
    :param request_code: 请求的货币代码，例如 'USD', 'CNY', 'HKD'
    """
    real_request_url = REQUEST_URL.format(code=request_code)
    response = requests.get(real_request_url, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch exchange rate data: {response.status_code}")
    data = response.json()
    return data['rates']


def exclude_element_from_list(target_list, index):
    """
    从列表中排除指定索引的元素
    :param target_list: 目标列表
    :param index: 要排除的元素索引
    :return: 新列表，不包含指定索引的元素
    """

    length = len(target_list)

    # 处理空列表情况
    if length == 0:
        return []

    # 规范化索引（处理负数索引）
    if index < 0:
        normalized_index = index + length
    else:
        normalized_index = index

    # 检查索引是否有效
    if 0 <= normalized_index < length:
        # 使用切片组合排除指定位置的元素
        return target_list[:normalized_index] + target_list[normalized_index + 1:]
    else:
        # 索引无效时返回整个列表的副本
        return target_list.copy()


def calculate_exchange_rate(cal_money, cal_code_index, other_rate_map):
    """
    计算指定货币与其他两种货币的汇率转换
    :param cal_money: 要计算的金额
    :param cal_code_index: 要计算的货币在 MONEY_CODE_LIST 中的索引
    :param other_rate_map: 其他货币的汇率映射，键为货币代码，值为对应的汇率
    """
    other_code_list = exclude_element_from_list(MONEY_CODE_LIST, cal_code_index)

    base_to_other_first_rate = other_rate_map[other_code_list[0]]
    base_to_other_second_rate = other_rate_map[other_code_list[1]]

    # USD 为基准计算金额
    base_to_first_money = Decimal(str(base_to_other_first_rate)) * Decimal(str(cal_money))
    base_to_second_money = Decimal(str(base_to_other_second_rate)) * Decimal(str(cal_money))

    print(
        f"1 {MONEY_CODE_LIST[cal_code_index]} = {base_to_other_first_rate:.3f} {other_code_list[0]} = {base_to_other_second_rate:.3f} {other_code_list[1]}")
    print(
        f"{cal_money:.3f} {MONEY_CODE_LIST[cal_code_index]} = {base_to_first_money:.3f} {other_code_list[0]} = {base_to_second_money:.3f} {other_code_list[1]}")


def show_rate(cal_money):
    usd_to_other_rate_map = exchange_rate(USD_CODE)

    usd_to_cny_rate = Decimal(str(usd_to_other_rate_map[CNY_CODE]))
    usd_to_hkd_rate = Decimal(str(usd_to_other_rate_map[HKD_CODE]))

    cny_to_usd_rate = Decimal("1.00") / usd_to_cny_rate
    cny_to_hkd_rate = usd_to_hkd_rate / usd_to_cny_rate

    hkd_to_usd_rate = Decimal("1.00") / usd_to_hkd_rate
    hkd_to_cny_rate = usd_to_cny_rate / usd_to_hkd_rate

    print(f"以 {USD_CODE} 为基准计算汇率:")
    calculate_exchange_rate(cal_money, 0, {"CNY": usd_to_cny_rate, "HKD": usd_to_hkd_rate})

    print(f"\n以 {CNY_CODE} 为基准计算汇率:")
    calculate_exchange_rate(cal_money, 1, {"USD": cny_to_usd_rate, "HKD": cny_to_hkd_rate})

    print(f"\n以 {HKD_CODE} 为基准计算汇率:")
    calculate_exchange_rate(cal_money, 2, {"USD": hkd_to_usd_rate, "CNY": hkd_to_cny_rate})


# 可以修改为需要计算的金额
CAL_NUMBER = 321.67 * 10

if __name__ == '__main__':
    show_rate(cal_money=CAL_NUMBER)
