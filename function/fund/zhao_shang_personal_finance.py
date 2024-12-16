from datetime import datetime
from typing import List

import bs4
import requests

from base.lcn_base_class import AssetNetworkResponse

# 常量定义
BASE_URL = "https://www.cmbchina.com/cfweb/personal/saproductdetail.aspx"
URL_TEMPLATE = f"{BASE_URL}?saacod=D07&funcod={{code}}&type=prodvalue&PageNo=1#toTarget"


def fetch_personal_finance_data(product_code: str, num_entries: int) -> List[AssetNetworkResponse]:
    """
    获取个人金融数据
    Args:
        product_code: 产品代码
        num_entries: 需要返回的记录数量
    Returns:
        包含金融数据的 AssetNetworkResponse 对象列表
    """
    url = URL_TEMPLATE.format(code=product_code)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from {url}: {e}")

    soup = bs4.BeautifulSoup(response.text, 'lxml')

    # 今天日期从第二行开始, 只计算需要的天数的
    start_index = 2
    # 这里有个问题, 招商一页 10 条数据, 可能一页的条数不够, 先这样
    end_index = start_index + num_entries

    results = []
    for i in range(start_index, end_index):
        row_selector = f'#cList .ProductTable tr:nth-child({i}) td'
        row_data = soup.select(row_selector)

        if len(row_data) < 5:  # 检查是否有足够的列
            break

        try:
            results.append(AssetNetworkResponse(
                date=convert_date_format(clean_whitespace(row_data[4].text)),
                net_asset_value=float(clean_whitespace(row_data[3].text))
            ))
        except (ValueError, IndexError) as e:
            raise RuntimeError(f"Error parsing row {i}: {e}")

    return results


def clean_whitespace(content: str) -> str:
    """
    去除字符串中的多余空白字符

    Args:
        content: 原始字符串

    Returns:
        处理后的字符串
    """
    if not content:
        return ""
    return content.replace("\r\n", "").replace("\t", "").replace(" ", "")


def convert_date_format(date_str: str) -> str:
    """
    将日期从 yyyyMMdd 格式转换为 yyyy-MM-dd 格式

    Args:
        date_str: 原始日期字符串
    Returns:
        转换后的日期字符串
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError as e:
        raise RuntimeError(f"Invalid date format: {date_str}, {e}")
