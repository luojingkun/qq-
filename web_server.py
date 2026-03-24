import json
import threading
from flask import Flask, render_template_string, request, redirect, url_for

# 配置文件路径
CONFIG_PATH = "config.json"
app = Flask(__name__)

def load_config():
    """加载配置"""
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

def save_config(data):
    """保存配置"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 后台页面模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>网站状态检测机器人 - 后台管理</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:微软雅黑;}
        body{background:#f5f5f5;padding:20px;}
        .container{max-width:900px;margin:0 auto;background:white;padding:30px;border-radius:10px;box-shadow:0 0 10px rgba(0,0,0,0.1);}
        h1{text-align:center;color:#333;margin-bottom:30px;}
        .form-item{margin-bottom:20px;}
        label{display:block;margin-bottom:8px;color:#555;font-weight:bold;}
        input,textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:5px;font-size:16px;}
        button{background:#409eff;color:white;padding:12px 30px;border:none;border-radius:5px;font-size:16px;cursor:pointer;}
        button:hover{background:#337ecc;}
        .dev{text-align:center;margin-top:20px;color:#999;}
    </style>
</head>
<body>
    <div class="container">
        <h1>机器人后台管理</h1>
        <form action="/save" method="post">
            <div class="form-item">
                <label>机器人QQ号</label>
                <input type="text" name="bot_qq" value="{{config.bot_qq}}">
            </div>
            <div class="form-item">
                <label>NapCat WS地址</label>
                <input type="text" name="napcat_ws" value="{{config.napcat_ws}}">
            </div>
            <div class="form-item">
                <label>检测指令</label>
                <input type="text" name="command" value="{{config.command}}">
            </div>
            <div class="form-item">
                <label>管理员QQ（一行一个）</label>
                <textarea name="admin_qq" rows="3">{{'\n'.join(config.admin_qq)}}</textarea>
            </div>
            <div class="form-item">
                <label>检测网址（一行一个）</label>
                <textarea name="check_urls" rows="5">{{'\n'.join(config.check_urls)}}</textarea>
            </div>
            <button type="submit">保存配置</button>
        </form>
        <div class="dev">
            开发者：灵烁 | 邮箱：lingshuo070330@163.com
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    config = load_config()
    return render_template_string(HTML_TEMPLATE, config=config)

@app.route("/save", methods=["POST"])
def save():
    config = load_config()
    config["bot_qq"] = request.form.get("bot_qq", "")
    config["napcat_ws"] = request.form.get("napcat_ws", "")
    config["command"] = request.form.get("command", "状态")
    
    # 处理多行数据
    config["admin_qq"] = [i.strip() for i in request.form.get("admin_qq", "").split("\n") if i.strip()]
    config["check_urls"] = [i.strip() for i in request.form.get("check_urls", "").split("\n") if i.strip()]
    
    save_config(config)
    return redirect(url_for("index"))

def run_server():
    app.run(host="0.0.0.0", port=2025, debug=False)
