import os
import sys
from PIL import Image
from pathlib import Path

# 设置源文件夹（原始图片）和目标文件夹（WebP输出）
SOURCE_DIR = "images"
TARGET_DIR = "images_webp"

# 支持的图片格式
SUPPORTED_EXT = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

# 检查是否带有 --force 参数（强制覆盖所有图片）
FORCE = '--force' in sys.argv

def convert_to_webp(source_path, target_path):
    # 如果不是强制模式，且目标文件已存在，则跳过
    if not FORCE and os.path.exists(target_path):
        print(f"⏭️  跳过已存在: {target_path}")
        return False

    try:
        with Image.open(source_path) as img:
            # 处理透明背景（PNG）
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            
            # 保存为 WebP，质量 80（可调整）
            img.save(target_path, 'webp', quality=80, method=6)
            print(f"✅ 转换成功: {source_path} -> {target_path}")
            return True
    except Exception as e:
        print(f"❌ 转换失败: {source_path} - 错误: {e}")
        return False

def main():
    total = 0
    converted = 0
    skipped = 0

    # 遍历源文件夹
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in SUPPORTED_EXT:
                continue

            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, SOURCE_DIR)
            target_path = os.path.join(TARGET_DIR, os.path.splitext(relative_path)[0] + '.webp')

            # 确保目标文件夹存在
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            total += 1
            if convert_to_webp(source_path, target_path):
                converted += 1
            else:
                skipped += 1

    print(f"\n📊 统计: 总共扫描 {total} 张图片，新转换 {converted} 张，跳过 {skipped} 张（已存在）")

if __name__ == "__main__":
    main()