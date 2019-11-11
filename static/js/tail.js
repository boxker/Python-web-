$(document).ready(function () {
    let cont_tpl = null;
    let cont_err_tpl = null;
    $.get("static/ejs/more.ejs", function (data) {
        var html = ejs.render(data);
        // console.log(html);
        $("#top").html(html);
        $("#btn").click(btn);
    });
    $.get("static/ejs/content.ejs", function (data) {
        cont_tpl = data;
    });
    $.get("static/ejs/content_err.ejs", function (data) {
        cont_err_tpl = data;
    });

    function btn() {
        $("#content").html("");
        let user = $("#user").val();
        let pwd = $("#pwd").val();
        let ips = $("#ips").val();
        let path = $("#path").val();
        let count = $("#count").val();
        ipList = ips.split("\n")
        // console.log(ipList);
        for (var index in ipList) {
            let ip = ipList[index]
            $.post(
                "api/do",
                {
                    username: user,
                    password: pwd,
                    ip: ip,
                    path: "/usr/local/" + path,
                    count: count,
                    port: 22,
                },
                function (data) {
                    console.log(data);
                    if (data["status"] == "ok") {
                        new_data = {
                            ip: ip,
                            path: "/usr/local/" + path,
                            cont: data["result"],
                        };
                        let html = ejs.render(cont_tpl, {data: new_data});
                        $("#content").append(html);
                    } else {
                        new_data = {
                            ip: ip,
                            path: "/usr/local/" + path,
                            cont: data["error"],
                        };
                        let html = ejs.render(cont_err_tpl, {data: new_data});
                        $("#content").append(html);
                    }
                }
            );
        }

    }
});