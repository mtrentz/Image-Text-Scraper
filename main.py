from database import (
    start_db,
    insert_text,
    image_already_scraped,
    get_all_images_with_text,
    get_new_images_from_path_list,
)
from text_scraper import ImageTextScraper
from classifier import TextClassifier
from tqdm import tqdm
import glob
import os
from logger import logger


def list_all_images(dir: str) -> list[str]:
    """
    Return a list of all images in a directory recursively, including its sub-directories.
    """
    file_types = ["*.jpg", "*.jpeg", "*.png"]
    all_images = []
    for file_type in file_types:
        all_images.extend(glob.glob(os.path.join(dir, file_type), recursive=True))
    return all_images


if __name__ == "__main__":
    IMGS_ROOT_DIR = "/path/to/folder/**"

    # Start database
    print("Starting database...")
    conn = start_db()

    # Start Text Scraper
    print("Starting scraper...")
    scraper = ImageTextScraper(gpu=True)

    # Read all images
    print("Loading all images...")
    all_images = list_all_images(IMGS_ROOT_DIR)

    # Filter images already scraped
    print("Filtering images already scraped...")
    all_images = get_new_images_from_path_list(conn, all_images)

    for img_path in tqdm(all_images):
        # Get the IMGUR ID from the image path
        imgur_id = img_path.split("/")[-1].split(".")[0]

        # Scrape text from image
        text = scraper.detect_text(img_path)

        # Insert text into database
        insert_text(conn, imgur_id, img_path, text)

    # Iterate through all images in database and classify them
    print("Classifying all images...")
    scraped_texts = get_all_images_with_text(conn)

    output_root_dir = "./classifications"

    for item in tqdm(scraped_texts):
        _, _, img_path, text = item
        clf = TextClassifier(
            text,
            img_path,
            output_root_dir,
        )
        clf.classify()
        clf.copy_image_to_category_dirs()
