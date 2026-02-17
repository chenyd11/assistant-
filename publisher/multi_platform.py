#!/usr/bin/env python3
"""
多平台内容分发工具 - 简化版"字流"
一键将内容发布到多个平台
"""

import json
import os
from datetime import datetime

# 平台配置 - 支持的平台列表
PLATFORMS = {
    "wechat": {
        "name": "微信公众号",
        "url": "https://mp.weixin.qq.com",
        "features": ["富文本", "图文", "原创声明"],
        "format": "html"
    },
    "xiaohongshu": {
        "name": "小红书",
        "url": "https://www.xiaohongshu.com",
        "features": ["图文笔记", "标签", "emoji"],
        "format": "markdown",
        "max_length": 1000
    },
    "douyin": {
        "name": "抖音",
        "url": "https://creator.douyin.com",
        "features": ["图文", "短视频", "话题"],
        "format": "text",
        "max_length": 500
    },
    "zhihu": {
        "name": "知乎",
        "url": "https://zhuanlan.zhihu.com",
        "features": ["文章", "回答", "专栏"],
        "format": "markdown"
    },
    "juejin": {
        "name": "掘金",
        "url": "https://juejin.cn",
        "features": ["文章", "沸点", "专栏"],
        "format": "markdown"
    },
    "bilibili": {
        "name": "B站专栏",
        "url": "https://member.bilibili.com",
        "features": ["专栏", "图文", "标签"],
        "format": "markdown"
    },
    "weibo": {
        "name": "微博",
        "url": "https://weibo.com",
        "features": ["图文", "话题", "长微博"],
        "format": "text",
        "max_length": 5000
    },
    "toutiao": {
        "name": "今日头条",
        "url": "https://mp.toutiao.com",
        "features": ["文章", "微头条", "原创"],
        "format": "html"
    },
    "baijiahao": {
        "name": "百家号",
        "url": "https://baijiahao.baidu.com",
        "features": ["文章", "动态", "原创"],
        "format": "html"
    },
    "csdn": {
        "name": "CSDN",
        "url": "https://mp.csdn.net",
        "features": ["博客", "blink", "专栏"],
        "format": "markdown"
    },
    "jianshu": {
        "name": "简书",
        "url": "https://www.jianshu.com",
        "features": ["文章", "专题", "连载"],
        "format": "markdown"
    },
    "sspai": {
        "name": "少数派",
        "url": "https://sspai.com",
        "features": ["文章", "Matrix", "标签"],
        "format": "markdown"
    },
    "douban": {
        "name": "豆瓣",
        "url": "https://www.douban.com",
        "features": ["日记", "广播", "小组"],
        "format": "html"
    },
    "即刻": {
        "name": "即刻",
        "url": "https://web.okjike.com",
        "features": ["动态", "话题", "圈子"],
        "format": "text",
        "max_length": 2000
    }
}

class MultiPlatformPublisher:
    """多平台发布器"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or "/Users/chenyd11/.openclaw/workspace/publisher/config.json"
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"accounts": {}, "published": []}
    
    def _save_config(self):
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def list_platforms(self):
        """列出支持的平台"""
        print("=" * 60)
        print("📱 支持发布的平台")
        print("=" * 60)
        for key, info in PLATFORMS.items():
            status = "✅ 已配置" if key in self.config.get("accounts", {}) else "⏳ 未配置"
            print(f"\n{info['name']} ({key})")
            print(f"   功能: {', '.join(info['features'])}")
            print(f"   格式: {info['format']}")
            print(f"   状态: {status}")
        print()
    
    def add_account(self, platform, username, cookie=None, token=None):
        """添加账号配置"""
        if platform not in PLATFORMS:
            print(f"❌ 不支持的平台: {platform}")
            return False
        
        if "accounts" not in self.config:
            self.config["accounts"] = {}
        
        self.config["accounts"][platform] = {
            "username": username,
            "cookie": cookie,
            "token": token,
            "added_at": datetime.now().isoformat()
        }
        self._save_config()
        
        print(f"✅ 已添加 {PLATFORMS[platform]['name']} 账号: {username}")
        return True
    
    def format_content(self, content, platform, content_type="article"):
        """
        根据平台格式化内容
        
        Args:
            content: 原始内容 (dict with 'title', 'body', 'tags')
            platform: 目标平台
            content_type: 内容类型 (article, short, note)
        """
        if platform not in PLATFORMS:
            return content
        
        platform_info = PLATFORMS[platform]
        formatted = content.copy()
        
        # 根据平台调整格式
        if platform == "xiaohongshu":
            # 小红书：添加emoji，限制长度
            formatted["body"] = self._add_emoji(formatted["body"])
            formatted["body"] = self._truncate(formatted["body", platform_info.get("max_length", 1000)])
            
        elif platform == "douyin":
            # 抖音：超短文案
            formatted["body"] = self._shorten(formatted["body"], 300)
            
        elif platform == "zhihu":
            # 知乎：专业格式
            formatted["body"] = self._add_references(formatted["body"])
            
        elif platform in ["wechat", "toutiao", "baijiahao"]:
            # 富文本平台：转换为HTML
            formatted["body"] = self._markdown_to_html(formatted["body"])
        
        return formatted
    
    def _add_emoji(self, text):
        """添加emoji（小红书风格）"""
        # 简化的emoji映射
        emoji_map = {
            "重要": "❗",
            "注意": "⚠️",
            "推荐": "👍",
            "喜欢": "❤️",
            "开心": "😊",
            "难过": "😢",
            "生气": "😠",
            "惊讶": "😲",
        }
        for word, emoji in emoji_map.items():
            text = text.replace(word, f"{emoji}{word}")
        return text
    
    def _truncate(self, text, max_length):
        """截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _shorten(self, text, max_length):
        """缩短为短文案"""
        lines = text.split('\n')
        short_lines = []
        total = 0
        
        for line in lines:
            if total + len(line) > max_length:
                break
            short_lines.append(line)
            total += len(line)
        
        return '\n'.join(short_lines)
    
    def _add_references(self, text):
        """添加引用（知乎风格）"""
        # 简化处理
        return text + "\n\n---\n*以上内容仅供参考*"
    
    def _markdown_to_html(self, text):
        """Markdown转HTML（简化版）"""
        import re
        
        # 标题
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # 粗体、斜体
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # 换行
        text = text.replace('\n\n', '</p><p>')
        text = '<p>' + text + '</p>'
        
        return text
    
    def publish_plan(self, content, platforms=None):
        """
        生成发布计划
        
        Args:
            content: 内容字典 {title, body, tags, images}
            platforms: 目标平台列表，None表示全部
        """
        if platforms is None:
            platforms = list(PLATFORMS.keys())
        
        plan = {
            "created_at": datetime.now().isoformat(),
            "content": content,
            "targets": []
        }
        
        print("=" * 60)
        print("📋 发布计划")
        print("=" * 60)
        print(f"标题: {content.get('title', '无标题')}")
        print(f"内容长度: {len(content.get('body', ''))} 字符")
        print()
        
        for platform in platforms:
            if platform not in PLATFORMS:
                continue
            
            info = PLATFORMS[platform]
            formatted = self.format_content(content, platform)
            
            target = {
                "platform": platform,
                "platform_name": info["name"],
                "status": "pending",
                "formatted_content": formatted
            }
            plan["targets"].append(target)
            
            print(f"📱 {info['name']}")
            print(f"   格式: {info['format']}")
            print(f"   调整后长度: {len(formatted['body'])} 字符")
            print()
        
        return plan
    
    def generate_publish_script(self, plan, output_path=None):
        """
        生成发布脚本（浏览器自动化）
        
        这会生成一个Python脚本，使用Playwright/Selenium
        自动打开发布页面并填充内容
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/Users/chenyd11/.openclaw/workspace/publisher/scripts/publish_{timestamp}.py"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        script_content = f'''#!/usr/bin/env python3
"""
自动发布脚本
生成时间: {datetime.now().isoformat()}
"""

import time

# 发布配置
PLAN = {json.dumps(plan, ensure_ascii=False, indent=2)}

def publish_to_platform(platform, content):
    """
    发布到指定平台
    
    注意: 这是一个模板脚本，需要手动完成以下步骤:
    1. 安装依赖: pip install playwright
    2. 安装浏览器: playwright install
    3. 实现具体的登录和发布逻辑
    """
    print(f"正在发布到 {{platform}}...")
    print(f"标题: {{content['title']}}")
    print(f"内容预览: {{content['body'][:100]}}...")
    print()
    
    # TODO: 实现浏览器自动化
    # from playwright.sync_api import sync_playwright
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     page = browser.new_page()
    #     # ... 具体的发布逻辑
    
    print("⚠️  请手动完成发布")
    input("按回车键继续下一个平台...")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 多平台自动发布")
    print("=" * 60)
    print()
    
    for target in PLAN["targets"]:
        platform = target["platform"]
        content = target["formatted_content"]
        publish_to_platform(platform, content)
    
    print()
    print("✅ 所有平台处理完成")
'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        os.chmod(output_path, 0o755)
        
        print(f"✅ 发布脚本已生成: {output_path}")
        print()
        print("使用说明:")
        print(f"  1. 查看脚本: cat {output_path}")
        print(f"  2. 手动运行: python3 {output_path}")
        print(f"  3. 按提示逐个平台发布")
        
        return output_path

# CLI接口
if __name__ == "__main__":
    import sys
    
    publisher = MultiPlatformPublisher()
    
    if len(sys.argv) < 2:
        print("多平台内容分发工具")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} platforms              # 列出支持的平台")
        print(f"  {sys.argv[0]} add <平台> <用户名>    # 添加账号")
        print(f"  {sys.argv[0]} plan <内容文件>        # 生成发布计划")
        print()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "platforms":
        publisher.list_platforms()
    
    elif cmd == "add":
        if len(sys.argv) < 4:
            print("请提供平台名称和用户名")
            sys.exit(1)
        platform = sys.argv[2]
        username = sys.argv[3]
        publisher.add_account(platform, username)
    
    elif cmd == "plan":
        # 示例：从文件读取内容生成发布计划
        print("请提供内容文件路径")
        print("示例内容格式:")
        print(json.dumps({
            "title": "文章标题",
            "body": "文章内容...",
            "tags": ["标签1", "标签2"]
        }, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {cmd}")
