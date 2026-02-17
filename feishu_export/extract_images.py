#!/usr/bin/env python3
"""
飞书文档图片提取脚本
使用 Playwright 连接 CDP 端口并截图
"""

import asyncio
import os
from playwright.async_api import async_playwright

# 文档列表
docs = [
    "https://my.feishu.cn/docx/FaCTdkKBfol6upx2CYTciFcpnrd",
    "https://lv9qj6hfr4z.feishu.cn/docx/VEZQdB4oRo0xIlxQgxscQibLng9",
    "https://ub9lv2h75d.feishu.cn/docx/CNgvdtoKio8Pbqxcs3Wcuz04nhh",
    "https://my.feishu.cn/docx/RlLedKTwkoRE3yxG33ictYyInjc",
    "https://my.feishu.cn/docx/Hjkmd6PWPozKo9xsQggce4wjnJe",
    "https://my.feishu.cn/docx/T07HdgMvioUyLZxeHcUcXYo2nYg",
    "https://my.feishu.cn/docx/MGtIdI9XeoRFJoxA34xcr31enBe",
    "https://my.feishu.cn/docx/N1mfdzICzoOJXmxgZ91cSBohn7g",
]

output_dir = "/Users/chenyd11/.openclaw/workspace/feishu_export/images"
os.makedirs(output_dir, exist_ok=True)

async def extract_images_from_doc(page, doc_url, doc_index):
    """从文档中提取图片"""
    print(f"\n{'='*60}")
    print(f"处理文档 {doc_index}: {doc_url}")
    print(f"{'='*60}")
    
    # 打开文档
    await page.goto(doc_url, timeout=60000)
    await page.wait_for_timeout(5000)  # 等待页面加载
    
    # 获取文档标题
    title = await page.title()
    print(f"文档标题: {title}")
    
    # 滚动页面并截图
    screenshot_path = f"{output_dir}/doc{doc_index}_full.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"✓ 已保存完整页面截图: {screenshot_path}")
    
    # 查找所有图片元素
    images = await page.query_selector_all('img')
    print(f"找到 {len(images)} 个 img 标签")
    
    # 截图每个图片
    image_list = []
    for i, img in enumerate(images):
        try:
            # 检查图片是否可见且有尺寸
            bbox = await img.bounding_box()
            if bbox and bbox['width'] > 50 and bbox['height'] > 50:
                img_path = f"{output_dir}/doc{doc_index}_img{i+1}.png"
                await img.screenshot(path=img_path)
                image_list.append({
                    'index': i+1,
                    'path': img_path,
                    'width': bbox['width'],
                    'height': bbox['height']
                })
                print(f"  ✓ 图片 {i+1}: {bbox['width']}x{bbox['height']} -> {img_path}")
        except Exception as e:
            print(f"  ✗ 图片 {i+1} 截图失败: {e}")
    
    return {
        'doc_index': doc_index,
        'url': doc_url,
        'title': title,
        'image_count': len(image_list),
        'images': image_list
    }

async def main():
    async with async_playwright() as p:
        # 连接到 CDP 端口
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()
        
        print(f"已连接到 Chrome CDP 端口 9222")
        print(f"输出目录: {output_dir}")
        
        results = []
        
        # 处理每个文档
        for idx, doc_url in enumerate(docs, 1):
            try:
                result = await extract_images_from_doc(page, doc_url, idx)
                results.append(result)
            except Exception as e:
                print(f"✗ 文档 {idx} 处理失败: {e}")
                results.append({
                    'doc_index': idx,
                    'url': doc_url,
                    'title': 'Error',
                    'image_count': 0,
                    'images': [],
                    'error': str(e)
                })
        
        # 输出汇总
        print(f"\n{'='*60}")
        print("处理完成汇总")
        print(f"{'='*60}")
        for r in results:
            print(f"\n文档 {r['doc_index']}: {r['title']}")
            print(f"  URL: {r['url']}")
            print(f"  图片数量: {r['image_count']}")
            for img in r['images']:
                print(f"    - {img['path']} ({img['width']}x{img['height']})")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
