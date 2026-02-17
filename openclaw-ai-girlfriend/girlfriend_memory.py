#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣 (带对话记忆版)
"""

import os
import json
import subprocess
import time
import re
from collections import deque

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MODEL = "dolphin-mistral:7b"

# 存储每个用户的对话历史
user_chats = {}

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

def clean_response(raw_reply):
    """清理AI回复"""
    if not raw_reply:
        return "老公...🙈"
    
    reply = raw_reply.strip()
    reply = re.sub(r'^小嫣[：:说\s]*', '', reply)
    
    # 截断到新对话开始
    for pattern in ['男友：', '老公：', 'Yi说', '用户说', '你说：']:
        if pattern in reply:
            reply = reply.split(pattern)[0]
    
    reply = reply.replace('朋友', '老公').strip()
    
    if len(reply) > 100:
        reply = reply[:97] + "..."
    
    return reply if reply else "老公...🙈"

def chat_with_ai(user_message, chat_history):
    """带上下文的对话"""
    try:
        # 构建带上下文的prompt
        context = ""
        for msg in chat_history:
            context += f"男友：{msg['user']}\n小嫣：{msg['ai']}\n"
        
        prompt = f"""你是小嫣，25岁，男友的女朋友。矜持害羞但配合男友。

对话历史：
{context}

现在：
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
            return clean_response(raw)
        return "老公..."
    except Exception as e:
        print(f"错误: {e}")
        return "老公..."

def main():
    print("💕 小嫣已启动 (带记忆版)")
    print("📝 记住最近10轮对话\n")
    
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
                                user_chats[chat_id] = deque(maxlen=10)
                            continue
                        
                        # 获取或创建对话历史
                        if chat_id not in user_chats:
                            user_chats[chat_id] = deque(maxlen=10)
                        
                        history = list(user_chats[chat_id])
                        
                        print(f"📩 {text[:20]}")
                        print(f"   历史: {len(history)}轮")
                        
                        reply = chat_with_ai(text, history)
                        print(f"📤 {reply[:50]}\n")
                        
                        # 保存到历史
                        user_chats[chat_id].append({
                            'user': text,
                            'ai': reply
                        })
                        
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋 再见")

if __name__ == "__main__":
    main()
