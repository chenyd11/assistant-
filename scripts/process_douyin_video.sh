#!/bin/bash
#
# 抖音视频处理脚本
# 输入：视频文件路径
# 输出：飞书文档链接
#

set -e

VIDEO_PATH="$1"
OUTPUT_DIR="/tmp/douyin_process_$(date +%s)"
mkdir -p "$OUTPUT_DIR"

echo "🎬 开始处理视频: $VIDEO_PATH"

# 1. 提取音频
echo "🎵 提取音频..."
ffmpeg -i "$VIDEO_PATH" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_DIR/audio.mp3" -y 2>/dev/null

# 2. 语音转文字
echo "📝 语音转文字 (Whisper)..."
whisper "$OUTPUT_DIR/audio.mp3" --model small --language Chinese --output_format txt --output_dir "$OUTPUT_DIR" 2>/dev/null

echo "✅ 转录完成！"
echo "📄 文本文件: $OUTPUT_DIR/audio.txt"

# 3. 显示前500字预览
echo ""
echo "📝 转录内容预览："
echo "---"
head -c 500 "$OUTPUT_DIR/audio.txt" 2>/dev/null || cat "$OUTPUT_DIR/audio.txt" 2>/dev/null | head -20
echo "..."
echo "---"

echo ""
echo "💡 提示：请使用OpenClaw的sessions_spawn进行洗稿重写"
echo "   输入文件: $OUTPUT_DIR/audio.txt"
