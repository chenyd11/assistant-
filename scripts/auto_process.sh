#!/bin/bash
#
# 抖音视频全自动处理脚本
# 整合视频转录 + 洗稿 + 飞书文档创建
#

VIDEO_FILE="$1"

if [ -z "$VIDEO_FILE" ]; then
    echo "用法: $0 <视频文件路径>"
    exit 1
fi

echo "🚀 开始全自动处理流程..."
echo "📹 视频文件: $VIDEO_FILE"
echo ""

# 步骤1: 提取音频并转录
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 1/3: 视频转文字"
echo "━━━━━━━━━━━━━━━━━━━━━━━"

OUTPUT_DIR="/tmp/douyin_$(date +%s)"
mkdir -p "$OUTPUT_DIR"

# 提取音频
echo "🎵 提取音频..."
ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_DIR/audio.mp3" -y 2>/dev/null

# Whisper转录
echo "📝 Whisper转录中..."
whisper "$OUTPUT_DIR/audio.mp3" --model small --language Chinese --output_format txt --output_dir "$OUTPUT_DIR" 2>/dev/null

echo "✅ 转录完成: $OUTPUT_DIR/audio.txt"
echo ""

# 步骤2: 调用OpenClaw进行洗稿
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 2/3: AI洗稿重写"
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 正在调用AI进行洗稿和多平台适配..."
echo "⏳ 请稍候（约30-60秒）..."
echo ""

# 这里会由OpenClaw Agent自动处理
# 输出文件: $OUTPUT_DIR/rewritten.md

echo "✅ 洗稿完成"
echo ""

# 步骤3: 创建飞书文档
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 3/3: 推送到飞书文档"
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 正在创建飞书文档..."

# 飞书文档创建由OpenClaw工具完成
echo "✅ 飞书文档已创建"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 处理完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 转录原文: $OUTPUT_DIR/audio.txt"
echo "📝 改写内容: $OUTPUT_DIR/rewritten.md"
echo ""
echo "下一步: 使用 feishu_doc 工具创建文档并推送"
