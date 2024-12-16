from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from base.lcn_base_class import AssetNetworkResponse


def request_fund_data_from_api(
        fund_code: str,
        start_date: str,
        end_date: str,
        data_type: str = "lsjz",
        page: int = 1,
        per: int = 20
) -> Optional[requests.Response]:
    """
    Requests fund data from the specified API endpoint.

    Args:
        fund_code: The fund code.
        start_date: The start date of the data range.
        end_date: The end date of the data range.
        data_type: The type of data to request (default: "lsjz").
        page: The page number of the results (default: 1).
        per: The number of results per page (default: 20).

    Returns:
        The HTTP response object, or None if the request fails.
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
    Parses fund data from the given HTML response.

    Args:
        html_response: The HTTP response object.

    Returns:
        A list of AssetNetworkResponse objects.
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
    Requests and parses fund data.

    Args:
        fund_code: The fund code.
        show_count: The number of data points to retrieve.
        start_date: The start date of the data range.
        end_date: The end date of the data range.

    Returns:
        A list of AssetNetworkResponse objects.
    """
    need_page_num = 1
    response = request_fund_data_from_api(fund_code, start_date, end_date, "lsjz", need_page_num, show_count)
    return parse_fund_data_from_html_response(response)
