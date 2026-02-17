# 抖音视频转三平台内容 - 完整系统

## 🎯 核心功能

1. **视频库管理** - 编号存储视频和转录文本，可复用
2. **三平台分发** - 公众号 + 小红书（多账号）+ 抖音（多账号）
3. **自动格式化** - 根据平台特点自动调整内容格式

---

## 📁 项目结构

```
workspace/
├── library/                      # 视频库
│   ├── db.json                   # 数据库
│   ├── videos/                   # 视频文件
│   ├── transcripts/              # 转录文本
│   ├── rewritten/                # 改写后内容
│   ├── video_lib.py              # 库管理脚本
│   └── example_usage.py          # 使用示例
│
├── publisher/                    # 发布工具
│   ├── triple_config.json        # 账号配置
│   ├── triple_platform.py        # 三平台发布器
│   └── scripts/                  # 生成的发布脚本
│       └── 20260215_xxxxxx/
│           ├── wechat_wechat_1.py
│           ├── xiaohongshu_xiaohongshu_1.py
│           ├── xiaohongshu_xiaohongshu_2.py
│           ├── douyin_douyin_1.py
│           ├── douyin_douyin_2.py
│           └── publish_all.sh    # 一键运行
│
└── README.md
```

---

## 🚀 使用流程

### 1. 视频入库

```python
import sys
sys.path.insert(0, 'library')
from video_lib import VideoLibrary

lib = VideoLibrary()

# 添加视频
video_id = lib.add_video(
    'video.mp4',
    '视频标题',
    source_url='https://v.douyin.com/xxxxx',
    tags=['标签1', '标签2']
)
# 返回: VID_2026_0001_xxxxx

# 添加转录文本
lib.add_transcript(video_id, '转录的文本内容...')

# 添加改写版本
lib.add_rewritten(video_id, 'wechat', '公众号文章内容')
lib.add_rewritten(video_id, 'xiaohongshu', '小红书内容')
lib.add_rewritten(video_id, 'douyin', '抖音内容')
```

### 2. 配置发布账号

```bash
# 添加公众号（通常只有一个）
python3 publisher/triple_platform.py add wechat "我的公众号" "主公众号"

# 添加小红书多账号
python3 publisher/triple_platform.py add xiaohongshu "个人生活号" "日常分享"
python3 publisher/triple_platform.py add xiaohongshu "职场干货号" "求职内容"

# 添加抖音多账号
python3 publisher/triple_platform.py add douyin "主账号" "日常内容"
python3 publisher/triple_platform.py add douyin "小号" "测试内容"

# 查看所有账号
python3 publisher/triple_platform.py accounts
```

### 3. 创建发布计划并生成脚本

```python
from publisher.triple_platform import TriplePlatformPublisher

publisher = TriplePlatformPublisher()

# 定义内容
content = {
    'title': '文章标题',
    'body': '文章内容...',
    'tags': ['标签1', '标签2', '标签3']
}

# 创建发布计划
plan = publisher.create_publish_plan(content)

# 生成发布脚本
output_dir = publisher.generate_publish_scripts(plan)
```

### 4. 执行发布

```bash
# 一键发布到所有平台
./publisher/scripts/20260215_xxxxxx/publish_all.sh

# 或单独发布某个平台
python3 publisher/scripts/20260215_xxxxxx/xiaohongshu_xiaohongshu_1.py
```

---

## 📝 平台格式对比

| 平台 | 格式特点 | 长度限制 | 账号支持 |
|------|----------|----------|----------|
| **公众号** | 富文本HTML | 无限制 | 单账号 |
| **小红书** | Markdown+emoji | 1000字 | **多账号** |
| **抖音** | 超短文本 | 500字 | **多账号** |

### 格式转换示例

**原始内容：**
```
第一点，厂名叫什么？不敢说的直接拉黑。
第二点，地址在哪？写字楼面试都是中介套路。
```

**小红书版：**
```
1️⃣第一点，厂名叫什么？不敢说的直接拉黑。

2️⃣第二点，地址在哪？写字楼面试都是中介套路。
```

**抖音版：**
```
第一，厂名叫什么？不敢说的直接拉黑。
第二，地址在哪？写字楼面试都是中介套路。
```

---

## 📊 当前状态

### 视频库
- ✅ 已入库视频: 1个
- ✅ 已转录: 1个
- ✅ 编号系统: VID_2026_XXXX

### 发布账号
- ✅ 公众号: 1个
- ✅ 小红书: 2个账号
- ✅ 抖音: 2个账号

### 已生成发布脚本
- ✅ 5个平台脚本（1公众号+2小红书+2抖音）

---

## 🔄 完整工作流

```
┌─────────────┐
│ 1. 视频入库  │ → 编号: VID_2026_0001_xxxxx
└──────┬──────┘
       ↓
┌─────────────┐
│ 2. 转录文本  │ → 保存到 library/transcripts/
└──────┬──────┘
       ↓
┌─────────────┐
│ 3. AI洗稿   │ → 生成3平台版本
└──────┬──────┘
       ↓
┌─────────────┐
│ 4. 入库保存  │ → 保存到 library/rewritten/
└──────┬──────┘
       ↓
┌─────────────┐
│ 5. 生成脚本  │ → publisher/scripts/日期/
└──────┬──────┘
       ↓
┌─────────────┐
│ 6. 一键发布  │ → publish_all.sh
└─────────────┘
```

---

## 🎨 后续优化方向

1. **浏览器自动化** - 使用Playwright自动登录和发布
2. **定时发布** - 支持预约发布时间
3. **数据分析** - 追踪各平台阅读/互动数据
4. **模板系统** - 保存常用发布模板
5. **批量入库** - 一次处理多个视频

---

## 💡 使用建议

1. **视频入库时添加详细标签** - 方便日后搜索和分类
2. **账号备注写清楚用途** - 区分不同账号的定位
3. **内容改写后保存到库** - 形成可复用的内容资产
4. **发布脚本定期清理** - 避免scripts目录堆积

---

**当前已完成：**
- ✅ 视频库（编号系统）
- ✅ 三平台发布工具（支持多账号）
- ✅ 自动格式转换
- ✅ 发布脚本生成

**待接入：**
- ⏳ 浏览器自动化发布
- ⏳ 飞书文档推送
- ⏳ AI洗稿（根据你的风格调整）
