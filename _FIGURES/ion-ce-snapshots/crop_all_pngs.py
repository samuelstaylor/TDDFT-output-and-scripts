import os
import numpy as np
from PIL import Image

def crop_image_numpy(img_path, save_path, white_threshold=240):
    """Crop white borders from an image using numpy mask."""
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGBA")
            arr = np.array(img)

            # mask = True where pixel is white
            mask = np.all(arr[:, :, :3] >= white_threshold, axis=-1)

            # Non-white pixels are mask == False
            non_white = np.where(mask == False)

            if non_white[0].size == 0:
                # Entire image is white — save original
                img.save(save_path)
                return False

            min_x, max_x = np.min(non_white[1]), np.max(non_white[1])
            min_y, max_y = np.min(non_white[0]), np.max(non_white[0])

            cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
            cropped.save(save_path)
            return True

    except Exception as e:
        print(f"   ✗ Error processing {img_path}: {e}")
        return False


def process_directory(root_dir):
    """Recursively crop all PNGs in all directories under root_dir."""
    for root, dirs, files in os.walk(root_dir):
        
        pngs = [f for f in files if f.lower().endswith(".png")]
        if not pngs:
            continue

        cropped_dir = os.path.join(root, "cropped")
        os.makedirs(cropped_dir, exist_ok=True)

        print(f"\nProcessing: {root}")
        print(f"Saving to:  {cropped_dir}")

        for name in pngs:
            src = os.path.join(root, name)
            dst = os.path.join(cropped_dir, name)

            success = crop_image_numpy(src, dst)

            if success:
                print(f"   ✓ Cropped {name}")
            else:
                print(f"   • No crop needed {name}")


if __name__ == "__main__":
    start_dir = os.getcwd()
    print(f"Starting recursive cropping in: {start_dir}")
    process_directory(start_dir)
