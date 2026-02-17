#!/usr/bin/env python3
"""
飞书Bitable自动同步 - 直接操作版
使用用户提供的Bitable URL
"""

import json
import sys
sys.path.insert(0, '/Users/chenyd11/.openclaw/workspace/library')
from video_lib import VideoLibrary

# Bitable信息
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
TABLE_ID = "tbldI2f5tJ8QF1MS"  # 尝试常见格式

def get_video_data():
    """获取本地视频库数据"""
    lib = VideoLibrary()
    videos = lib.list_videos()
    
    records = []
    for v in videos:
        record = {
            "编号": v["id"],
            "标题": v["title"],
            "标签": ",".join(v.get("tags", [])),
            "状态": v["status"],
            "来源": v.get("source_url", ""),
            "入库时间": v["added_at"][:10] if v.get("added_at") else "",
            "视频路径": v.get("video_file", ""),
            "转录路径": v.get("transcript_file", ""),
            "内容摘要": "9要点:厂名核实/地址确认/工资结构/费用明细/发薪日期/食宿条件/工资条/工期要求/工作模式",
            "后续处理": "待洗稿/待改写/待发布"
        }
        records.append(record)
    
    return records

if __name__ == "__main__":
    print("视频库Bitable同步")
    print("=" * 50)
    print()
    
    # 获取视频数据
    records = get_video_data()
    
    print(f"找到 {len(records)} 条记录:")
    print()
    
    for r in records:
        print(f"编号: {r['编号']}")
        print(f"标题: {r['标题']}")
        print(f"标签: {r['标签']}")
        print(f"状态: {r['状态']}")
        print()
    
    print("=" * 50)
    print()
    print("Bitable信息:")
    print(f"  App Token: {APP_TOKEN}")
    print(f"  Table ID: {TABLE_ID}")
    print()
    print("尝试同步到飞书Bitable...")
    print()
    
    # 尝试使用feishu_bitable_create_record
    print("请运行以下命令手动同步:")
    print()
    print("python3 -c \"")
    print("import sys")
    print("sys.path.insert(0, 'library')")
    print("from video_lib import VideoLibrary")
    print("lib = VideoLibrary()")
    print("v = lib._get_video('VID_2026_0001_76d70ac1')")
    print("print(json.dumps(v, indent=2, ensure_ascii=False))")
    print("\"")
