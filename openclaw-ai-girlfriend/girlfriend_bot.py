#!/usr/bin/env python3
"""
AI Girlfriend - Telegram Bot 完整版
连接 Ollama 本地模型 + Telegram Bot
"""

import os
import sys
import time
import requests

# 配置
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    """发送消息到 Telegram"""
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", 
                     json={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"发送消息失败: {e}")

def get_updates(offset=None):
    """获取最新消息"""
    try:
        params = {"offset": offset, "limit": 10}
        response = requests.get(f"{TELEGRAM_API}/getUpdates", params=params)
        return response.json()
    except Exception as e:
        print(f"获取消息失败: {e}")
        return {"ok": False}

def chat_with_ai(user_message, user_name="用户"):
    """和 Ollama AI 对话"""
    try:
        # 构建提示词 - 设定为温柔女友角色
        prompt = f"""你是一个温柔体贴的虚拟女友。用户名叫{user_name}。
请用中文简短回复（2-3句话），语气亲切可爱。

用户说: {user_message}

你的回复:"""
        
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,  # 创造性
                "num_predict": 100   # 限制回复长度
            }
        }, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '抱歉，我没听清楚...').strip()
        else:
            return f"抱歉，我现在有点混乱 (错误码: {response.status_code})"
            
    except Exception as e:
        print(f"AI 对话错误: {e}")
        return "抱歉，我卡住了，请稍后再试..."

def main():
    print("="*60)
    print("💕 AI Girlfriend Bot 已启动!")
    print("="*60)
    print(f"🤖 模型: {MODEL}")
    print(f"📱 Bot: @Zezedy_bot")
    print("\n提示: 在 Telegram 上给 @Zezedy_bot 发消息开始聊天")
    print("按 Ctrl+C 停止\n")
    
    last_update_id = None
    message_count = 0
    
    try:
        while True:
            updates = get_updates(last_update_id)
            
            if updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        user_name = msg["from"].get("first_name", "用户")
                        text = msg.get("text", "")
                        
                        print(f"📩 [{user_name}]: {text}")
                        
                        # 跳过命令
                        if text.startswith("/"):
                            if text == "/start":
                                send_message(chat_id, f"你好 {user_name}! 我是你的 AI 女友 😊\n\n想聊点什么?")
                            continue
                        
                        # AI 回复
                        print("🧠 AI 思考中...")
                        reply = chat_with_ai(text, user_name)
                        
                        send_message(chat_id, reply)
                        print(f"📤 AI: {reply[:50]}...\n")
                        
                        message_count += 1
            
            time.sleep(2)  # 每2秒检查一次
            
    except KeyboardInterrupt:
        print(f"\n\n👋 已停止，共处理了 {message_count} 条消息")
        print("再见!")

if __name__ == "__main__":
    main()
