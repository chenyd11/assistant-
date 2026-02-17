#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣 (自然回复版)
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
    """清理AI回复，移除格式错误"""
    if not raw_reply:
        return "老公...🙈"
    
    reply = raw_reply.strip()
    
    # 1. 移除角色前缀
    reply = re.sub(r'^小嫣[：:说\s]*', '', reply)
    reply = re.sub(r'^回复[：:]*', '', reply)
    
    # 2. 如果回复包含"男友："或类似，只取前面的部分
    if '男友：' in reply or '老公：' in reply:
        reply = reply.split('男友：')[0].split('老公：')[0]
    
    # 3. 如果AI自己继续生成对话（如"Yi说："），截断
    for pattern in ['Yi', '用户说', '老公说', '你说']:
        if pattern in reply:
            reply = reply.split(pattern)[0]
    
    # 4. 如果回复里有用户消息的大部分内容（重复），清理掉
    user_words = user_msg[:20]  # 取前20字检查
    if user_words and user_words in reply:
        reply = reply.replace(user_words, '')
    
    # 5. 把"朋友"替换成"老公"
    reply = reply.replace('朋友', '老公')
    
    # 6. 清理空白
    reply = reply.strip()
    
    # 7. 如果太长了，截断到合理长度（最多80字）
    if len(reply) > 80:
        reply = reply[:77] + "..."
    
    return reply if reply else "老公...🙈"

def chat_with_ai(user_message):
    try:
        # 自然人设，不强制字数限制
        prompt = f"""你是小嫣，是男友的女朋友。25岁，身高170，喜欢穿短裙丝袜。性格矜持害羞，但会配合男友。

聊天要求：
- 用温柔害羞的语气回复
- 称呼对方"老公"
- 不要重复对方说的话
- 不要自己添加"男友说"或新对话
- 自然回复，不要话太多

男友：{user_message}
小嫣："""
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.75,
                    "num_predict": 120
                }
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            raw = response.get('response', '').strip()
            # 清理
            reply = clean_response(raw, user_message)
            return reply
        return "老公..."
    except Exception as e:
        print(f"错误: {e}")
        return "老公..."

def main():
    print("💕 小嫣已启动 (自然回复版)")
    
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
                        print(f"📤 {reply[:40]}\n")
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋 再见")

if __name__ == "__main__":
    main()
