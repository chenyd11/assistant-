#!/usr/bin/env python3
"""
Telegram Bot 简单测试脚本
不需要完整模型，仅测试 Bot 连接和消息收发
"""

import os
import sys
import time
import requests

# 读取环境变量
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_bot_info():
    """获取 Bot 信息"""
    response = requests.get(f"{API_URL}/getMe")
    return response.json()

def get_updates(offset=None):
    """获取最新消息"""
    params = {"offset": offset, "limit": 10}
    response = requests.get(f"{API_URL}/getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    """发送消息"""
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(f"{API_URL}/sendMessage", json=payload)
    return response.json()

def main():
    print("="*50)
    print("🤖 Telegram Bot 连接测试")
    print("="*50)
    
    # 测试 1: 获取 Bot 信息
    print("\n✅ 测试 1: 获取 Bot 信息")
    info = get_bot_info()
    if info.get("ok"):
        result = info["result"]
        print(f"   Bot 名称: {result['first_name']}")
        print(f"   用户名: @{result['username']}")
        print(f"   Bot ID: {result['id']}")
    else:
        print(f"   ❌ 错误: {info}")
        return
    
    # 测试 2: 检查最新消息
    print("\n✅ 测试 2: 检查最新消息")
    print("   正在监听消息 (按 Ctrl+C 停止)...")
    print("   请在你的 Telegram 上给 @Zezedy_bot 发一条消息!\n")
    
    last_update_id = None
    message_count = 0
    
    try:
        while message_count < 3:  # 测试接收3条消息
            updates = get_updates(last_update_id)
            
            if updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        user_name = msg["from"].get("first_name", "用户")
                        text = msg.get("text", "")
                        
                        print(f"   📩 收到消息来自 {user_name}: {text}")
                        
                        # 回复消息
                        reply = f"你好 {user_name}! 我收到了你的消息: '{text}'\n\n(这是测试回复，模型还在下载中 😊)"
                        send_message(chat_id, reply)
                        print(f"   📤 已回复\n")
                        
                        message_count += 1
                        
                        if message_count >= 3:
                            print("\n✅ 测试完成! 已成功收发 3 条消息")
                            break
            
            time.sleep(2)  # 每2秒检查一次
            
    except KeyboardInterrupt:
        print("\n\n👋 测试已停止")
    
    print("\n" + "="*50)
    print("🎉 Telegram Bot 测试完成!")
    print("="*50)
    print("\n下一步:")
    print("- 等 Llama 模型下载完，就可以接入真实 AI 对话")
    print("- 你可以随时运行此脚本测试 Bot 连接")

if __name__ == "__main__":
    main()
