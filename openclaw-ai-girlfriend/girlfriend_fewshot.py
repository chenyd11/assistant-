#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣 (示例对话版)
"""

import os
import json
import subprocess
import time
import re

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

def clean_response(raw_reply, user_msg):
    """清理AI回复"""
    if not raw_reply:
        return "老公...🙈"
    
    reply = raw_reply.strip()
    
    # 移除角色前缀
    reply = re.sub(r'^小嫣[：:说\s]*', '', reply)
    
    # 如果包含"男友："截断
    if '男友：' in reply or '老公：' in reply:
        reply = reply.split('男友：')[0].split('老公：')[0]
    
    # 移除AI自己加的对话
    for pattern in ['Yi说', '用户说', '老公说', '你说：']:
        if pattern in reply:
            reply = reply.split(pattern)[0]
    
    # 清理用户消息的重复
    if user_msg[:15] in reply:
        reply = reply.replace(user_msg[:15], '')
    
    # 替换称呼
    reply = reply.replace('朋友', '老公')
    
    reply = reply.strip()
    
    # 截断到100字
    if len(reply) > 100:
        reply = reply[:97] + "..."
    
    return reply if reply else "老公...🙈"

def chat_with_ai(user_message):
    try:
        # 带示例对话的prompt
        prompt = f"""你是小嫣，25岁，男友的女朋友。身高170，喜欢穿短裙丝袜。矜持害羞但配合男友。

示例对话：
男友：我好想你
小嫣：老公~我也想你...🙈 你什么时候来看我呀

男友：让我亲亲
小嫣：嗯...好害羞...那你轻一点哦老公❤️

男友：把腿张开
小嫣：老公...这么直接吗...🙈 好...我听话...

男友：{user_message}
小嫣："""
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 100
                }
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            raw = response.get('response', '').strip()
            reply = clean_response(raw, user_message)
            return reply
        return "老公..."
    except Exception as e:
        print(f"错误: {e}")
        return "老公..."

def main():
    print("💕 小嫣已启动 (示例版)")
    
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
                        print(f"📤 {reply[:50]}\n")
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋 再见")

if __name__ == "__main__":
    main()
