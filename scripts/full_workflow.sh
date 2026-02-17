#!/bin/bash
#
# 完整工作流脚本
# 视频入库 → 转录 → 洗稿 → 生成发布计划
#

VIDEO_FILE="$1"
TITLE="$2"

if [ -z "$VIDEO_FILE" ] || [ -z "$TITLE" ]; then
    echo "用法: $0 <视频文件> <标题>"
    echo "示例: $0 video.mp4 '进厂打工避坑指南'"
    exit 1
fi

SCRIPT_DIR="/Users/chenyd11/.openclaw/workspace"
cd "$SCRIPT_DIR"

echo "🚀 开始完整工作流"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 步骤1: 视频入库
echo "📥 步骤 1/4: 视频入库"
python3 -c "
import sys
sys.path.insert(0, 'library')
from video_lib import VideoLibrary

lib = VideoLibrary()
video_id = lib.add_video('$VIDEO_FILE', '$TITLE')
print(f'VIDEO_ID={video_id}')
" > /tmp/video_id.txt

VIDEO_ID=$(cat /tmp/video_id.txt | grep VIDEO_ID= | cut -d= -f2)
echo "   视频编号: $VIDEO_ID"
echo ""

# 步骤2: 转录
echo "🎵 步骤 2/4: 视频转录"
OUTPUT_DIR="/tmp/douyin_$(date +%s)"
mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_DIR/audio.mp3" -y 2>/dev/null
whisper "$OUTPUT_DIR/audio.mp3" --model small --language Chinese --output_format txt --output_dir "$OUTPUT_DIR" 2>/dev/null

TRANSCRIPT=$(cat "$OUTPUT_DIR/audio.txt")
echo "   转录完成，字数: ${#TRANSCRIPT}"

# 保存转录文本
python3 -c "
import sys
sys.path.insert(0, 'library')
from video_lib import VideoLibrary

lib = VideoLibrary()
with open('$OUTPUT_DIR/audio.txt', 'r') as f:
    transcript = f.read()
lib.add_transcript('$VIDEO_ID', transcript)
"
echo "   已保存到库"
echo ""

# 步骤3: 洗稿（需要AI处理，这里输出提示）
echo "📝 步骤 3/4: 洗稿重写"
echo "   转录文本已保存，请使用AI进行洗稿"
echo "   视频编号: $VIDEO_ID"
echo "   转录文件: library/transcripts/${VIDEO_ID}.txt"
echo ""

# 步骤4: 生成发布计划（示例）
echo "📋 步骤 4/4: 生成发布计划"
python3 -c "
import sys
import json
sys.path.insert(0, 'publisher')
from multi_platform import MultiPlatformPublisher

publisher = MultiPlatformPublisher()

# 示例内容
content = {
    'title': '$TITLE',
    'body': '(洗稿后的内容将放在这里)',
    'tags': ['标签1', '标签2', '标签3']
}

plan = publisher.publish_plan(content)

# 生成发布脚本
script_path = publisher.generate_publish_script(plan)
print(f'发布脚本: {script_path}')
" > /tmp/plan_output.txt

cat /tmp/plan_output.txt
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 工作流完成"
echo ""
echo "下一步:"
echo "  1. 查看转录文本: cat library/transcripts/${VIDEO_ID}.txt"
echo "  2. 使用AI洗稿后保存到 library/rewritten/${VIDEO_ID}_*.md"
echo "  3. 运行发布脚本进行多平台分发"
echo ""
echo "视频编号: $VIDEO_ID"
