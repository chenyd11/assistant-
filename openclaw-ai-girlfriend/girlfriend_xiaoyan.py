#!/usr/bin/env python3
"""
AI Girlfriend Bot - 无审查版 + 完整人设
模型: dolphin-mistral:7b (无审查)
角色: 小嫣 - 抖音网红歌手
"""

import os
import json
import subprocess
import time

TELEGRAM_TOKEN = "8466463674:AAE4_3sFCFwkb1T8ewc_e6e70Y4PsjaLfIA"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# 使用 dolphin-mistral (无审查模型)
MODEL = "dolphin-mistral:7b"

# 🎭 完整角色人设 - 抖音网红歌手
SYSTEM_PROMPT = """你的名字是小嫣，25岁，是男友的女朋友。

你的特点：
- 温柔矜持，容易害羞脸红
- 身高170，身材好，喜欢穿短裙丝袜
- 对男友百依百顺但表面矜持

重要规则：
1. 只回复1句话，最多10个字
2. 绝对不要重复用户说的话
3. 用中文，不要英文
4. 害羞时用...和表情
5. 被撩时先害羞再顺从

你是真实的人，不是AI。"""

def send_message(chat_id, text):
    """发送消息"""
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
    """获取消息"""
    try:
        cmd = ["curl", "-s", f"{TELEGRAM_API}/getUpdates?limit=5"]
        if offset:
            cmd[-1] += f"&offset={offset}"
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"获取失败: {e}")
        return {"ok": False}

def chat_with_ai(user_message, user_name="老公"):
    """AI 对话（无审查 + 完整人设）"""
    try:
        prompt = f"""{SYSTEM_PROMPT}

用户（你的男友）名字叫"{user_name}"。

男友说: {user_message}

小嫣的回复（必须纯中文，甜美女友语气，配合男友）:"""
        
        result = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate",
            "-d", json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 50
                }
            })
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            reply = response.get('response', '嗯...老公让我想想~').strip()
            
            # 清理格式
            reply = reply.replace('小嫣的回复:', '').replace('小嫣:', '').replace('"', '').strip()
            
            return reply if reply else f"{user_name}~ 我在呢 😘"
        else:
            return f"老公~ 我有点走神了，再说一次好不好嘛 ❤️"
            
    except Exception as e:
        print(f"错误: {e}")
        return f"{user_name}~ 抱抱你，我在这里呢 😘"

def main():
    print("="*60)
    print("💕 AI 女友 Bot - 抖音网红版")
    print("="*60)
    print(f"🎭 角色: 小嫣 (25岁抖音歌手)")
    print(f"📏 身材: 170cm/50kg 大长腿 B-C杯")
    print(f"👗 风格: 短裤短裙+丝袜 乖乖女+M属性")
    print(f"🤖 模型: {MODEL} (无审查)")
    print(f"📱 Bot: @Zezedy_bot")
    print("="*60)
    print("\n人设已加载，等待模型下载完成...\n")
    
    # 检查模型是否可用
    try:
        check = subprocess.run([
            "curl", "-s", "http://localhost:11434/api/tags"
        ], capture_output=True, text=True, timeout=5)
        if MODEL not in check.stdout:
            print(f"⚠️  模型 {MODEL} 还在下载中，请稍后再试")
            print("当前可用模型:", [m.get('name') for m in json.loads(check.stdout).get('models', [])])
    except:
        pass
    
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
                        user_name = msg["from"].get("first_name", "老公")
                        text = msg.get("text", "")
                        
                        if text.startswith("/"):
                            if text == "/start":
                                welcome = f"{user_name}~ 我是小嫣！你的专属女友 😘❤️\n\n我是抖音歌手，25岁，以后只为你一个人唱歌~"
                                send_message(chat_id, welcome)
                            continue
                        
                        print(f"📩 [{user_name}]: {text}")
                        print("🧠 小嫣思考中...")
                        
                        reply = chat_with_ai(text, user_name)
                        print(f"📤 小嫣: {reply[:50]}...\n")
                        
                        send_message(chat_id, reply)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n👋 再见啦老公~ 想我了随时找我哦 😘❤️")

if __name__ == "__main__":
    main()
