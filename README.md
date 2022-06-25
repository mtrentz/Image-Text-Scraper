# Image Text Scraper

Program made to detect text from a bunch of downloaded imgur images.

Starting from a root directory defined in the main.py file, traverse through all subdirectories and run a text detection on each image.

The text detection tool used is EasyOCR.

All image_ids (filenames), paths and texts are stored in a sqlite3 database.

Subsequently, run a text classification script on it. This script looks for specific regular expressions in the text and group them by some categories defined in the classifier.py script.

At last, it will make a copy of the images that were classified into another folder.
