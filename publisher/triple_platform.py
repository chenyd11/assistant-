#!/usr/bin/env python3
"""
三平台内容分发工具
支持：公众号、抖音、小红书（支持多账号）
"""

import json
import os
from datetime import datetime

# 平台配置
PLATFORMS = {
    "wechat": {
        "name": "微信公众号",
        "url": "https://mp.weixin.qq.com",
        "features": ["富文本", "图文", "原创声明"],
        "format": "html",
        "max_length": None,
        "supports_multi_account": False  # 公众号通常只有一个
    },
    "xiaohongshu": {
        "name": "小红书",
        "url": "https://creator.xiaohongshu.com",
        "features": ["图文笔记", "标签", "emoji", "多账号"],
        "format": "markdown",
        "max_length": 1000,
        "supports_multi_account": True
    },
    "douyin": {
        "name": "抖音",
        "url": "https://creator.douyin.com",
        "features": ["图文", "短视频", "话题", "多账号"],
        "format": "text",
        "max_length": 500,
        "supports_multi_account": True
    }
}

class TriplePlatformPublisher:
    """三平台发布器（公众号+抖音+小红书）"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or "/Users/chenyd11/.openclaw/workspace/publisher/triple_config.json"
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "accounts": {
                "wechat": [],
                "xiaohongshu": [],
                "douyin": []
            },
            "published": []
        }
    
    def _save_config(self):
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def add_account(self, platform, account_name, cookie=None, token=None, notes=""):
        """
        添加账号
        
        Args:
            platform: wechat | xiaohongshu | douyin
            account_name: 账号名称（如"主号"、"小号"、"XX品牌号"）
            cookie: 登录cookie（可选）
            token: API token（可选）
            notes: 备注说明
        """
        if platform not in PLATFORMS:
            print(f"❌ 不支持的平台: {platform}")
            return False
        
        account = {
            "id": f"{platform}_{len(self.config['accounts'][platform]) + 1}",
            "name": account_name,
            "cookie": cookie,
            "token": token,
            "notes": notes,
            "added_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.config["accounts"][platform].append(account)
        self._save_config()
        
        platform_name = PLATFORMS[platform]["name"]
        print(f"✅ 已添加 {platform_name} 账号: {account_name} (ID: {account['id']})")
        return True
    
    def list_accounts(self, platform=None):
        """列出已配置的账号"""
        print("=" * 60)
        print("📱 已配置的账号")
        print("=" * 60)
        
        platforms_to_show = [platform] if platform else PLATFORMS.keys()
        
        for p in platforms_to_show:
            if p not in PLATFORMS:
                continue
            
            info = PLATFORMS[p]
            accounts = self.config["accounts"].get(p, [])
            
            print(f"\n{info['name']} ({p})")
            print("-" * 40)
            
            if not accounts:
                print("   (暂无账号)")
            else:
                for acc in accounts:
                    status = "✅" if acc.get("status") == "active" else "❌"
                    print(f"   {status} [{acc['id']}] {acc['name']}")
                    if acc.get("notes"):
                        print(f"      备注: {acc['notes']}")
        print()
    
    def remove_account(self, platform, account_id):
        """删除账号"""
        accounts = self.config["accounts"].get(platform, [])
        for i, acc in enumerate(accounts):
            if acc["id"] == account_id:
                del accounts[i]
                self._save_config()
                print(f"✅ 已删除账号: {account_id}")
                return True
        print(f"❌ 未找到账号: {account_id}")
        return False
    
    def format_for_platform(self, content, platform, account_name=""):
        """
        根据平台格式化内容
        
        Args:
            content: {title, body, tags, images}
            platform: 目标平台
            account_name: 账号名称（用于个性化）
        """
        if platform not in PLATFORMS:
            return content
        
        info = PLATFORMS[platform]
        formatted = content.copy()
        
        # 根据平台调整
        if platform == "wechat":
            # 公众号：富文本格式
            formatted["body"] = self._to_wechat_format(formatted["body"])
            formatted["cover"] = formatted.get("images", [""])[0] if formatted.get("images") else ""
            
        elif platform == "xiaohongshu":
            # 小红书：emoji风格，限制长度
            formatted["body"] = self._to_xiaohongshu_format(formatted["body"])
            formatted["body"] = self._truncate(formatted["body"], info.get("max_length", 1000))
            formatted["tags"] = self._format_tags(formatted.get("tags", []), "#")
            
        elif platform == "douyin":
            # 抖音：超短文案，话题标签
            formatted["body"] = self._to_douyin_format(formatted["body"])
            formatted["body"] = self._truncate(formatted["body"], info.get("max_length", 500))
            formatted["tags"] = self._format_tags(formatted.get("tags", []), "#")
        
        return formatted
    
    def _to_wechat_format(self, text):
        """转换为公众号格式（HTML）"""
        import re
        
        # 标题转换
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # 粗体、斜体
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # 段落
        paragraphs = text.split('\n\n')
        text = ''.join([f'<p>{p}</p>' for p in paragraphs if p.strip()])
        
        return text
    
    def _to_xiaohongshu_format(self, text):
        """转换为小红书格式（emoji+短句）"""
        # 添加emoji映射
        emoji_map = {
            "重要": "❗",
            "注意": "⚠️",
            "推荐": "👍",
            "干货": "💡",
            "必看": "👀",
            "收藏": "⭐",
            "喜欢": "❤️",
            "开心": "😊",
            "难过": "😢",
            "警告": "🚨",
            "第一": "1️⃣",
            "第二": "2️⃣",
            "第三": "3️⃣",
            "第四": "4️⃣",
            "第五": "5️⃣",
            "第六": "6️⃣",
            "第七": "7️⃣",
            "第八": "8️⃣",
            "第九": "9️⃣",
            "第十": "🔟",
        }
        
        for word, emoji in emoji_map.items():
            text = text.replace(word, f"{emoji}{word}")
        
        # 确保有适当的换行
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                formatted_lines.append(line)
                if len(line) < 30:  # 短句后加空行
                    formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _to_douyin_format(self, text):
        """转换为抖音格式（超短+抓眼球）"""
        lines = text.split('\n')
        short_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 只保留关键短句
            if len(line) <= 50:
                short_lines.append(line)
            if len(short_lines) >= 9:  # 最多9点
                break
        
        return '\n'.join(short_lines)
    
    def _truncate(self, text, max_length):
        """截断文本"""
        if not max_length or len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _format_tags(self, tags, prefix="#"):
        """格式化标签"""
        return [f"{prefix}{tag}" for tag in tags]
    
    def create_publish_plan(self, content, platforms=None, accounts=None):
        """
        创建发布计划
        
        Args:
            content: {title, body, tags, images}
            platforms: 平台列表 ['wechat', 'xiaohongshu', 'douyin']，None表示全部
            accounts: 指定账号 {'xiaohongshu': ['xiaohongshu_1', 'xiaohongshu_2']}
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
        print(f"原始长度: {len(content.get('body', ''))} 字符")
        print()
        
        for platform in platforms:
            if platform not in PLATFORMS:
                continue
            
            info = PLATFORMS[platform]
            platform_accounts = accounts.get(platform, []) if accounts else []
            
            # 如果没有指定账号，使用所有已配置账号
            if not platform_accounts:
                platform_accounts = [acc["id"] for acc in self.config["accounts"].get(platform, [])]
            
            # 如果没有配置账号，提示添加
            if not platform_accounts:
                print(f"⚠️  {info['name']}: 未配置账号，请先添加")
                continue
            
            for account_id in platform_accounts:
                account = self._get_account(platform, account_id)
                account_name = account["name"] if account else account_id
                
                formatted = self.format_for_platform(content, platform, account_name)
                
                target = {
                    "platform": platform,
                    "platform_name": info["name"],
                    "account_id": account_id,
                    "account_name": account_name,
                    "status": "pending",
                    "formatted_content": formatted
                }
                plan["targets"].append(target)
                
                print(f"📱 {info['name']} - {account_name}")
                print(f"   调整后长度: {len(formatted['body'])} 字符")
        
        print()
        print(f"共 {len(plan['targets'])} 个发布目标")
        
        return plan
    
    def _get_account(self, platform, account_id):
        """获取账号信息"""
        for acc in self.config["accounts"].get(platform, []):
            if acc["id"] == account_id:
                return acc
        return None
    
    def generate_publish_scripts(self, plan, output_dir=None):
        """
        生成发布脚本（为每个平台生成独立脚本）
        """
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"/Users/chenyd11/.openclaw/workspace/publisher/scripts/{timestamp}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        generated = []
        
        for target in plan["targets"]:
            platform = target["platform"]
            account = target["account_name"]
            content = target["formatted_content"]
            
            filename = f"{platform}_{target['account_id']}.py"
            filepath = os.path.join(output_dir, filename)
            
            script = self._generate_platform_script(platform, account, content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script)
            
            os.chmod(filepath, 0o755)
            generated.append(filepath)
        
        # 生成主运行脚本
        main_script = os.path.join(output_dir, "publish_all.sh")
        with open(main_script, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write("# 一键发布到所有平台\n\n")
            for script in generated:
                f.write(f'echo "发布: {os.path.basename(script)}"\n')
                f.write(f'python3 "{script}"\n')
                f.write('echo ""\n')
        os.chmod(main_script, 0o755)
        
        print("=" * 60)
        print("✅ 发布脚本已生成")
        print("=" * 60)
        print(f"目录: {output_dir}")
        print()
        print("生成的脚本:")
        for script in generated:
            print(f"  - {os.path.basename(script)}")
        print()
        print(f"一键运行: {main_script}")
        
        return output_dir
    
    def _generate_platform_script(self, platform, account_name, content):
        """生成单个平台的发布脚本"""
        info = PLATFORMS[platform]
        
        script = f'''#!/usr/bin/env python3
"""
发布到 {info['name']} - {account_name}
生成时间: {datetime.now().isoformat()}
"""

CONTENT = {json.dumps(content, ensure_ascii=False, indent=2)}

def publish():
    print("=" * 60)
    print("📱 发布到: {info['name']}")
    print("👤 账号: {account_name}")
    print("=" * 60)
    print()
    print("标题:")
    print(f"  {{CONTENT['title']}}")
    print()
    print("内容:")
    print(f"  {{CONTENT['body'][:200]}}...")
    print()
    if CONTENT.get('tags'):
        print("标签:")
        print(f"  {{', '.join(CONTENT['tags'])}}")
    print()
    
    # TODO: 实现浏览器自动化
    # 1. 打开 {info['url']}
    # 2. 登录账号
    # 3. 创建新内容
    # 4. 填充标题、正文、标签
    # 5. 发布
    
    print("⚠️  请手动完成以下步骤:")
    print("  1. 打开 {info['url']}")
    print("  2. 登录账号: {account_name}")
    print("  3. 创建新内容")
    print("  4. 复制以下内容:")
    print()
    print("-" * 40)
    print(CONTENT['title'])
    print("-" * 40)
    print(CONTENT['body'])
    print("-" * 40)
    if CONTENT.get('tags'):
        print("标签: " + " ".join(CONTENT['tags']))
    print("-" * 40)
    print()
    input("发布完成后按回车键继续...")

if __name__ == "__main__":
    publish()
'''
        return script

# CLI接口
if __name__ == "__main__":
    import sys
    
    publisher = TriplePlatformPublisher()
    
    if len(sys.argv) < 2:
        print("三平台内容分发工具 (公众号+抖音+小红书)")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} accounts                    # 列出所有账号")
        print(f"  {sys.argv[0]} add <平台> <账号名> [备注]   # 添加账号")
        print(f"  {sys.argv[0]} remove <平台> <账号ID>       # 删除账号")
        print()
        print("平台代码: wechat(公众号), xiaohongshu(小红书), douyin(抖音)")
        print()
        print("示例:")
        print(f"  {sys.argv[0]} add xiaohongshu 主号 日常分享号")
        print(f"  {sys.argv[0]} add xiaohongshu 品牌号 XX品牌推广")
        print(f"  {sys.argv[0]} add douyin 个人号")
        print()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "accounts":
        publisher.list_accounts()
    
    elif cmd == "add":
        if len(sys.argv) < 4:
            print("请提供平台代码和账号名称")
            sys.exit(1)
        platform = sys.argv[2]
        account_name = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        publisher.add_account(platform, account_name, notes=notes)
    
    elif cmd == "remove":
        if len(sys.argv) < 4:
            print("请提供平台代码和账号ID")
            sys.exit(1)
        platform = sys.argv[2]
        account_id = sys.argv[3]
        publisher.remove_account(platform, account_id)
    
    else:
        print(f"未知命令: {cmd}")
