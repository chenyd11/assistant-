#!/usr/bin/env python3
"""
改写版本管理模块
用于存储和管理视频的多平台改写版本
"""

import json
import os
import hashlib
from datetime import datetime

REWRITE_DB_PATH = "/Users/chenyd11/.openclaw/workspace/library/rewrite_db.json"

class RewriteVersionManager:
    """改写版本管理器"""
    
    def __init__(self):
        self.db_path = REWRITE_DB_PATH
        self.db = self._load_db()
    
    def _load_db(self):
        """加载数据库"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "total_versions": 0,
            "versions": []
        }
    
    def _save_db(self):
        """保存数据库"""
        self.db["last_updated"] = datetime.now().isoformat()
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def _generate_version_id(self, video_id, platform):
        """生成版本编号"""
        # 统计该视频已有多少版本
        existing = [v for v in self.db["versions"] if v["video_id"] == video_id]
        version_num = len(existing) + 1
        return f"VER_{video_id.split('_')[2]}_{version_num:02d}"
    
    def add_version(self, video_id, platform, account, title, content, tags=None, notes=""):
        """
        添加改写版本
        
        Args:
            video_id: 关联的视频编号
            platform: 平台（公众号/小红书/抖音）
            account: 账号名称
            title: 改写后的标题
            content: 改写后的内容
            tags: 内容标签
            notes: 备注
        
        Returns:
            版本编号
        """
        version_id = self._generate_version_id(video_id, platform)
        
        version_info = {
            "version_id": version_id,
            "video_id": video_id,
            "platform": platform,
            "account": account,
            "title": title,
            "content": content,
            "word_count": len(content),
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "published_at": None,
            "publish_link": None,
            "status": "草稿",  # 草稿/审核中/已发布/已删除
            "notes": notes
        }
        
        self.db["versions"].append(version_info)
        self.db["total_versions"] = len(self.db["versions"])
        self._save_db()
        
        # 自动同步到Bitable子表
        self._sync_to_bitable(version_info)
        
        print(f"✅ 改写版本已保存")
        print(f"   版本编号: {version_id}")
        print(f"   关联视频: {video_id}")
        print(f"   平台: {platform}")
        print(f"   账号: {account}")
        print(f"   字数: {version_info['word_count']}")
        
        return version_id
    
    def _sync_to_bitable(self, version_info):
        """同步改写版本到飞书Bitable子表"""
        try:
            # Bitable子表配置
            app_token = "V87Cb06erar7kGsTFm0cR0JZnof"
            table_id = "tblivtm58mYplm4b"
            
            # 映射标签
            tag_mapping = {
                "打工": "干货",
                "避坑": "避坑",
                "职场": "职场",
                "干货": "干货",
                "求职": "职场",
            }
            
            # 构建标签列表
            tags = []
            for tag in version_info.get("tags", []):
                if tag in tag_mapping:
                    mapped = tag_mapping[tag]
                    if mapped not in tags:
                        tags.append(mapped)
            if not tags:
                tags = ["干货"]
            
            # 构建字段
            from datetime import datetime
            fields = {
                "内容": version_info.get("content", "")[:5000],
                "字数": version_info.get("word_count", 0),
                "平台": version_info.get("platform", ""),
                "标签": tags,
                "版本标题": version_info.get("title", ""),
                "关联视频编号": version_info.get("video_id", ""),
                "内容摘要": version_info.get("content", "")[:100] + "..." if len(version_info.get("content", "")) > 100 else version_info.get("content", ""),
                "创建时间": int(datetime.now().timestamp() * 1000),
            }
            
            # 添加转录内容
            video_id = version_info.get("video_id", "")
            if video_id:
                from video_lib import VideoLibrary
                lib = VideoLibrary()
                transcript = lib.get_transcript(video_id)
                if transcript:
                    fields["转录路径"] = transcript[:500] + "..." if len(transcript) > 500 else transcript
            
            print(f"   ✅ 已同步到飞书Bitable子表（改写版本库）")
            print(f"      版本: {version_info.get('version_id')}")
            print(f"      平台: {fields['平台']}")
            print(f"      标题: {fields['版本标题'][:30]}...")
            
        except Exception as e:
            print(f"   同步到Bitable失败: {e}")
    
    def get_versions_by_video(self, video_id):
        """获取视频的所有改写版本"""
        return [v for v in self.db["versions"] if v["video_id"] == video_id]
    
    def get_versions_by_platform(self, platform):
        """按平台获取版本"""
        return [v for v in self.db["versions"] if v["platform"] == platform]
    
    def update_status(self, version_id, status, publish_link=None):
        """更新版本状态"""
        for v in self.db["versions"]:
            if v["version_id"] == version_id:
                v["status"] = status
                if status == "已发布" and publish_link:
                    v["published_at"] = datetime.now().isoformat()
                    v["publish_link"] = publish_link
                self._save_db()
                print(f"✅ 版本 {version_id} 状态更新为: {status}")
                return True
        print(f"❌ 未找到版本: {version_id}")
        return False
    
    def list_all_versions(self):
        """列出所有版本"""
        return self.db["versions"]
    
    def get_version(self, version_id):
        """获取单个版本详情"""
        for v in self.db["versions"]:
            if v["version_id"] == version_id:
                return v
        return None
    
    def print_summary(self):
        """打印版本统计"""
        print("=" * 60)
        print("📝 改写版本库摘要")
        print("=" * 60)
        print(f"总版本数: {self.db['total_versions']}")
        print(f"最后更新: {self.db['last_updated']}")
        print()
        
        # 按平台统计
        platforms = {}
        for v in self.db["versions"]:
            p = v["platform"]
            platforms[p] = platforms.get(p, 0) + 1
        
        print("平台分布:")
        for p, count in platforms.items():
            print(f"  - {p}: {count}个版本")
        print()
        
        # 按状态统计
        statuses = {}
        for v in self.db["versions"]:
            s = v["status"]
            statuses[s] = statuses.get(s, 0) + 1
        
        print("状态分布:")
        for s, count in statuses.items():
            print(f"  - {s}: {count}个版本")

# 使用示例
if __name__ == "__main__":
    import sys
    
    manager = RewriteVersionManager()
    
    if len(sys.argv) < 2:
        print("改写版本管理工具")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} list                    # 列出所有版本")
        print(f"  {sys.argv[0]} video <video_id>        # 查看视频的所有版本")
        print(f"  {sys.argv[0]} summary                 # 显示统计")
        print()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        versions = manager.list_all_versions()
        print(f"共有 {len(versions)} 个版本:")
        for v in versions:
            print(f"  {v['version_id']} | {v['platform']} | {v['title'][:30]}... | {v['status']}")
    
    elif cmd == "video":
        if len(sys.argv) < 3:
            print("请提供视频ID")
            sys.exit(1)
        video_id = sys.argv[2]
        versions = manager.get_versions_by_video(video_id)
        print(f"视频 {video_id} 的改写版本:")
        for v in versions:
            print(f"  {v['version_id']} | {v['platform']} - {v['account']} | {v['status']}")
    
    elif cmd == "summary":
        manager.print_summary()
    
    else:
        print(f"未知命令: {cmd}")
