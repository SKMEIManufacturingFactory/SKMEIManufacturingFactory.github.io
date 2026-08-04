import os
import re

html_files = [
    "index.html",
    "about.html",
    "products.html"
]

for file in html_files:

    if not os.path.exists(file):
        print("Not found:", file)
        continue

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换图片目录
    content = content.replace(
        'images/',
        'images_webp/'
    )

    # 替换图片格式
    content = re.sub(
        r'\.(jpg|jpeg|JPG|JPEG|png|PNG)',
        '.webp',
        content
    )

    # 添加懒加载（避免重复添加）
    content = content.replace(
        '<img ',
        '<img loading="lazy" '
    )

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated:", file)

print("Done")