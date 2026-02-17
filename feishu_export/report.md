# 飞书文档图片提取报告

## 任务概述
- 处理文档数：8 个
- 提取图片总数：8 张
- 输出目录：/Users/chenyd11/.openclaw/workspace/feishu_export/images/

---

## 文档处理详情

### 文档 1
- **URL**: https://my.feishu.cn/docx/FaCTdkKBfol6upx2CYTciFcpnrd
- **标题**: 让新人无痛入局，用 AI 写出一部网络小说
- **图片数量**: 0 张
- **说明**: 文档中没有找到尺寸大于 50x50 像素的图片

### 文档 2
- **URL**: https://lv9qj6hfr4z.feishu.cn/docx/VEZQdB4oRo0xIlxQgxscQibLng9
- **标题**: 【ai写作】 我用ai写爽文小说 赚到第一笔小说稿费的故事 全文拆解我的思路和流程
- **图片数量**: 2 张
- **提取图片**:
  1. `doc2_img1.png` (472×324 像素)
  2. `doc2_img2.png` (324×324 像素)

### 文档 3
- **URL**: https://ub9lv2h75d.feishu.cn/docx/CNgvdtoKio8Pbqxcs3Wcuz04nhh
- **标题**: 短篇小说的本质是"情绪商品"，AI辅助写作、从拆解到变现的SOP分享
- **图片数量**: 1 张
- **提取图片**:
  1. `doc3_img1.png` (820×275 像素)

### 文档 4
- **URL**: https://my.feishu.cn/docx/RlLedKTwkoRE3yxG33ictYyInjc
- **标题**: 如何用脑洞文的思路为AI生成的小说加上好的创意
- **图片数量**: 0 张
- **说明**: 文档中没有找到尺寸大于 50x50 像素的图片

### 文档 5
- **URL**: https://my.feishu.cn/docx/Hjkmd6PWPozKo9xsQggce4wjnJe
- **标题**: AI小说-如何有效改稿：让你的作品更上一层楼
- **图片数量**: 0 张
- **说明**: 文档中没有找到尺寸大于 50x50 像素的图片

### 文档 6
- **URL**: https://my.feishu.cn/docx/T07HdgMvioUyLZxeHcUcXYo2nYg
- **标题**: 如何解决 AI 生成的短篇小说"AI 味"，让小说更有"人味"
- **图片数量**: 2 张
- **提取图片**:
  1. `doc6_img1.png` (314×553 像素)
  2. `doc6_img2.png` (308×467 像素)

### 文档 7
- **URL**: https://my.feishu.cn/docx/MGtIdI9XeoRFJoxA34xcr31enBe
- **标题**: 如何解决 AI 生成的短篇小说"AI 味"，让小说更有"人味"
- **图片数量**: 2 张
- **提取图片**:
  1. `doc7_img1.png` (314×553 像素)
  2. `doc7_img2.png` (308×467 像素)

### 文档 8
- **URL**: https://my.feishu.cn/docx/N1mfdzICzoOJXmxgZ91cSBohn7g
- **标题**: 我是如何用AI找到适合自己的副业：一个普通人的AI成长经历
- **图片数量**: 1 张
- **提取图片**:
  1. `doc8_img1.png` (820×588 像素)

---

## 提取图片完整路径列表

```
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc2_img1.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc2_img2.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc3_img1.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc6_img1.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc6_img2.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc7_img1.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc7_img2.png
/Users/chenyd11/.openclaw/workspace/feishu_export/images/doc8_img1.png
```

---

## 完整页面截图（额外保存）

除单独提取的图片外，还保存了每个文档的完整页面截图：

- `doc1_full.png` - 让新人无痛入局，用 AI 写出一部网络小说
- `doc1_page1.png` ~ `doc1_page10.png` - 文档 1 的分页截图
- `doc2_full.png` - 【ai写作】 我用ai写爽文小说...
- `doc3_full.png` - 短篇小说的本质是"情绪商品"...
- `doc4_full.png` - 如何用脑洞文的思路为AI生成的小说加上好的创意
- `doc5_full.png` - AI小说-如何有效改稿...
- `doc6_full.png` - 如何解决 AI 生成的短篇小说"AI 味"...
- `doc7_full.png` - 如何解决 AI 生成的短篇小说"AI 味"...
- `doc8_full.png` - 我是如何用AI找到适合自己的副业...

---

## 技术说明

- **连接方式**: Chrome CDP (端口 9222)
- **图片筛选条件**: 尺寸大于 50×50 像素的可见图片
- **命名格式**: doc{文档序号}_img{图片序号}.png
- **处理时间**: 2025-02-16
