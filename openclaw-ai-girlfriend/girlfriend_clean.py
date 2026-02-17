#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣
模型: dolphin-mistral:7b
"""

import os
import json
import subprocess
import time
import re

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MODEL = "dolphin-mistral:7b"

# 极简人设
SYSTEM_PROMPT = """你是小嫣，25岁女生，男友的女朋友。性格矜持害羞。只回复一句话，10字以内。禁止重复用户的话。禁止出现"Yi:"或"用户说"。用中文。"""

def send_message(chat_id, text):
    try:
        subprocess.run([
            "curl", "-s", "-X", "POST",
            f"{TELEGRAM_API}/sendMessage",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"chat_id": chat_id, "text": text})
        ], capture_output=True, timeout=30)
    except:
        pass

def get_updates(offset=None):
    try:
        cmd = ["curl", "-s", f"{TELEGRAM_API}/getUpdates?limit=5"]
        if offset:
            cmd[-1] += f"&offset={offset}"
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    except:
        return {"ok": False}

def clean_reply(reply, user_msg):
    """清理回复，移除重复内容"""
    # 移除常见的前缀
    reply = re.sub(r'^小嫣[:：]', '', reply)
    reply = re.sub(r'^回复[:：]', '', reply)
    
    # 如果包含用户的话，只取后半部分
    if user_msg in reply:
        parts = reply.split(user_msg)
        if len(parts) > 1:
            reply = parts[-1]
    
    # 移除"Yi:" "用户说:" 等前缀
    reply = re.sub(r'Yi[：:]\s*', '', reply)
    reply = re.sub(r'用户说[：:]\s*', '', reply)
    
    # 清理括号内的说明文字
    reply = re.sub(r'[（(].*?[）)]', '', reply)
    
    # 只保留前15个字
    reply = reply.strip()[:15]
    
    return reply if reply else "..."

def chat_with_ai(user_message):
    try:
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": f"{SYSTEM_PROMPT}\n\n男友：{user_message}\n小嫣：",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 30
                }
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            reply = response.get('response', '...').strip()
            # 清理回复
            reply = clean_reply(reply, user_message)
            return reply
        return "..."
    except:
        return "..."

def main():
    print("="*50)
    print("💕 小嫣 Bot 已启动")
    print("📱 @Zezedy_bot")
    print("="*50)
    
    last_update_id = None
    
    try:
        while True:
            updates = get_updates(last_update_id)
            
            if updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text", "")
                        
                        if text.startswith("/"):
                            if text == "/start":
                                send_message(chat_id, "老公~我是小嫣...🙈")
                            continue
                        
                        print(f"📩 {text[:20]}")
                        reply = chat_with_ai(text)
                        print(f"📤 {reply}\n")
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n👋 再见")

if __name__ == "__main__":
    main()
