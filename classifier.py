from shutil import copyfile
from logger import logger
import re
import os

REGEX_DETECTION_LIST = {
    "email": [
        r"email",
        r"mail",
        r"[^@\s]+@[^@\s\.]+\.[^@\.\s]+",
    ],
    "password": [
        r"password",
    ],
    "crypto": [
        r"bitcoin",
        r"bit",
        r"crypto",
        r"binance",
        r"wallet",
        # Bitcoin wallet regex
        r"(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}",
        # Eth wallet regex
        r"0x[a-fA-F0-9]{30,40}",
    ],
    "phone": [
        # US phone
        r"\([0-9]{3}\)[0-9]{3}-[0-9]{4}",
        # Brazil phone
        r"\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*",
        # India phone
        r"\+?\d[\d -]{8,12}\d",
    ],
    "payments": [
        r"payment",
        r"purchase",
        r"credit",
        r"card",
        r"charge",
        r"billing",
        r"ccv",
        r"mastercard",
        r"visa",
    ],
}


class TextClassifier:
    def __init__(self, text: str, input_path: str = None, output_root_path: str = None):
        self.text = text
        self.input_path = input_path
        self.output_root_path = output_root_path
        self.classifications = []

    def classify(self):
        # Iterate over each category and its list of regexes
        for category, regexes in REGEX_DETECTION_LIST.items():
            for regex in regexes:
                re_exp = re.compile(regex, re.IGNORECASE)
                # If it identifies one of the regexes, break the inner loop
                # and move on to the next category
                if re_exp.search(self.text):
                    self.classifications.append(category)
                    break

    @staticmethod
    def copy_img(origin, destination):
        # Check if the source exists so it can copy over
        if os.path.exists(origin):
            # If exists, then check if it wasn't already copied to destination folder.
            if not os.path.exists(destination):
                copyfile(origin, destination)

    def copy_image_to_category_dirs(self):
        """
        This function will make a copy of the image on a named classification directory on
        output_root_path for every category that the image is in.

        For example in the image in /path/to/img.png classified as 'email' and 'password',
        the image will be copied to:
            /path/to/root_path/email/img.png
            /path/to/root_path/password/img.png
        """
        if not self.input_path and not self.output_root_path:
            logger.warning("Image input path and outpoot root path need to be provided")
            return

        image_fname = self.input_path.split("/")[-1]

        if not self.classifications:
            logger.warning(
                f"Image classification wasn't performed or no categories were found for id {image_fname}"
            )
            return

        for classif in self.classifications:
            # Guarantee that the output directory exists, if not, create
            output_dir = os.path.join(self.output_root_path, classif)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Copy the image to the output directory
            final_path = os.path.join(self.output_root_path, classif, image_fname)
            self.copy_img(self.input_path, final_path)
