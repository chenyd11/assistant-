#!/usr/bin/env python3
"""
飞书文档自动创建和推送脚本
"""

import sys
import json

# 读取输入参数
if len(sys.argv) < 4:
    print("用法: python3 push_to_feishu.py <标题> <公众号内容> <小红书内容> <抖音内容>")
    sys.exit(1)

title = sys.argv[1]
wechat_content = sys.argv[2]
xiaohongshu_content = sys.argv[3]
douyin_content = sys.argv[4]

# 构建Markdown内容
markdown_content = f"""# {title}

> 本文由AI自动从抖音视频转录并改写生成

---

## 版本一：公众号长文

{wechat_content}

---

## 版本二：小红书图文

{xiaohongshu_content}

---

## 版本三：抖音图文

{douyin_content}

---

*生成时间：自动生成*
"""

print(markdown_content)
print("\n" + "="*50)
print("✅ 内容已生成，请调用 feishu_doc 工具创建文档")
