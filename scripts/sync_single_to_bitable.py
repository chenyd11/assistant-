#!/usr/bin/env python3
"""
同步单个视频到飞书Bitable
被video_lib.py调用
"""

import json
import sys

# Bitable配置
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
TABLE_ID = "tbl49MRT9hEVlCVX"

# 标签映射
TAG_MAPPING = {
    "打工": "optjmoA0jO",
    "避坑": "optPJCqHvR",
    "工厂": "opt7KOmU6y",
    "求职": "optmeJn1LS",
}

# 状态映射
STATUS_MAPPING = {
    "added": "optEQQtHMh",
    "transcribed": "optKfzA76J",
    "rewritten": "optDg5NHBb",
    "published": "optCbvBkr0",
}

def sync_video(video_info):
    """同步视频到Bitable"""
    
    # 映射标签
    tags = []
    for tag in video_info.get("tags", []):
        if tag in TAG_MAPPING:
            tags.append(TAG_MAPPING[tag])
    if not tags:
        tags = ["optjmoA0jO"]
    
    # 映射状态
    status = STATUS_MAPPING.get(video_info.get("status", "added"), "optEQQtHMh")
    
    # 构建字段
    fields = {
        "文本": video_info["title"][:20] if len(video_info["title"]) > 20 else video_info["title"],
        "视频唯一编号": video_info["id"],
        "标题": video_info["title"],
        "标签": tags,
        "状态": status,
        "视频路径": video_info.get("video_file", ""),
        "转录路径": video_info.get("transcript_file", ""),
        "内容摘要": "待补充",
        "后续处理": "待洗稿/待改写/待发布"
    }
    
    # 添加来源（如果有）
    if video_info.get("source_url"):
        fields["来源"] = {
            "text": "查看链接",
            "link": video_info["source_url"]
        }
    
    # 添加入库时间
    from datetime import datetime
    fields["入库时间"] = int(datetime.now().timestamp())
    
    print(f"正在同步: {video_info['id']}")
    print(f"字段: {json.dumps(fields, ensure_ascii=False)}")
    
    # 这里应该调用feishu_bitable_create_record
    # 但由于是在子进程中，我们直接输出字段，由调用者处理
    return fields

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_info = json.loads(sys.argv[1])
        fields = sync_video(video_info)
        print(json.dumps(fields, ensure_ascii=False))
    else:
        print("请提供视频信息")
        sys.exit(1)
