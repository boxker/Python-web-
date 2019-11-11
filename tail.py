import re

import paramiko as pm


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





if __name__ == "__main__":
    tf, ssh = get_ssh("10.112.98.159", "root", "222")
    if tf is True:
        print(tail_one(ssh, "/root/logs"))

