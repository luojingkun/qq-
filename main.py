import json
import time
import threading
import requests
from napcat import NapCat

# 开发者信息
DEVELOPER = "灵烁"
EMAIL = "lingshuo070330@163.com"

# 配置路径
CONFIG_PATH = "config.json"

# 默认配置
config = {
    "bot_qq": "",
    "napcat_ws": "ws://127.0.0.1:3001",
    "check_urls": [],
    "admin_qq": [],
    "command": "状态"
}

def load_config():
    global config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        save_config()

def save_config():
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def check_website(url):
    try:
        start_time = time.time()
        res = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"},
            allow_redirects=True
        )
        delay = round((time.time() - start_time) * 1000, 2)
        if res.status_code == 200:
            return f"✅ 正常 | 响应：{delay}ms"
        else:
            return f"⚠️ 异常 | 状态码：{res.status_code}"
    except Exception:
        return "❌ 无法连接"

def run_bot():
    load_config()
    bot = NapCat(
        qq=int(config["bot_qq"]),
        ws_url=config["napcat_ws"]
    )

    @bot.on_message()
    def handle_msg(ctx):
        msg = ctx.message.strip()
        if msg == config["command"]:
            if not config["check_urls"]:
                ctx.reply("未配置检测网址，请前往后台管理")
                return
            
            reply = "📊 网站状态检测报告\n"
            reply += "=" * 28 + "\n"
            for i, url in enumerate(config["check_urls"], 1):
                status = check_website(url)
                reply += f"{i}. {url}\n{status}\n\n"
            reply += f"🤖 开发者：{DEVELOPER}"
            ctx.reply(reply)

    bot.run()

def run_web_server():
    from web_server import start_server
    start_server()

if __name__ == "__main__":
    load_config()
    threading.Thread(target=run_web_server, daemon=True).start()
    run_bot()
