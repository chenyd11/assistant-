#!/usr/bin/env python3
"""
改写版本自动同步到飞书Bitable子表
"""

import json
import sys
import os

# 添加库路径
sys.path.insert(0, '/Users/chenyd11/.openclaw/workspace/library')
from rewrite_manager import RewriteVersionManager

# Bitable子表配置
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
TABLE_ID = "tblivtm58mYplm4b"  # 改写版本库子表

# 字段映射（Bitable字段名 → 本地数据字段名）
FIELD_MAPPING = {
    "内容": "content",           # 主字段，放完整内容
    "字数": "word_count",        # 数字
    "平台": "platform",          # 单选：公众号/小红书/抖音
    "标签": "tags",              # 多选：干货/避坑/职场
    "版本标题": "title",         # 文本
    "发布链接": "publish_link",  # URL
    "创建时间": "created_at",    # 日期
    "关联视频编号": "video_id",  # 文本
    "转录路径": "transcript",    # 文本，这里放转录内容
    "内容摘要": "summary",       # 文本
}

def sync_version_to_bitable(version_info):
    """
    同步单个改写版本到Bitable子表
    
    Args:
        version_info: 改写版本信息字典
    """
    from datetime import datetime
    
    # 映射标签（本地标签 → Bitable选项）
    tag_mapping = {
        "干货": "optKjncNeS",
        "避坑": "optujStt7e", 
        "职场": "optsU2v2PQ",
        "打工": "optKjncNeS",  # 默认映射到干货
        "求职": "optsU2v2PQ",  # 映射到职场
    }
    
    # 映射平台（直接使用中文名称）
    platform = version_info.get("platform", "")
    
    # 映射标签
    tags = []
    for tag in version_info.get("tags", []):
        if tag in tag_mapping:
            tags.append(tag)  # 使用中文名称
    if not tags:
        tags = ["干货"]  # 默认标签
    
    # 构建字段
    fields = {
        "内容": version_info.get("content", "")[:5000],  # 限制长度
        "字数": version_info.get("word_count", 0),
        "平台": platform,
        "标签": tags,
        "版本标题": version_info.get("title", ""),
        "关联视频编号": version_info.get("video_id", ""),
        "内容摘要": version_info.get("content", "")[:100] + "..." if len(version_info.get("content", "")) > 100 else version_info.get("content", ""),
        "创建时间": int(datetime.now().timestamp() * 1000),
    }
    
    # 如果有发布链接
    if version_info.get("publish_link"):
        fields["发布链接"] = {
            "text": "查看发布",
            "link": version_info["publish_link"]
        }
    
    # 转录内容（从本地读取）
    video_id = version_info.get("video_id", "")
    if video_id:
        from video_lib import VideoLibrary
        lib = VideoLibrary()
        transcript = lib.get_transcript(video_id)
        if transcript:
            fields["转录路径"] = transcript[:500] + "..." if len(transcript) > 500 else transcript
    
    print(f"准备同步版本: {version_info.get('version_id', 'unknown')}")
    print(f"标题: {fields['版本标题'][:30]}...")
    print(f"平台: {fields['平台']}")
    print(f"字数: {fields['字数']}")
    
    return fields

def sync_all_versions():
    """同步所有改写版本到Bitable"""
    mgr = RewriteVersionManager()
    versions = mgr.list_all_versions()
    
    print(f"共有 {len(versions)} 个版本需要同步")
    print()
    
    for v in versions:
        fields = sync_version_to_bitable(v)
        print(f"\n版本 {v.get('version_id')}: {v.get('platform')} - {v.get('account')}")
        print(f"字段预览: {json.dumps({k: str(v)[:50] for k, v in fields.items()}, ensure_ascii=False)}")
        print("-" * 60)

if __name__ == "__main__":
    sync_all_versions()
