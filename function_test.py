import sys

import base.lcn_file as lcn_file
import financial_management.integrated_resources as integrated_resources


def get_file_path_from_argv(arg_name: str, default_value: str) -> str:
    """
    获取文件路径

    从命令行参数中获取文件路径，如果没有则返回默认路径

    Returns
        文件路径
    """

    # 第一个参数为脚本的名称
    for index in range(1, len(sys.argv)):
        if sys.argv[index] == arg_name:
            return sys.argv[index + 1]
    return default_value


def test_convert_file_encoding():
    file_path = "/Users/lcn/Downloads/a.txt"
    target_encoding = "utf-8"
    new_file_path = lcn_file.convert_file_encoding(file_path, target_encoding)
    print(new_file_path)


def test_financial_management():
    config_file_path = "my_python_config.json"
    arg_name = "--lcn_file"

    config_file_path = get_file_path_from_argv(arg_name, config_file_path)

    # 理财管理
    integrated_resources.start_handle(config_file_path)


if __name__ == '__main__':
    # 测试转换文件编码
    # test_convert_file_encoding()

    # 测试理财管理
    test_financial_management()
