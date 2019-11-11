import flask
from gevent import monkey, pywsgi

import tail
import tool

monkey.patch_all()

app = flask.Flask(__name__, static_folder="static")


# app.debug = True


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


@app.route('/')
def tail_html():
    return flask.send_file("static/tail.html")


if __name__ == "__main__":
    # app.run(host="localhost", port=8003,debug=True)
    print("server run ...")
    server = pywsgi.WSGIServer(("localhost", 8003), app)
    server.serve_forever()
