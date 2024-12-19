import time
from datetime import datetime, timedelta


def today():
    """
    获取今天日期

    Returns:
        yyyy-mm-dd 格式的字符串
    """
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def before_today(before_day):
    """
    获取距离今天多少天前的日期

    Args:
        before_day: 天数

    Returns:
        距离今天多少天前的日期, yyyy-mm-dd 格式的字符串
    """
    days_ago = datetime.now() - timedelta(days=before_day)
    return days_ago.strftime('%Y-%m-%d')
