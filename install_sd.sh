#!/bin/bash
# Stable Diffusion WebUI 安装脚本 (MacBook Air Apple Silicon)

echo "========================================"
echo "🎨 Stable Diffusion WebUI 安装"
echo "========================================"
echo ""

# 安装目录
INSTALL_DIR="$HOME/.openclaw/workspace/stable-diffusion-webui"

echo "📁 安装目录: $INSTALL_DIR"
echo ""

# 检查是否已安装
if [ -d "$INSTALL_DIR" ]; then
    echo "✅ SD WebUI 已安装"
    echo "启动命令: cd $INSTALL_DIR && ./webui.sh --api"
    exit 0
fi

# 克隆仓库
echo "⬇️  下载 Stable Diffusion WebUI..."
cd ~/.openclaw/workspace
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

# 安装依赖
echo "📦 安装依赖..."
cd stable-diffusion-webui

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 PyTorch (Apple Silicon 版本)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 安装其他依赖
pip install -r requirements.txt

echo ""
echo "✅ 安装完成!"
echo ""
echo "========================================"
echo "🚀 启动命令:"
echo "   cd $INSTALL_DIR"
echo "   ./webui.sh --api --no-half"
echo "========================================"
