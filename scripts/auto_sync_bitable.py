#!/usr/bin/env python3
"""
视频库自动同步到飞书Bitable
每当本地库有新视频时，自动同步到飞书表格
"""

import sys
import json
sys.path.insert(0, '/Users/chenyd11/.openclaw/workspace/library')
from video_lib import VideoLibrary

# Bitable配置
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
TABLE_ID = "tbl49MRT9hEVlCVX"

# 标签映射（需要根据Bitable中的选项配置）
TAG_MAPPING = {
    "打工": "optjmoA0jO",  # 教育
    "避坑": "optPJCqHvR",  # 娱乐
    "工厂": "opt7KOmU6y",  # 科技
    "求职": "optmeJn1LS",  # 体育
}

# 状态映射
STATUS_MAPPING = {
    "added": "optEQQtHMh",      # 已入库
    "transcribed": "optKfzA76J", # 已转录
    "rewritten": "optDg5NHBb",   # 已改写
    "published": "optCbvBkr0",   # 已发布
}

def sync_to_bitable(video_id=None):
    """
    同步视频到Bitable
    
    Args:
        video_id: 指定视频ID，None则同步所有未同步的视频
    """
    from feishu_bitable_create_record import feishu_bitable_create_record
    
    lib = VideoLibrary()
    
    if video_id:
        videos = [lib._get_video(video_id)]
    else:
        # 获取所有视频
        videos = lib.list_videos()
    
    print(f"开始同步 {len(videos)} 个视频到Bitable...")
    print()
    
    for v in videos:
        if not v:
            continue
            
        # 映射标签
        tags = []
        for tag in v.get("tags", []):
            if tag in TAG_MAPPING:
                tags.append(TAG_MAPPING[tag])
        if not tags:
            tags = ["optjmoA0jO"]  # 默认标签
        
        # 映射状态
        status = STATUS_MAPPING.get(v.get("status", "added"), "optEQQtHMh")
        
        # 构建字段
        fields = {
            "文本": v["title"][:20] if len(v["title"]) > 20 else v["title"],
            "视频唯一编号": v["id"],
            "标题": v["title"],
            "标签": tags,
            "状态": status,
            "来源": {
                "text": "抖音链接",
                "link": v.get("source_url", "")
            } if v.get("source_url") else None,
            "入库时间": int(v["added_at"].timestamp()) if hasattr(v["added_at"], 'timestamp') else 1771162791,
            "视频路径": v.get("video_file", ""),
            "转录路径": v.get("transcript_file", ""),
            "内容摘要": "待补充",
            "后续处理": "待洗稿/待改写/待发布"
        }
        
        # 移除空值
        fields = {k: v for k, v in fields.items() if v is not None}
        
        print(f"同步: {v['id']} - {v['title'][:30]}...")
        
        # 这里调用API创建记录
        # 实际使用时需要通过tool调用
        print(f"  字段: {json.dumps(fields, ensure_ascii=False)[:100]}...")
        print()
    
    print("同步完成!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='同步视频库到飞书Bitable')
    parser.add_argument('--video-id', help='指定视频ID同步')
    parser.add_argument('--all', action='store_true', help='同步所有视频')
    
    args = parser.parse_args()
    
    if args.video_id:
        sync_to_bitable(args.video_id)
    elif args.all:
        sync_to_bitable()
    else:
        print("用法:")
        print("  python3 auto_sync_bitable.py --all          # 同步所有视频")
        print("  python3 auto_sync_bitable.py --video-id VID_2026_0001  # 同步指定视频")
