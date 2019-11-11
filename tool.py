import re


def get_ip_port(ip_and_port):
    # 未用到
    ip_port_for = r'^[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}:[0-9]{1,5}$'
    ip_for = r'^[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}.[1-2]?[0-9]{0,2}'
    port_for = r'[0-9]{1,5}$'
    res = re.search(ip_port_for, ip_and_port)
    print(res.span())
    print(res)


def check_ip(ip):
    # 检查ip是否合法
    ip_format = r'^((([1-2][0-9]{2})|([1-9][0-9])|([0-9]))[.]){3}(([1-2][0-9]{2})|([1-9][0-9])|([0-9]))$'
    # ip_format = r'^[1-2]?[0-9]{1,2}.[1-2]?[0-9]{1,2}.[1-2]?[0-9]{1,2}.[1-2]?[0-9]{1,2}$'
    match = re.search(ip_format, ip)
    # print(match)
    if match:
        return match.group()
    else:
        return False


def check_file(path):
    # 检查路径是否合法，限定使用区域，禁止执行其他命令
    path_default = "/usr/local/logs"
    forbid_word = r'&|\||[ ]|`|"|\''
    allow_path = r'/usr/local/'
    match = re.search(forbid_word, path)
    if match:
        return False
    match = re.search(allow_path, path)
    if match:
        return path
    else:
        return False


if __name__ == "__main__":
    get_ip_port("1.1.1.1:8080")
    print(check_ip("27.10.1.1"))
    print(check_file("/usr/local/log/log"))
