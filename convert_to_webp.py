import os
import sys
from PIL import Image

SOURCE_DIR = "images"
TARGET_DIR = "images_webp"
SUPPORTED_EXT = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
FORCE = '--force' in sys.argv

# ★★★ 全能优化参数（兼顾欧美画质 + 移动端速度） ★★★
MAX_WIDTH = 1200      # 移动端友好，桌面 Retina 也够用
MAX_HEIGHT = 1200
QUALITY = 82          # 介于 75 和 85 之间的黄金平衡点

def resize_and_convert(source_path, target_path):
    if not FORCE and os.path.exists(target_path):
        print(f"⏭️  跳过已存在: {target_path}")
        return False

    try:
        with Image.open(source_path) as img:
            original_size = f"{img.width}x{img.height}"
            
            # 等比例缩放
            if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
                print(f"📐 缩放: {original_size} → {img.width}x{img.height}")

            # 处理透明度
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            
            # ★★★ 质量 82（兼顾欧美画质 + 移动端速度） ★★★
            img.save(target_path, 'webp', quality=QUALITY, method=6)
            print(f"✅ 转换成功: {source_path} -> {target_path}")
            return True
    except Exception as e:
        print(f"❌ 转换失败: {source_path} - 错误: {e}")
        return False

def main():
    total = 0
    converted = 0
    skipped = 0
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in SUPPORTED_EXT:
                continue
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, SOURCE_DIR)
            target_path = os.path.join(TARGET_DIR, os.path.splitext(relative_path)[0] + '.webp')
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            total += 1
            if resize_and_convert(source_path, target_path):
                converted += 1
            else:
                skipped += 1
    print(f"\n📊 统计: 总共扫描 {total} 张，新转换 {converted} 张，跳过 {skipped} 张")
    print(f"🎯 优化参数: 尺寸 ≤ {MAX_WIDTH}x{MAX_HEIGHT}px，质量 {QUALITY}（兼顾欧美画质 + 移动端速度）")

if __name__ == "__main__":
    main()