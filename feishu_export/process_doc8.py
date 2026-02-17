#!/usr/bin/env python3
"""处理文档 8"""

import asyncio
from playwright.async_api import async_playwright

output_dir = "/Users/chenyd11/.openclaw/workspace/feishu_export/images"
doc_url = "https://my.feishu.cn/docx/N1mfdzICzoOJXmxgZ91cSBohn7g"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()
        
        print(f"处理文档 8: {doc_url}")
        
        # 打开文档
        await page.goto(doc_url, timeout=60000)
        await page.wait_for_timeout(8000)
        
        # 获取标题
        title = await page.title()
        print(f"文档标题: {title}")
        
        # 截图完整页面
        screenshot_path = f"{output_dir}/doc8_full.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"✓ 已保存完整页面截图: {screenshot_path}")
        
        # 查找所有图片
        images = await page.query_selector_all('img')
        print(f"找到 {len(images)} 个 img 标签")
        
        # 截图每个图片
        image_list = []
        for i, img in enumerate(images):
            try:
                bbox = await img.bounding_box()
                if bbox and bbox['width'] > 50 and bbox['height'] > 50:
                    img_path = f"{output_dir}/doc8_img{i+1}.png"
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
        
        print(f"\n文档 8 处理完成，共提取 {len(image_list)} 张图片")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
