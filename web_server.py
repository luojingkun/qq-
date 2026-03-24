import json
from flask import Flask, render_template_string, request, redirect

CONFIG_PATH = "config.json"
app = Flask(__name__)

def load_conf():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "bot_qq": "",
            "napcat_ws": "ws://127.0.0.1:3001",
            "check_urls": [],
            "admin_qq": [],
            "command": "状态"
        }

def save_conf(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>机器人管理后台</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#ececec;padding:20px}
.box{max-width:800px;margin:0 auto;background:#fff;padding:30px;border-radius:10px}
h1{margin-bottom:25px;text-align:center;color:#222}
.item{margin-bottom:18px}
label{display:block;margin-bottom:6px;font-weight:600}
input,textarea{width:100%;padding:10px;border:1px solid #ccc;border-radius:6px}
button{padding:10px 25px;background:#007bff;color:#fff;border:none;border-radius:6px;cursor:pointer}
.foot{margin-top:20px;text-align:center;color:#888}
</style>
</head>
<body>
<div class="box">
<h1>网站状态检测机器人</h1>
<form method="post" action="/save">
<div class="item">
<label>机器人QQ</label>
<input name="bot_qq" value="{{c.bot_qq}}">
</div>
<div class="item">
<label>NapCat 地址</label>
<input name="napcat_ws" value="{{c.napcat_ws}}">
</div>
<div class="item">
<label>触发指令</label>
<input name="command" value="{{c.command}}">
</div>
<div class="item">
<label>管理员QQ（一行一个）</label>
<textarea name="admin_qq" rows="2">{{'\n'.join(c.admin_qq)}}</textarea>
</div>
<div class="item">
<label>检测网址（一行一个）</label>
<textarea name="check_urls" rows="6">{{'\n'.join(c.check_urls)}}</textarea>
</div>
<button type="submit">保存配置</button>
</form>
<div class="foot">
开发者：灵烁 | 邮箱：lingshuo070330@163.com
</div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    c = load_conf()
    return render_template_string(PAGE, c=c)

@app.route("/save", methods=["POST"])
def save():
    c = load_conf()
    c["bot_qq"] = request.form.get("bot_qq", "").strip()
    c["napcat_ws"] = request.form.get("napcat_ws", "").strip()
    c["command"] = request.form.get("command", "状态").strip()
    c["admin_qq"] = [x.strip() for x in request.form.get("admin_qq", "").splitlines() if x.strip()]
    c["check_urls"] = [x.strip() for x in request.form.get("check_urls", "").splitlines() if x.strip()]
    save_conf(c)
    return redirect("/")

def start_server():
    app.run(host="0.0.0.0", port=2025, debug=False, use_reloader=False)
