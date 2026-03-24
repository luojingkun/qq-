import json
import time
import threading
import requests
from napcat import NapCat

# 开发者信息
DEVELOPER = "灵烁"
EMAIL = "lingshuo070330@163.com"

# 配置文件路径
CONFIG_PATH = "config.json"

# 全局配置变量
config = {
    "bot_qq": "",
    "napcat_ws": "ws://127.0.0.1:3001",
    "check_urls": [],
    "admin_qq": [],
    "command": "状态"
}

def load_config():
    """加载配置文件"""
    global config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except:
        save_config()

def save_config():
    """保存配置文件"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def check_website(url):
    """检测网站状态"""
    try:
        start_time = time.time()
        res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        res_time = round((time.time() - start_time) * 1000, 2)
        
        if res.status_code == 200:
            return f"✅ 在线\n响应时间：{res_time}ms"
        else:
            return f"⚠️ 异常\n状态码：{res.status_code}"
    except:
        return "❌ 无法访问"

def run_bot():
    """运行机器人"""
    load_config()
    bot = NapCat(
        qq=int(config["bot_qq"]),
        ws_url=config["napcat_ws"]
    )

    @bot.on_message()
    def handle_msg(ctx):
        """消息处理"""
        msg = ctx.message.strip()
        sender = ctx.user_id

        # 状态检测指令
        if msg == config["command"]:
            if not config["check_urls"]:
                ctx.reply("未配置任何检测网址，请前往后台添加")
                return
            
            reply_text = "📊 网站状态检测结果\n"
            reply_text += "="*30 + "\n"
            for idx, url in enumerate(config["check_urls"], 1):
                status = check_website(url)
                reply_text += f"{idx}. {url}\n{status}\n\n"
            
            reply_text += f"🤖 开发者：{DEVELOPER}"
            ctx.reply(reply_text)

    bot.run()

def start_background():
    """后台线程启动"""
    from web_server import run_server
    run_server()

if __name__ == "__main__":
    load_config()
    # 启动后台线程
    threading.Thread(target=start_background, daemon=True).start()
    # 启动机器人
    run_bot()
