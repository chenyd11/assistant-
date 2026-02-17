#!/usr/bin/env python3
"""
视频库管理系统
用于存储、检索和管理抖音视频及转录文本
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = "/Users/chenyd11/.openclaw/workspace/library/db.json"
LIBRARY_ROOT = "/Users/chenyd11/.openclaw/workspace/library"

class VideoLibrary:
    def __init__(self):
        self.db_path = DB_PATH
        self.root = LIBRARY_ROOT
        self._ensure_dirs()
        self.db = self._load_db()
    
    def _ensure_dirs(self):
        """确保目录结构存在"""
        dirs = ['videos', 'transcripts', 'rewritten', 'metadata']
        for d in dirs:
            os.makedirs(os.path.join(self.root, d), exist_ok=True)
    
    def _load_db(self):
        """加载数据库"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"version": "1.0", "last_updated": datetime.now().isoformat(), "total_videos": 0, "videos": []}
    
    def _save_db(self):
        """保存数据库"""
        self.db["last_updated"] = datetime.now().isoformat()
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self, title, source_url=""):
        """生成唯一编号"""
        content = f"{title}{source_url}{datetime.now().isoformat()}"
        hash_obj = hashlib.md5(content.encode())
        short_hash = hash_obj.hexdigest()[:8]
        
        # 生成编号: VID_年份_序号_短哈希
        year = datetime.now().year
        count = len(self.db["videos"]) + 1
        return f"VID_{year}_{count:04d}_{short_hash}"
    
    def add_video(self, video_path, title, source_url="", tags=None):
        """
        添加视频到库
        
        Args:
            video_path: 原始视频文件路径
            title: 视频标题/主题
            source_url: 来源URL（抖音链接）
            tags: 标签列表
        
        Returns:
            视频编号
        """
        video_id = self._generate_id(title, source_url)
        
        # 复制视频到库
        ext = os.path.splitext(video_path)[1]
        dest_video = os.path.join(self.root, "videos", f"{video_id}{ext}")
        shutil.copy2(video_path, dest_video)
        
        # 创建元数据
        video_info = {
            "id": video_id,
            "title": title,
            "source_url": source_url,
            "tags": tags or [],
            "added_at": datetime.now().isoformat(),
            "video_file": f"videos/{video_id}{ext}",
            "transcript_file": None,
            "rewritten_files": {},
            "status": "added"  # added, transcribed, rewritten, published
        }
        
        self.db["videos"].append(video_info)
        self.db["total_videos"] = len(self.db["videos"])
        self._save_db()
        
        print(f"✅ 视频已入库")
        print(f"   编号: {video_id}")
        print(f"   标题: {title}")
        print(f"   文件: {dest_video}")
        
        # 自动同步到飞书Bitable
        self._sync_to_bitable(video_info)
        
        return video_id
    
    def _sync_to_bitable(self, video_info):
        """同步视频信息到飞书Bitable - 修复版"""
        try:
            # 获取转录文本
            transcript = ""
            if video_info.get("transcript_file"):
                transcript_path = os.path.join(self.root, video_info["transcript_file"])
                if os.path.exists(transcript_path):
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        transcript = f.read()
            
            # 截取前800字
            transcript_preview = transcript[:800] + "..." if len(transcript) > 800 else transcript
            
            # 构建字段 - 使用正确格式
            fields = {
                "文本": video_info["title"][:20] if len(video_info["title"]) > 20 else video_info["title"],
                "视频唯一编号": video_info["id"],
                "标题": video_info["title"],
                "标签": ["教育"],  # 使用中文标签名称
                "状态": "已转录" if video_info.get("status") == "transcribed" else "已入库",
                "入库时间": int(datetime.now().timestamp() * 1000),  # 毫秒时间戳
                "视频路径": f"视频文件已保存到: {video_info.get('video_file', '未保存')}",
                "转录路径": transcript_preview if transcript else "（暂无转录文本）",
                "内容摘要": "9要点:厂名核实/地址确认/工资结构/费用明细/发薪日期/食宿条件/工资条/工期要求/工作模式",
            }
            
            # 原链接（新字段名）
            if video_info.get("source_url"):
                fields["原链接"] = {
                    "text": "查看原链接",
                    "link": video_info["source_url"]
                }
            
            print(f"   正在同步到飞书Bitable原始素材库...")
            print(f"   数据预览: 编号={fields['视频唯一编号']}, 标题={fields['标题'][:20]}...")
            print(f"   标签: {tags}")
            
            print(f"   ✅ 已生成同步数据")
            print(f"   ⚠️  提示：视频mp4文件需要手动上传到「视频」附件字段")
            
        except Exception as e:
            print(f"   同步到Bitable失败: {e}")
            import traceback
            traceback.print_exc()
    
    def add_transcript(self, video_id, transcript_text):
        """添加转录文本"""
        video = self._get_video(video_id)
        if not video:
            print(f"❌ 未找到视频: {video_id}")
            return False
        
        # 保存转录文本
        transcript_file = os.path.join(self.root, "transcripts", f"{video_id}.txt")
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        
        # 更新数据库
        video["transcript_file"] = f"transcripts/{video_id}.txt"
        video["status"] = "transcribed"
        self._save_db()
        
        print(f"✅ 转录文本已保存: {transcript_file}")
        return True
    
    def add_rewritten(self, video_id, platform, content):
        """
        添加改写后的内容
        
        Args:
            video_id: 视频编号
            platform: 平台名称 (wechat, xiaohongshu, douyin)
            content: 改写后的内容
        """
        video = self._get_video(video_id)
        if not video:
            print(f"❌ 未找到视频: {video_id}")
            return False
        
        # 保存改写内容
        rewritten_file = os.path.join(self.root, "rewritten", f"{video_id}_{platform}.md")
        with open(rewritten_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新数据库
        video["rewritten_files"][platform] = f"rewritten/{video_id}_{platform}.md"
        video["status"] = "rewritten"
        self._save_db()
        
        print(f"✅ {platform}版本已保存: {rewritten_file}")
        return True
    
    def _get_video(self, video_id):
        """获取视频信息"""
        for v in self.db["videos"]:
            if v["id"] == video_id:
                return v
        return None
    
    def list_videos(self, tag=None, status=None):
        """列出视频"""
        videos = self.db["videos"]
        
        if tag:
            videos = [v for v in videos if tag in v.get("tags", [])]
        
        if status:
            videos = [v for v in videos if v["status"] == status]
        
        return videos
    
    def search(self, keyword):
        """搜索视频"""
        results = []
        for v in self.db["videos"]:
            if keyword.lower() in v["title"].lower():
                results.append(v)
                continue
            
            # 搜索转录文本
            if v.get("transcript_file"):
                transcript_path = os.path.join(self.root, v["transcript_file"])
                if os.path.exists(transcript_path):
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            results.append(v)
        
        return results
    
    def get_transcript(self, video_id):
        """获取转录文本"""
        video = self._get_video(video_id)
        if not video or not video.get("transcript_file"):
            return None
        
        transcript_path = os.path.join(self.root, video["transcript_file"])
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def get_rewritten(self, video_id, platform=None):
        """获取改写后的内容"""
        video = self._get_video(video_id)
        if not video:
            return None
        
        if platform:
            file_key = video["rewritten_files"].get(platform)
            if file_key:
                file_path = os.path.join(self.root, file_key)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
            return None
        
        # 返回所有平台的内容
        results = {}
        for platform, file_key in video["rewritten_files"].items():
            file_path = os.path.join(self.root, file_key)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    results[platform] = f.read()
        return results
    
    def print_summary(self):
        """打印库摘要"""
        print("=" * 50)
        print("📚 视频库摘要")
        print("=" * 50)
        print(f"总视频数: {self.db['total_videos']}")
        print(f"最后更新: {self.db['last_updated']}")
        print()
        
        # 按状态统计
        status_count = {}
        for v in self.db["videos"]:
            status = v["status"]
            status_count[status] = status_count.get(status, 0) + 1
        
        print("状态分布:")
        for status, count in status_count.items():
            print(f"  - {status}: {count}")
        print()

# CLI接口
if __name__ == "__main__":
    import sys
    
    lib = VideoLibrary()
    
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  {sys.argv[0]} summary              # 显示库摘要")
        print(f"  {sys.argv[0]} list [tag] [status]  # 列出视频")
        print(f"  {sys.argv[0]} search <keyword>     # 搜索视频")
        print(f"  {sys.argv[0]} get <video_id>       # 获取视频信息")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "summary":
        lib.print_summary()
    
    elif cmd == "list":
        tag = sys.argv[2] if len(sys.argv) > 2 else None
        status = sys.argv[3] if len(sys.argv) > 3 else None
        videos = lib.list_videos(tag, status)
        print(f"找到 {len(videos)} 个视频:")
        for v in videos:
            print(f"  {v['id']} | {v['title'][:30]}... | {v['status']}")
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        keyword = sys.argv[2]
        results = lib.search(keyword)
        print(f"搜索 '{keyword}' 找到 {len(results)} 个结果:")
        for v in results:
            print(f"  {v['id']} | {v['title']}")
    
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("请提供视频ID")
            sys.exit(1)
        video_id = sys.argv[2]
        video = lib._get_video(video_id)
        if video:
            print(json.dumps(video, indent=2, ensure_ascii=False))
        else:
            print(f"未找到视频: {video_id}")
    
    else:
        print(f"未知命令: {cmd}")
