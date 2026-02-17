#!/bin/bash
#
# 视频入库 + 自动同步到飞书Bitable
#

VIDEO_FILE="$1"
TITLE="$2"
SOURCE_URL="${3:-}"

if [ -z "$VIDEO_FILE" ] || [ -z "$TITLE" ]; then
    echo "用法: $0 <视频文件> <标题> [来源URL]"
    echo "示例: $0 video.mp4 '进厂打工避坑指南' 'https://v.douyin.com/xxxxx'"
    exit 1
fi

cd /Users/chenyd11/.openclaw/workspace

echo "=========================================="
echo "🎬 视频入库 + 自动同步到飞书Bitable"
echo "=========================================="
echo ""

# 1. 视频转录
echo "📝 步骤1: 视频转录..."
OUTPUT_DIR="/tmp/douyin_$(date +%s)"
mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_DIR/audio.mp3" -y 2>/dev/null
whisper "$OUTPUT_DIR/audio.mp3" --model small --language Chinese --output_format txt --output_dir "$OUTPUT_DIR" 2>/dev/null

echo "✅ 转录完成"
echo ""

# 2. 视频入库（自动同步到Bitable）
echo "📥 步骤2: 视频入库 + 同步到Bitable..."

python3 -c "
import sys
sys.path.insert(0, 'library')
from video_lib import VideoLibrary

lib = VideoLibrary()
video_id = lib.add_video(
    '$VIDEO_FILE',
    '$TITLE',
    source_url='$SOURCE_URL',
    tags=['待分类']
)

# 添加转录文本
with open('$OUTPUT_DIR/audio.txt', 'r') as f:
    transcript = f.read()
lib.add_transcript(video_id, transcript)

print(f'\n🎉 完成! 视频编号: {video_id}')
print('✅ 已自动同步到飞书Bitable')
"

echo ""
echo "=========================================="
echo "✅ 全部完成!"
echo "=========================================="
echo ""
echo "请查看飞书Bitable表格，新视频已自动添加:"
echo "https://fcnrncf2hy2l.feishu.cn/base/V87Cb06erar7kGsTFm0cR0JZnof"
