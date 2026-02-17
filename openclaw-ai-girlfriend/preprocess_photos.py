#!/usr/bin/env python3
"""
照片预处理脚本 - 自动裁剪/去字幕
"""

import os
import cv2
import numpy as np
from pathlib import Path

def remove_subtitles(image_path, output_path):
    """
    尝试检测并去除底部字幕区域
    策略: 检测图片底部 10-15% 区域，如果有大量文字特征就裁剪掉
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取: {image_path}")
        return False
    
    height, width = img.shape[:2]
    
    # 策略1: 裁剪底部 15% (常见字幕位置)
    # 如果检测到底部有明显文字特征，裁剪掉
    bottom_region = img[int(height*0.82):, :]
    
    # 转换为灰度，检测边缘密度(文字有很多边缘)
    gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # 如果底部边缘密度高(可能是字幕)，裁剪掉底部 15%
    if edge_density > 0.05:  # 阈值可调
        print(f"  检测到字幕，裁剪底部 15%")
        img = img[:int(height*0.85), :]
    
    # 保存
    cv2.imwrite(output_path, img)
    return True

def preprocess_images(input_dir, output_dir):
    """预处理所有照片"""
    os.makedirs(output_dir, exist_ok=True)
    
    image_files = list(Path(input_dir).glob("*.jpg")) + \
                  list(Path(input_dir).glob("*.png")) + \
                  list(Path(input_dir).glob("*.jpeg"))
    
    print(f"找到 {len(image_files)} 张照片")
    print("开始处理...\n")
    
    for i, img_path in enumerate(image_files, 1):
        output_path = os.path.join(output_dir, f"{i:02d}.jpg")
        print(f"[{i}/{len(image_files)}] {img_path.name}")
        
        if remove_subtitles(str(img_path), output_path):
            print(f"  ✅ 已保存到: {output_path}")
        else:
            print(f"  ❌ 处理失败")
    
    print(f"\n✅ 处理完成! 照片保存在: {output_dir}")

if __name__ == "__main__":
    # 使用示例
    input_folder = "raw_photos"      # 你放原始照片的地方
    output_folder = "training_images" # 处理后用于训练的照片
    
    print("="*50)
    print("📸 照片预处理工具")
    print("="*50)
    print(f"输入: {input_folder}")
    print(f"输出: {output_folder}")
    print("="*50 + "\n")
    
    preprocess_images(input_folder, output_folder)
