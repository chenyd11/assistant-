#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣 (最终版)
"""

import os
import json
import subprocess
import time

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MODEL = "dolphin-mistral:7b"

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

def chat_with_ai(user_message):
    """AI对话，极简prompt避免重复"""
    try:
        # 极简prompt，只给角色和任务
        prompt = f"""你是小嫣，是男友的害羞女友。说话简短害羞。

规则：
- 只回复1句话，最多8个字
- 不要重复对方的话  
- 称呼对方为"老公"
- 害羞时用...或🙈

男友说：{user_message}
小嫣说："""
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 20
                }
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            reply = response.get('response', '').strip()
            
            # 强力清理
            # 1. 移除所有引号
            reply = reply.replace('"', '').replace("'", "")
            # 2. 如果包含用户消息的前半部分，截断
            for i in range(min(len(user_message), 10), 0, -1):
                if user_message[:i] in reply:
                    reply = reply.replace(user_message[:i], '')
            # 3. 移除"Yi""用户""说"等
            for bad in ['Yi', '用户', '说：', '说:', '：', '小嫣说']:
                reply = reply.replace(bad, '')
            # 4. 如果叫"朋友"改"老公"
            reply = reply.replace('朋友', '老公')
            # 5. 截断到8个字
            reply = reply.strip()[:8]
            
            return reply if reply else "老公...🙈"
        return "老公..."
    except:
        return "老公..."

def main():
    print("💕 小嫣已启动")
    
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
                                send_message(chat_id, "老公~🙈")
                            continue
                        
                        print(f"📩 {text[:15]}")
                        reply = chat_with_ai(text)
                        print(f"📤 {reply}\n")
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋")

if __name__ == "__main__":
    main()
