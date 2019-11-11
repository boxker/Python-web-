# Python 简易web日志查看工具&可改装为命令行工具

## 效果图

![](https://img2018.cnblogs.com/blog/1098476/201911/1098476-20191111143716541-1412515442.png)

![](https://img2018.cnblogs.com/blog/1098476/201911/1098476-20191111143717017-1185655442.png)

![](https://img2018.cnblogs.com/blog/1098476/201911/1098476-20191111143717343-73287820.png)

![](https://img2018.cnblogs.com/blog/1098476/201911/1098476-20191111143717676-1668594360.png)

![](https://img2018.cnblogs.com/blog/1098476/201911/1098476-20191111143717998-439192973.png)

## 原理

利用python的paramiko库模拟ssh登录操作，并执行tail命令

## 所需库

flask、paramiko、gevent，python3


## 部分代码

```python
@app.route('/api/do', methods=["POST", "GET"])
def api_do():
    try:
        ip = flask.request.form.get("ip")
        port = flask.request.form.get("port")
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        path = flask.request.form.get("path")
        count = flask.request.form.get("count")
    except:
        return {
            "status": "err",
            "code": "200",
            "error": "params error"
        }
    if ip is None:
        ip = "127.0.0.1"
    if port is None:
        port = 22
    if username is None:
        username = "root"
    if password is None:
        password = "root"
    if path is None:
        path = "/usr/local/logs"
    if count is None:
        count = 100
    if tool.check_ip(ip) is False:
        return {
            "status": "err",
            "code": "202",
            "error": "ip error"
        }
    if tool.check_file(path) is False:
        return {
            "status": "err",
            "code": "203",
            "error": "file path error or forbid"
        }
    tf, ssh = tail.get_ssh(ip, username, password, port=port)
    if tf is False:
        return {
            "status": "err",
            "code": "201",
            "error": "ssh login error"
        }
    res = tail.tail_one(ssh, path, count=count)
    return res
```

```python
def get_ssh(ip, username, password, port=22):
    # 实例化SSHClient
    client = pm.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    try:
        client.connect(hostname=ip, port=port, username=username, password=password)
    except BaseException as e:
        print(e)
        return False, e
    return True, client


def tail_one(ssh, path, count=100):
    # 获取日志信息，传入利用get_ssh生成的client，路径，显示数量
    cmd = "tail -n {count} {path}".format(count=count, path=path)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    err = stderr.read().decode()
    if len(err) != 0:
        return {
            "status": "err",
            "code": "300",
            "error": err
        }
    else:
        return {
            "status": "ok",
            "code": "100",
            "result": stdout.read().decode()
        }

```


```python
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
```

代码详见[Python-webLogSight](https://github.com/boxker/Python-webLogSight.git "Python-webLogSight")
