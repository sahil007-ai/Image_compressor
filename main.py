import os
from PIL import Image


def compress_image(
    input_image_path, output_image_path, target_size_kb, initial_quality=85
):
    img = Image.open(input_image_path)

    # Convert the target size to bytes
    target_size_bytes = target_size_kb * 1024

    # If the image is in PNG mode (RGBA), convert it to RGB to save as JPEG
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    quality = initial_quality
    img.save(output_image_path, "JPEG", quality=quality, optimize=True)

    # Compress image iteratively until the size is below the target
    while os.path.getsize(output_image_path) > target_size_bytes and quality > 5:
        quality -= 5
        img.save(output_image_path, "JPEG", quality=quality, optimize=True)

    return os.path.getsize(output_image_path)


def compress_images_in_folder(input_folder, output_folder, target_size_kb):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_image_path = os.path.join(input_folder, filename)

        # Check if the file is an image (by extension, e.g., .jpg, .jpeg, .png)
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            output_image_path = os.path.join(output_folder, filename)

            try:
                # Compress the image
                final_size = compress_image(
                    input_image_path, output_image_path, target_size_kb
                )
                print(f"Compressed {filename}: {final_size / 1024:.2f} KB")
            except Exception as e:
                print(f"Error compressing {filename}: {e}")


# Example usage
input_folder = "E:\sahil\certificates\DOCS - Copy"
output_folder = "E:\sahil\certificates\compressed"
target_size_kb = 250  # Target size for each image

compress_images_in_folder(input_folder, output_folder, target_size_kb)
