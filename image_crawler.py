#!/usr/bin/env python3
"""
图片搜索爬虫 - 用于 LoRA 训练数据收集
注意：请遵守网站服务条款和版权法规
"""

import requests
from bs4 import BeautifulSoup
import os
import time
import random
from urllib.parse import urljoin, urlparse

class ImageCrawler:
    def __init__(self):
        self.session = requests.Session()
        # 伪装浏览器请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(self.headers)
        
    def search_duckduckgo(self, query, max_results=10):
        """从 DuckDuckGo 搜索图片链接"""
        print(f"🔍 搜索: {query}")
        
        # 构造搜索 URL
        search_url = f"https://duckduckgo.com/"
        params = {'q': query}
        
        try:
            # 第一步：获取 token
            response = self.session.get(search_url, params=params, timeout=10)
            time.sleep(random.uniform(2, 4))  # 随机延迟
            
            # 尝试从页面提取图片
            soup = BeautifulSoup(response.text, 'html.parser')
            images = []
            
            # 查找图片元素
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http'):
                    images.append({
                        'url': src,
                        'alt': img.get('alt', '')
                    })
                    if len(images) >= max_results:
                        break
            
            print(f"✅ 找到 {len(images)} 张图片")
            return images
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def search_bing(self, query, max_results=10):
        """从 Bing 搜索图片链接（更友好）"""
        print(f"🔍 Bing 搜索: {query}")
        
        search_url = "https://www.bing.com/images/search"
        params = {'q': query}
        
        try:
            response = self.session.get(search_url, params=params, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            images = []
            # Bing 图片通常在 murl 属性中
            for a in soup.find_all('a', class_='iusc'):
                m = a.get('m')
                if m:
                    import json
                    try:
                        data = json.loads(m)
                        img_url = data.get('murl')
                        if img_url:
                            images.append({
                                'url': img_url,
                                'alt': data.get('desc', '')
                            })
                            if len(images) >= max_results:
                                break
                    except:
                        pass
            
            print(f"✅ Bing 找到 {len(images)} 张图片")
            return images
            
        except Exception as e:
            print(f"❌ Bing 搜索失败: {e}")
            return []
    
    def download_image(self, url, output_dir, filename):
        """下载单张图片"""
        try:
            # 随机延迟，避免触发限制
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=15, stream=True)
            
            if response.status_code == 200:
                # 确定文件扩展名
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'webp' in content_type:
                    ext = '.webp'
                else:
                    ext = '.jpg'
                
                filepath = os.path.join(output_dir, f"{filename}{ext}")
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ 下载成功: {filepath}")
                return filepath
            else:
                print(f"❌ HTTP {response.status_code}: {url}")
                return None
                
        except Exception as e:
            print(f"❌ 下载失败: {url} - {e}")
            return None
    
    def crawl_images(self, query, output_dir, max_images=10):
        """完整的爬取流程"""
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🚀 开始爬取: {query}")
        print(f"📁 保存到: {output_dir}")
        print("-" * 50)
        
        # 尝试多个搜索引擎
        all_images = []
        
        # Bing（更友好）
        bing_images = self.search_bing(query, max_results=max_images)
        all_images.extend(bing_images)
        
        if len(all_images) < max_images:
            # DuckDuckGo
            ddg_images = self.search_duckduckgo(query, max_results=max_images - len(all_images))
            all_images.extend(ddg_images)
        
        # 去重
        seen_urls = set()
        unique_images = []
        for img in all_images:
            if img['url'] not in seen_urls:
                seen_urls.add(img['url'])
                unique_images.append(img)
        
        print(f"\n📊 共找到 {len(unique_images)} 张唯一图片")
        print("-" * 50)
        
        # 下载图片
        downloaded = []
        for i, img in enumerate(unique_images[:max_images], 1):
            print(f"\n[{i}/{min(len(unique_images), max_images)}] 下载: {img['url'][:60]}...")
            filepath = self.download_image(img['url'], output_dir, f"image_{i:03d}")
            if filepath:
                downloaded.append(filepath)
        
        print("\n" + "=" * 50)
        print(f"🎉 完成！成功下载 {len(downloaded)}/{max_images} 张图片")
        print(f"📂 保存位置: {output_dir}")
        
        return downloaded


def main():
    """主函数"""
    # 搜索关键词
    query = "Android 18 Dragon Ball"
    
    # 输出目录
    output_dir = "/Users/chenyd11/Desktop/android18_crawl"
    
    # 最大下载数量
    max_images = 10
    
    # 创建爬虫实例
    crawler = ImageCrawler()
    
    # 开始爬取
    downloaded = crawler.crawl_images(query, output_dir, max_images)
    
    return downloaded


if __name__ == "__main__":
    main()
