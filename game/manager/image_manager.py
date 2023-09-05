import os
import random
import sqlite3

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps


class ImageManager:
    """Class that manages the image processing/manipulation."""

    def __init__(self):
        self.operations = {
            'flip': self.flip_image,
            'mirror': self.mirror_image,
            'brightness': self.change_brightness,
            'bgr': self.change_to_bgr_colors,
            'inverted_colors': self.change_to_inverted_colors
        }
        self.reverse_operations = {
            'flip': self.flip_image,
            'mirror': self.mirror_image,
            'brightness': self.revert_brightness,
            'bgr': self.revert_from_bgr_colors,
            'inverted_colors': self.change_to_inverted_colors
        }

    def make_images_database(threat_images_folder_path, non_threat_images_folder_path) -> None:
        """Saves threat and non-threat images in the database.

        Args:
            threat_images_folder_path (str): Path of the threat images folder
            non_threat_images_folder_path (str): Path of the non threat images folder
        """
        # Creating database and making a connection with it
        db_path = os.path.join('game', 'assets', 'images', 'images.sqlite3')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                width INTEGER,
                height INTEGER,
                channels INTEGER,
                threat INTEGER,
                image_data BLOB
            )'''
        )

        # Listing threat and non-threat images
        threat_image_files = os.listdir(threat_images_folder_path)
        non_threat_image_files = os.listdir(non_threat_images_folder_path)

        # Reading and saving all the threat images in the database
        for image_file in threat_image_files:
            image_path = os.path.join(threat_images_folder_path, image_file)
            image = np.array(Image.open(image_path))

            threat = 1
            width = image.shape[0]
            height = image.shape[1]
            channels = image.shape[2]

            cursor.execute(
                """INSERT INTO images (
                    name,
                    width,
                    height,
                    channels,
                    threat,
                    image_data
                ) VALUES (?, ?, ?, ? , ?, ?)""",
                (
                    image_file,
                    width,
                    height,
                    channels,
                    threat,
                    sqlite3.Binary(image.tobytes())
                )
            )
            connection.commit()

        # Reading and saving all the non-threat images in the database
        for image_file in non_threat_image_files:
            image_path = os.path.join(non_threat_images_folder_path, image_file)
            image = np.array(Image.open(image_path))

            threat = 0
            width = image.shape[0]
            height = image.shape[1]
            channels = image.shape[2]

            cursor.execute(
                """INSERT INTO images (
                    name,
                    width,
                    height,
                    channels,
                    threat,
                    image_data
                ) VALUES (?, ?, ?, ? , ?, ?)""",
                (
                    image_file,
                    width,
                    height,
                    channels,
                    threat,
                    sqlite3.Binary(image.tobytes())
                )
            )
            connection.commit()
        connection.close()
        return None

    def fetch_image():
        """Returns one image from the image database.

        Returns:
            Image: Fetched Image
        """
        db_path = os.path.join('game', 'assets', 'images', 'images.sqlite3')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name, width, height, channels, threat, image_data FROM images")

        row = cursor.fetchone()

        if row:
            width = row[1]
            height = row[2]
            channels = row[3]
            # threat = row[4]
            image = np.frombuffer(row[5], dtype=np.uint8).reshape(width, height, channels)
            image = Image.fromarray(image)
        connection.close()

        return image

    def prepare_morph_image(self, image) -> tuple[Image, list]:
        """Prepares the morphed image and returns that image and the list of performed operations

        Args:
            image (Image): Image file

        Returns:
            tuple: tuple containing morphed image and the list of performed operations
        """
        # Randomly choosing an operation from the dict and performing it then
        # storing the operation name in a seperate list
        performed_operations = []
        for i in range(random.randint(1, 5)):
            operation = random.choice(list(self.operations.keys()))
            image = self.operations[operation](image)
            performed_operations.append(operation)
        return (image, performed_operations)

    def reverse_morphed_image(self, image, performed_operations) -> Image:
        """Returns the image after applying the reverse operations.

        Args:
            image (Image): Morphed Image
            performed_operations (list): List of applied operations

        Returns:
            Image: Reversed Image
        """
        for operation in reversed(performed_operations):
            image = self.reverse_operations[operation](image)
        return image

    def flip_image(self, image) -> Image:
        """Flips the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        image = ImageOps.flip(image)
        return image

    def mirror_image(self, image) -> Image:
        """Mirrors the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        # image = image.rotate(180)
        image = ImageOps.mirror(image)
        return image

    def change_brightness(self, image) -> Image:
        """Adds brightness to the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        filter = ImageEnhance.Brightness(image)
        image = filter.enhance(1.05)
        return image

    def revert_brightness(self, image) -> Image:
        """Changes back the brightness of the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        filter = ImageEnhance.Brightness(image)
        image = filter.enhance(0.95)
        return image

    def change_to_bgr_colors(self, image) -> Image:
        """Changes colors of the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = Image.fromarray(image)
        return image

    def revert_from_bgr_colors(self, image) -> Image:
        """Changes back the colors of the image and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return image

    def change_to_inverted_colors(self, image) -> Image:
        """Inverts the image colors and returns the new image.

        Args:
            image (Image): Image to processed

        Returns:
            Image: Processed image
        """
        image = ImageOps.invert(image)
        return image
