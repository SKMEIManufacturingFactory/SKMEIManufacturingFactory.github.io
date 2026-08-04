from PIL import Image

source = "images/LOGO.png"
output = "images_webp/LOGO.webp"

img = Image.open(source)

# 保留透明背景
if img.mode != "RGBA":
    img = img.convert("RGBA")

img.save(
    output,
    "WEBP",
    quality=90,
    method=6
)

print("Logo fixed")