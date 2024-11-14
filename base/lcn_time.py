import time
from datetime import datetime, timedelta


def today():
    """
    get today str, format "yyyy-mm-dd"
    """
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def before_today(before_day):
    # 计算前几天的日期
    days_ago = datetime.now() - timedelta(days=before_day)
    return days_ago.strftime('%Y-%m-%d')
