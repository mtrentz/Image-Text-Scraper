import easyocr
import numpy as np
from PIL import Image
from logger import logger


class ImageTextScraper:
    def __init__(self, gpu: bool = False):
        self.reader = easyocr.Reader(["en"], gpu=gpu)

    @staticmethod
    def resize_img(img_path: str) -> Image:
        """Resize an image to a fixed size if it is too large."""
        try:
            with Image.open(img_path) as im:
                im = im.convert("RGB")
                max_size = 1000, 1000
                # Resizes image
                im.thumbnail(max_size, Image.ANTIALIAS)
            return im.copy()
        except Exception as e:
            logger.warning(f"Failed to resize image at {img_path}: {e}")
            return None

    def detect_text(self, img_path: str) -> str:
        resized_img = self.resize_img(img_path)
        if not resized_img:
            return None

        resized_img = np.asarray(resized_img)

        try:
            result = self.reader.readtext(resized_img)
        except Exception as e:
            logger.warning(f"Failed to detect text in image at {img_path}: {e}")
            return None
        detected_text = ""
        # Get detected text separated by newline
        for res in result:
            text = res[1]
            detected_text += text + "\n"

        if detected_text.replace(" ", "") == "":
            return None

        return detected_text
