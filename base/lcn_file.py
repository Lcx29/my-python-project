import os
import codecs
import chardet
from typing import Any


def convert_file_encoding(file_path: str, target_encoding: str) -> Any:
    """
    转换文件编码并将结果保存到新文件

    Args:
        file_path: 源文件路径
        target_encoding: 目标编码

    Returns:
        新文件的路径，如果转换失败则返回 None
    """
    try:
        original_encoding = detect_encoding(file_path)["encoding"]

        # 构建新文件名
        base_name, ext = os.path.splitext(file_path)
        new_file_path = f"{base_name}_converted{ext}"

        # 使用 codecs 模块以处理各种编码
        with codecs.open(file_path, 'r', encoding=original_encoding, errors='replace') as source_file:
            try:
                content = source_file.read()
            except UnicodeDecodeError as e:
                print(f"解码错误：{e}")
                return None

        with codecs.open(new_file_path, 'w', encoding=target_encoding) as target_file:
            target_file.write(content)

        return new_file_path
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None
    except Exception as e:  # 捕获其他可能出现的异常
        print(f"转换过程中发生错误：{e}")
        return None


def detect_encoding(file_path: str) -> Any:
    """
    检测文件编码

    Args:
        file_path: 文件路径

    Returns:
        检测到的编码信息字典，如果发生错误则返回 None
    """
    try:
        with open(file_path, 'rb') as f:  # 以二进制模式读取文件
            rawdata = f.read()
            result = chardet.detect(rawdata)
            return result
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None
    except Exception as e:
        print(f"检测编码时发生错误：{e}")
        return None
