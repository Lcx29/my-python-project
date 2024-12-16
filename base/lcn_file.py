import os


def user_base_path():
    # 获取用户的主目录
    return os.path.expanduser('~')


def current_path():
    # 获取当前所在的目录
    # return os.path.dirname(os.path.abspath(__file__))
    return os.getcwd()


def current_path_file(file_name):
    # 获取当前目录的文件
    return os.path.join(current_path(), file_name)


def user_path(other_path, file_name):
    if other_path is None or other_path == "":
        return os.path.join(user_base_path(), file_name)
    # 获取用户的文件目录
    return os.path.join(user_base_path(), other_path, file_name)
