import requests
import time

# 存储已出现过的评论，用于去重
seen_comments = set()
url = "https://apphwshhq.longhuvip.com/w1/api/index.php?PhoneOSNew=2&VerSion=5.19.0.3&a=ZhiBoContent&apiv=w40&c=ConceptionPoint"

def fetch_new_comments():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        data = response.json()
        if 'List' not in data:
            print("响应中未找到 'List' 字段")
            return
        
        new_comments = []
        for item in data['List']:
            comment = item.get('Comment', '')
            if comment and comment not in seen_comments:
                new_comments.append(comment)
                seen_comments.add(comment)
        
        # 输出新评论（从旧到新）
        for comment in new_comments:
            print(comment)
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except ValueError:
        print("响应不是有效的JSON格式")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    print("开始监控评论更新... (Ctrl+C 停止)")
    try:
        while True:
            fetch_new_comments()
            time.sleep(5)  # 每5秒检查一次更新
    except KeyboardInterrupt:
        print("\n程序已停止")