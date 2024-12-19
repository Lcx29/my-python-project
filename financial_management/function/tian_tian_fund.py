from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from financial_management.lcn_base_class import AssetNetworkResponse


def request_fund_data_from_api(
        fund_code: str,
        start_date: str,
        end_date: str,
        data_type: str = "lsjz",
        page: int = 1,
        per: int = 20
) -> Optional[requests.Response]:
    """
    从东方财富 API 获取基金数据。

    此函数使用东方财富的 API 检索指定基金在指定日期范围内的数据。
    它支持分页，并允许选择要检索的数据类型。

    Args:
        fund_code (str): 要检索数据的基金代码 (例如: "005905")。
        start_date (str): 数据检索的开始日期，格式为 YYYY-MM-DD。
        end_date (str): 数据检索的结束日期，格式为 YYYY-MM-DD。
        data_type (str, 可选): 要检索的数据类型。默认为 "lsjz" (可能是历史净值数据), 其他数据类型可能根据 API 的不同而有所不同。
        page (int, 可选): 分页的页码 (适用于大型数据集)。默认为 1。
        per (int, 可选): 每页的记录数。默认为 20。

    Returns:
        Optional[requests.Response]: 如果成功，则返回包含基金数据的 requests.Response 对象，否则返回 None。

    Raises:
        requests.RequestException: 用于一般的网络或请求错误。
    """

    url = (f"http://fund.eastmoney.com/f10/F10DataApi.aspx?"
           f"type={data_type}&code={fund_code}&page={page}&sdate={start_date}&edate={end_date}&per={per}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36'
    }

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        response.encoding = "utf-8"
        return response
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def parse_fund_data_from_html_response(html_response: Optional[requests.Response]) -> List[AssetNetworkResponse]:
    """
    解析包含资产净值信息的 HTML 响应。

    该函数从 HTML 响应中提取表格数据，并将其转换为 AssetNetworkResponse 对象列表。
    它使用 BeautifulSoup 解析 HTML，查找 <tr> (表格行) 和 <td> (表格单元格) 标签。

    Args:
        html_response (requests.Response): 包含 HTML 内容的 requests 响应对象。

    Returns:
        List[AssetNetworkResponse]: AssetNetworkResponse 对象列表，包含解析后的资产净值数据。
        如果 HTML 响应无效或解析过程中发生错误，则返回一个空列表。
    """

    if not html_response or not html_response.text:
        return []

    soup = BeautifulSoup(html_response.text, 'html.parser')
    table_rows = soup.find_all("tr")
    responses: List[AssetNetworkResponse] = []

    for row in table_rows[1:]:
        try:
            columns = row.find_all("td")
            if len(columns) < 2:
                continue  # Skip rows with insufficient data

            date = columns[0].text.strip()
            net_asset_value = float(columns[1].text.strip())
            responses.append(AssetNetworkResponse(
                date=date,
                net_asset_value=net_asset_value
            ))
        except (IndexError, ValueError) as e:
            print(f"Error parsing row: {row}, {e}")
    return responses


def fetch_fund_data(fund_code: str, show_count: int, start_date: str, end_date: str) -> List[AssetNetworkResponse]:
    """
    请求并解析基金数据。

    Args:
        fund_code: 基金代码。
        show_count: 需要获取的数据点数量。
        start_date: 数据范围的开始日期。
        end_date: 数据范围的结束日期。

    Returns:
        AssetNetworkResponse 对象的列表。
    """
    need_page_num = 1
    response = request_fund_data_from_api(fund_code, start_date, end_date, "lsjz", need_page_num, show_count)
    return parse_fund_data_from_html_response(response)
