#!/usr/bin/env python3
"""
AI Girlfriend Bot - 小嫣 (增强记忆版)
短期记忆(5轮详细) + 中期记忆(自动摘要)
"""

import os
import json
import subprocess
import time
import re
from collections import deque

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MODEL = "qwen:7b"

# 存储结构: {chat_id: {'short': deque(5轮), 'summary': str}}
user_memories = {}

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
    
    for pattern in ['男友：', '老公：', 'Yi说', '用户说', '你说：', 'Summary:']:
        if pattern in reply:
            reply = reply.split(pattern)[0]
    
    reply = reply.replace('朋友', '老公').strip()
    
    if len(reply) > 100:
        reply = reply[:97] + "..."
    
    return reply if reply else "老公...🙈"

def generate_summary(chat_history):
    """生成对话摘要"""
    if len(chat_history) < 3:
        return ""
    
    try:
        # 构建需要摘要的内容
        content = ""
        for msg in chat_history:
            content += f"男友：{msg['user']}\n小嫣：{msg['ai']}\n"
        
        prompt = f"""总结以下对话的主题和情感氛围，用1-2句话：

{content}

Summary:"""
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 50
                }
            })
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            summary = response.get('response', '').strip()
            return clean_response(summary)
    except:
        pass
    
    return ""

def chat_with_ai(user_message, short_memory, summary):
    """带分层记忆的对话"""
    try:
        # 只构建纯对话历史，不加任何指令标记
        history_lines = []
        
        if short_memory:
            for msg in short_memory[-3:]:  # 只取最近3轮，避免太长
                history_lines.append(f"男友：{msg['user']}")
                history_lines.append(f"小嫣：{msg['ai']}")
        
        history = "\n".join(history_lines)
        
        # 只保留最近1轮历史，避免模型混乱
        if short_memory and len(short_memory) > 0:
            last = short_memory[-1]
            prompt = f"你是小嫣，男友的害羞女友。\n\n上次：男友说\"{last['user']}\"，你回答\"{last['ai']}\"\n\n现在男友说：{user_message}\n你回答："
        else:
            prompt = f"你是小嫣，男友的害羞女友。\n\n男友说：{user_message}\n你回答："
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 80
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
    print("💕 小嫣已启动 (增强记忆版)")
    print("📝 短期5轮 + 自动摘要\n")
    
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
                                user_memories[chat_id] = {
                                    'short': deque(maxlen=5),
                                    'summary': ""
                                }
                            continue
                        
                        # 获取或创建记忆
                        if chat_id not in user_memories:
                            user_memories[chat_id] = {
                                'short': deque(maxlen=5),
                                'summary': ""
                            }
                        
                        memory = user_memories[chat_id]
                        short_list = list(memory['short'])
                        
                        print(f"📩 {text[:20]}")
                        print(f"   短期记忆: {len(short_list)}轮")
                        print(f"   摘要: {memory['summary'][:30] if memory['summary'] else '无'}...")
                        
                        # 生成回复
                        reply = chat_with_ai(text, short_list, memory['summary'])
                        print(f"📤 {reply[:50]}\n")
                        
                        # 保存到短期记忆
                        memory['short'].append({
                            'user': text,
                            'ai': reply
                        })
                        
                        # 每满5轮，生成摘要
                        if len(memory['short']) == 5 and not memory['summary']:
                            print("📝 生成对话摘要...")
                            new_summary = generate_summary(list(memory['short']))
                            if new_summary:
                                memory['summary'] = new_summary
                                print(f"   摘要: {new_summary}\n")
                        
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋 再见")

if __name__ == "__main__":
    main()
