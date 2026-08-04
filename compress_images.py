from PIL import Image
import os

source_folder = "images"
output_folder = "images_webp"

max_size = 1600
quality = 80

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

count = 0
total_size = 0

for root, dirs, files in os.walk(source_folder):

    for file in files:

        if file.lower().endswith((".jpg", ".jpeg", ".png")):

            input_path = os.path.join(root, file)

            relative_path = os.path.relpath(root, source_folder)

            save_folder = os.path.join(
                output_folder,
                relative_path
            )

            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            output_name = os.path.splitext(file)[0] + ".webp"

            output_path = os.path.join(
                save_folder,
                output_name
            )

            try:
                img = Image.open(input_path)

                img.thumbnail(
                    (max_size, max_size),
                    Image.Resampling.LANCZOS
                )

                if img.mode != "RGB":
                    img = img.convert("RGB")

                img.save(
                    output_path,
                    "WEBP",
                    quality=quality,
                    method=6
                )

                size = os.path.getsize(output_path)
                total_size += size

                count += 1

                print(f"{count}: {file}")

            except Exception as e:
                print("ERROR:", file, e)


print("========================")
print("Finished:", count)
print(
    "New size:",
    round(total_size / 1024 / 1024, 2),
    "MB"
)