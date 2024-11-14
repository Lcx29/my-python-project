import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
import base.lcn_time as lcn_time
from function.fund.fund_base_data import FundBaseData


def request_fund_data(fund_code, start_date, end_date, type_="lsjz", page=1, per=20):
    # 请求天天基金页面
    url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type={}&code={}&page={}&sdate={}&edate={}&per={}" \
        .format(type_, fund_code, page, start_date, end_date, per)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    html_response = requests.get(url, headers=headers)
    html_response.encoding = "utf-8"
    return html_response


def parse_fund_data_from_html_response(html_response):
    soup = BeautifulSoup(html_response.text, 'html.parser')
    trs = soup.find_all("tr")
    res = []
    for tr in trs[1:]:
        # 净值日期
        date = tr.find_all("td")[0].text
        # 单位净值
        unit_net = tr.find_all("td")[1].text
        res.append([date, unit_net])

    return pd.DataFrame(res, columns=['净值日期', '单位净值'])


def get_fund_data(fund_code, start_date, end_date, show_count):
    # 正常情况下, 1 页，20 条, 满足了
    need_page_num = 1

    # lsjz 获取的基金类型
    html_response = request_fund_data(fund_code, start_date, end_date, "lsjz", need_page_num, show_count)
    return parse_fund_data_from_html_response(html_response)

    # res_df = pd.DataFrame()
    # res_df.insert(0, "基金代码", fund_code)

    # 需要确保库中有 tabulate (可以先 import tabulate)
    print(parse_data.to_markdown(index=False))


def request_start_day_cal(want_show_count=3):
    # 有的基金最大显示 2 天前的数据 + 节假日不会有数据, 按照节假日最大 8 天坐冗余 + 希望请求的天数, 得到请求多少天前的数据
    day_ago = 2 + 8 + want_show_count
    return lcn_time.before_today(day_ago)


def cal_my_fund_profit_situation(fund_base_data, request_show_count=3):
    fund_data_in_network = get_fund_data(fund_base_data.fund_code, request_start_day_cal(request_show_count),
                                         lcn_time.today(), request_show_count)

    print(fund_data_in_network.to_string(index=False))
