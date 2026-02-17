#!/usr/bin/env python3
"""
AI Girlfriend Bot - 使用 subprocess 调用 curl (绕过 Python requests 502 问题)
"""

import os
import json
import subprocess
import time

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    """发送消息到 Telegram"""
    try:
        subprocess.run([
            "curl", "-s", "-X", "POST",
            f"{TELEGRAM_API}/sendMessage",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"chat_id": chat_id, "text": text})
        ], capture_output=True, timeout=30)
    except Exception as e:
        print(f"发送失败: {e}")

def get_updates(offset=None):
    """获取最新消息"""
    try:
        cmd = ["curl", "-s", f"{TELEGRAM_API}/getUpdates?limit=5"]
        if offset:
            cmd[-1] += f"&offset={offset}"
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"获取消息失败: {e}")
        return {"ok": False}

def chat_with_ai(user_message):
    """使用 curl 调用 Ollama"""
    try:
        prompt = f"用中文简短回答（2-3句话），语气亲切：{user_message}"
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response.get('response', '抱歉，我没听懂...').strip()
        else:
            return f"AI 错误 (code: {result.returncode})"
            
    except Exception as e:
        return f"出错了: {e}"

def main():
    print("="*60)
    print("💕 AI 女友 Bot 已启动! (使用 curl 模式)")
    print("="*60)
    print("📱 Bot: @Zezedy_bot")
    print("\n请发送消息测试...\n")
    
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
                        user_name = msg["from"].get("first_name", "用户")
                        text = msg.get("text", "")
                        
                        print(f"📩 [{user_name}]: {text}")
                        
                        # AI 回复
                        print("🧠 思考中...")
                        reply = chat_with_ai(text)
                        print(f"📤 回复: {reply[:40]}...\n")
                        
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n👋 再见!")

if __name__ == "__main__":
    main()
