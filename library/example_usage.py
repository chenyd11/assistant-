#!/usr/bin/env python3
"""
视频库使用示例
"""

import sys
sys.path.insert(0, '/Users/chenyd11/.openclaw/workspace/library')
from video_lib import VideoLibrary

# 初始化库
lib = VideoLibrary()

# 显示库摘要
print("=" * 60)
print("📚 视频库管理工具")
print("=" * 60)
print()
print("可用命令:")
print()
print("1. 添加视频到库:")
print("   python3 library/video_lib.py")
print("   (然后在Python中调用 lib.add_video('path/to/video.mp4', '标题'))")
print()
print("2. 查看库摘要:")
print("   python3 library/video_lib.py summary")
print()
print("3. 列出所有视频:")
print("   python3 library/video_lib.py list")
print()
print("4. 搜索视频:")
print("   python3 library/video_lib.py search <关键词>")
print()
print("5. 获取视频详情:")
print("   python3 library/video_lib.py get <视频编号>")
print()

# 显示当前库状态
lib.print_summary()
