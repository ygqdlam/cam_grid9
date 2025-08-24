import os
from PIL import Image

def stretch_to_square(image: Image.Image) -> Image.Image:
    """将图像拉伸为正方形，忽略长宽比"""
    w, h = image.size
    # 将图像拉伸为正方形
    return image.resize((min(w, h), min(w, h)), Image.ANTIALIAS)

def process_folder(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    for fname in os.listdir(input_folder):
        if fname.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(input_folder, fname)
            img = Image.open(path)
            img_resized = stretch_to_square(img)
            img_resized.save(os.path.join(output_folder, fname))
            print(f"✅ {fname} 已处理为 {img_resized.size}")

if __name__ == "__main__":
    process_folder("/Users/yanggq/yanggq/伪装项目/point_label_app_grid9/static/images_o", "/Users/yanggq/yanggq/伪装项目/point_label_app_grid9/static/images")
    process_folder("/Users/yanggq/yanggq/伪装项目/point_label_app_grid9/static/masks_o", "/Users/yanggq/yanggq/伪装项目/point_label_app_grid9/static/masks")
    print(f"🎉 所有图片已缩放，保存到 images_resized/ 和 masks_resized/")
