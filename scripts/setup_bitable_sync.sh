#!/bin/bash
#
# 视频库飞书Bitable同步配置脚本
#

echo "=========================================="
echo "视频库 - 飞书Bitable自动同步配置"
echo "=========================================="
echo ""

# 检查表格URL
BITABLE_URL="https://fcnrncf2hy2l.feishu.cn/base/V87Cb06erar7kGsTFm0cR0JZnof"
APP_TOKEN="V87Cb06erar7kGsTFm0cR0JZnof"

echo "📊 Bitable信息:"
echo "   URL: $BITABLE_URL"
echo "   App Token: $APP_TOKEN"
echo ""

echo "⚠️  需要完成的配置步骤:"
echo ""
echo "1. 创建飞书应用（如果还没有）"
echo "   访问: https://open.feishu.cn/app"
echo "   点击: 创建企业自建应用"
echo ""
echo "2. 获取应用凭证"
echo "   在应用详情页 → 凭证与基础信息"
echo "   复制: App ID 和 App Secret"
echo ""
echo "3. 添加Bitable权限"
echo "   在应用详情页 → 权限管理"
echo "   添加以下权限:"
echo "   - bitable:record:read"
echo "   - bitable:record:write"
echo "   - bitable:table:read"
echo ""
echo "4. 发布应用"
echo "   在应用详情页 → 版本管理与发布"
echo "   点击: 创建版本 → 申请发布"
echo ""
echo "5. 配置环境变量"
echo "   export FEISHU_APP_ID=cli_xxxxx"
echo "   export FEISHU_APP_SECRET=xxxxxxxxxx"
echo ""
echo "6. 授权应用访问表格"
echo "   在Bitable表格中 → 设置 → 权限"
echo "   添加应用: 选择你创建的应用"
echo ""
echo "7. 运行同步脚本"
echo "   python3 scripts/sync_to_bitable.py"
echo ""
echo "=========================================="
echo ""
echo "当前视频库数据预览:"
echo ""

# 显示当前视频
python3 -c "
import sys
sys.path.insert(0, 'library')
from video_lib import VideoLibrary

lib = VideoLibrary()
videos = lib.list_videos()

print(f'共有 {len(videos)} 个视频:\\n')
for v in videos:
    print(f'编号: {v[\"id\"]}')
    print(f'标题: {v[\"title\"]}')
    print(f'状态: {v[\"status\"]}')
    print(f'标签: {', '.join(v.get('tags', []))}')
    print()
"

echo ""
echo "配置完成后，每次新视频入库将自动同步到飞书Bitable!"
