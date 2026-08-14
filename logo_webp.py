from PIL import Image

input_path = "images/LOGO.png"
output_path = "images_webp/LOGO.webp"

img = Image.open(input_path)

# 保留透明通道
if img.mode not in ("RGBA", "LA"):
    img = img.convert("RGBA")

img.save(
    output_path,
    "WEBP",
    quality=90,
    method=6
)

print("Logo done")  