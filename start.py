import json
import sys
from typing import Dict, Any

import pandas as pd
from datetime import datetime

import base.lcn_time as lcn_time
import function.fund.tian_tian_fund as tian_tian_fund
import function.fund.zhao_shang_personal_finance as zhao_shang_personal_finance
import function.fund.fang_tang_push as fang_tang_push
from base.lcn_base_class import AssetOverview

DEFAULT_FILE_PATH = "./my_python_config.json"


def get_file_path_from_argv() -> str:
    """获取文件路径

    从命令行参数中获取文件路径，如果没有则返回默认路径

    Returns
        文件路径
    """

    # 第一个参数为脚本的名称
    for index in range(1, len(sys.argv)):
        if sys.argv[index] == "--file":
            return sys.argv[index + 1]
    return DEFAULT_FILE_PATH


def load_json_config_from_file(file_path: str) -> Dict[str, Any]:
    """从文件中读取 JSON 配置数据

    从指定的文件路径中读取 JSON 配置数据并按照字典格式返回

    Args:
        file_path: 文件路径

    Returns:
        包含 JSON 配置数据的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Configuration file not found.")
        return {}
    except json.JSONDecodeError:
        print("Invalid JSON format in configuration file.")
        return {}


def fetch_asset_data_overview(asset_config: Dict[str, Any], is_fund: bool) -> Dict[str, Any]:
    """获取资产数据总览

    从配置中获取资产初始数据，根据配置请求对应的接口获取基金或者理财数据，并返回总览数据

    Args:
        asset_config: 资产配置
        is_fund: 是否为基金

    Returns:
        资产数据总览
    """

    show_max_count = asset_config.get("show_max_count", 0)
    fund_buy_list = asset_config.get("buy_list", [])

    all_asset_overview = {
        "initial_amount": 0.0,
        "current_amount": 0.0,
        "profit_loss_situation": 0.0,
        "preview_day_diff_amount": 0.0,
        "overview_str": ""
    }

    for config_personal_finance_data in fund_buy_list:
        # 加 1, 为了计算每日的差值, 所以需要比需要的行数多请求 1 条数据
        one_asset_overview = handle_one_asset_data(config_personal_finance_data, show_max_count + 1, is_fund)
        all_asset_overview["initial_amount"] += one_asset_overview.initial_amount
        all_asset_overview["current_amount"] += one_asset_overview.current_amount
        all_asset_overview["profit_loss_situation"] += one_asset_overview.profit_loss_situation()
        all_asset_overview["preview_day_diff_amount"] += one_asset_overview.preview_day_diff_amount
        all_asset_overview["overview_str"] += change_one_asset_overview_to_string(one_asset_overview)

    return all_asset_overview


def handle_one_asset_data(config_data: dict[str, str], request_count: int, is_fund: bool) -> AssetOverview:
    """处理一个资产的数据

    Args:
        config_data: 配置的数据
        request_count:  请求的天数
        is_fund: 是否为基金

    Returns:
        资产数据总览
    """

    if is_fund:
        # 有的基金最大显示 2 天前的数据 + 节假日不会有数据, 按照节假日最大 8 天坐冗余 + 希望请求的天数, 得到请求多少天前的数据
        request_start_day = lcn_time.before_today(2 + 8 + request_count)
        # 结束时间, 直接为今天
        request_end_day = lcn_time.today()

        # 请求天天基金获取对应的基金情况
        asset_response_list = tian_tian_fund.fetch_fund_data(config_data["code"], request_count, request_start_day,
                                                             request_end_day)
    else:
        # 请求招商理财获取对应的理财情况
        asset_response_list = zhao_shang_personal_finance.fetch_personal_finance_data(config_data["code"],
                                                                                      request_count)

    # 持有份额
    available_shares = config_data["available_shares"]
    # 投入金额
    initial_amount = config_data["initial_amount"]

    asset_overview = AssetOverview(
        code=config_data["code"],
        name=config_data["name"],
        initial_amount=initial_amount,
        available_shares=available_shares,
        current_amount=0.0,
        preview_day_diff_amount=0.0,
        date_detail_list=[]
    )

    for index, asset_response in enumerate(asset_response_list):

        # 最后一行不处理, 只是用来计算上一次的差值
        if index + 1 == request_count:
            break

        # 当天的金额 = 持有的份额 * 当天的净值, 保留 2 为小数
        current_money = available_shares * asset_response.net_asset_value

        next_item = asset_response_list[index + 1]
        # 每个基金的盈利情况，只需要根据第一个的数据计算即可
        if index == 0:
            asset_overview.current_amount = current_money
            asset_overview.preview_day_diff_amount = (
                    available_shares * (asset_response.net_asset_value - next_item.net_asset_value))

        # 填充信息 日期 单位净值 当前金额 当天盈利情况
        asset_overview.date_detail_list.append([
            # 将字符串格式为 yy-mm-dd
            format_date_to_short(asset_response.date),
            asset_response.net_asset_value,
            current_money,
            current_money - initial_amount,
            available_shares * (asset_response.net_asset_value - next_item.net_asset_value)
        ])
    return asset_overview


def change_one_asset_overview_to_string(asset_overview: AssetOverview) -> str:
    """
    将资产的总览转为一个字符串
    Args:
        asset_overview: 资产的总览

    Returns:
        资产的总览字符串
    """

    # 在 markdown 中 2 个换行才是换行
    overview_title = (
        f"产品: {asset_overview.name}({asset_overview.code})\n\n"
        f"投入金额: {format_money(asset_overview.initial_amount)}, "
        f"当前金额: {format_money(asset_overview.current_amount)}, "
        f"总盈亏: {format_money(asset_overview.profit_loss_situation())}, "
        f"近两日差额: {format_money(asset_overview.preview_day_diff_amount)} \n\n"
    )

    asset_result_pd = pd.DataFrame(
        asset_overview.date_detail_list,
        columns=['日期', '净值', '金额', '盈亏', '近两日差额']
    )

    # 指定各列保留的小数位
    return overview_title + asset_result_pd.to_markdown(index=False, floatfmt=["", "", ".2f", ".2f", ".2f"]) + "\n\n"


def create_fang_tang_desc(fund_data_overview: dict[str, Any], personal_finance_data_overview: dict[str, Any]) -> str:
    init_amount_total = format_money(
        fund_data_overview["initial_amount"] + personal_finance_data_overview["initial_amount"])
    current_amount_total = format_money(
        fund_data_overview["current_amount"] + personal_finance_data_overview["current_amount"])
    profit_loss_situation_total = format_money(
        fund_data_overview["profit_loss_situation"] + personal_finance_data_overview[
            "profit_loss_situation"])
    preview_day_diff_amount_total = format_money(
        fund_data_overview["preview_day_diff_amount"] + personal_finance_data_overview["preview_day_diff_amount"])

    desc = (f"**日期: {lcn_time.today()}**\n\n"
            f"所有产品总览:\n\n"
            f"投入金额: {init_amount_total}, "
            f"当前金额: {current_amount_total}, "
            f"总盈亏: {profit_loss_situation_total}, "
            f"近两日差额: {preview_day_diff_amount_total}\n\n"
            f"\n\n")

    desc += build_asset_all_overview("基金", fund_data_overview)
    desc += build_asset_all_overview("理财", personal_finance_data_overview)
    return desc


def build_asset_all_overview(product_type, asset_overview):
    initial_amount = format_money(asset_overview["initial_amount"])
    current_amount = format_money(asset_overview["current_amount"])
    profit_loss_situation = format_money(asset_overview["profit_loss_situation"])
    preview_day_diff_amount = format_money(asset_overview["preview_day_diff_amount"])

    overview_str = asset_overview["overview_str"]

    return (
        f"***\n\n"
        f"{product_type}: 投入金额:{initial_amount}, "
        f"当前金额:{current_amount}, "
        f"总盈亏:{profit_loss_situation}, "
        f"近两日差额: {preview_day_diff_amount}\n\n"
        f"{overview_str}"
    )


def format_date_to_short(date_str: str) -> str:
    """
    将日期字符串从 'yyyy-mm-dd' 格式转换为 'yy-mm-dd' 格式

    Args:
        yyyy-mm-dd 格式的字符串

    Returns:
        yy-mm-dd 格式的字符串
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Parse to datetime object
    return date_obj.strftime("%y-%m-%d")  # Format to 'yy-mm-dd'


def format_money(money):
    if money is None:
        return 0.0
    return round(money, 2)


if __name__ == '__main__':
    # 获取文件路径
    config_file_path = get_file_path_from_argv()

    # 获取配置
    json_config_data = load_json_config_from_file(config_file_path)

    # 基金情况
    current_fund_data_overview = fetch_asset_data_overview(json_config_data["fund"], True)

    # 理财情况
    current_personal_finance_data_overview = fetch_asset_data_overview(json_config_data["personal_finance"], False)

    # 推送方糖的描述
    send_desc = create_fang_tang_desc(current_fund_data_overview, current_personal_finance_data_overview)
    print("推送内容: " + send_desc)
    # 推送方糖
    fang_tang_config = json_config_data["fang_tang"]
    send_title = f"{lcn_time.today()} 收益通知\n\n"
    fang_tang_push.sc_send(fang_tang_config["send_key"], send_title, send_desc)
    print("推送成功")
