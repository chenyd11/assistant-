#!/usr/bin/env python3
"""
视频库自动同步到飞书Bitable - 修复版
修复问题：
1. 标签和状态用中文名称而非代码
2. 时间戳用毫秒格式
3. 转录路径直接放文字内容
"""

import json
import sys
import os

# 添加库路径
sys.path.insert(0, '/Users/chenyd11/.openclaw/workspace/library')
from video_lib import VideoLibrary

# Bitable配置
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
TABLE_ID = "tbl49MRT9hEVlCVX"

def sync_video_to_bitable(video_id):
    """同步单个视频到Bitable"""
    
    lib = VideoLibrary()
    video = lib._get_video(video_id)
    
    if not video:
        print(f"❌ 未找到视频: {video_id}")
        return False
    
    # 获取转录文本
    transcript = lib.get_transcript(video_id) or "（暂无转录文本）"
    
    # 截取前500字作为内容
    transcript_preview = transcript[:500] + "..." if len(transcript) > 500 else transcript
    
    # 构建字段 - 使用正确格式
    from datetime import datetime
    
    fields = {
        "文本": video["title"][:20] if len(video["title"]) > 20 else video["title"],
        "视频唯一编号": video["id"],
        "标题": video["title"],
        "标签": ["教育"],  # 使用中文标签名称
        "状态": "已转录",  # 使用中文状态名称
        "来源": {
            "text": "查看抖音链接",
            "link": video.get("source_url", "")
        } if video.get("source_url") else None,
        "入库时间": int(datetime.now().timestamp() * 1000),  # 毫秒时间戳
        "视频路径": f"视频文件: {video.get('video_file', '未保存')}",
        "转录路径": transcript_preview,  # 直接放文字内容
        "内容摘要": "9要点:厂名核实/地址确认/工资结构/费用明细/发薪日期/食宿条件/工资条/工期要求/工作模式",
        "后续处理": "待洗稿/待改写/待发布"
    }
    
    # 移除空值
    fields = {k: v for k, v in fields.items() if v is not None}
    
    print(f"准备同步视频: {video_id}")
    print(f"标题: {video['title']}")
    print(f"字段预览: {json.dumps({k: str(v)[:50] for k, v in fields.items()}, ensure_ascii=False)}")
    
    # 这里输出字段，供调用者使用
    return fields

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_id = sys.argv[1]
        fields = sync_video_to_bitable(video_id)
        if fields:
            print("\n✅ 同步数据已生成:")
            print(json.dumps(fields, ensure_ascii=False))
    else:
        # 同步所有视频
        lib = VideoLibrary()
        videos = lib.list_videos()
        print(f"共有 {len(videos)} 个视频需要同步")
        for v in videos:
            print(f"\n处理: {v['id']}")
            fields = sync_video_to_bitable(v['id'])
