import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import color


def load_image_as_pixels(path: str, resize: int = 200) -> np.ndarray:
    """
    Load an image from the given path and convert it to a 2D array of LAB pixels.

    :param path: Path to the image file
    :type path: str
    :param resize: Maximum size to resize the image (maintains aspect ratio)
    :type resize: int
    :return: 2D array of LAB pixels
    :rtype: np.ndarray
    """

    im = Image.open(path)
    im.thumbnail((resize, resize))

    im_arr = np.array(im)
    # Normalize pixel values to [0, 1]
    im_arr = im_arr / 255.0
    # RGB to LAB
    im_lab = color.rgb2lab(im_arr)

    pixels = im_lab.reshape(-1, 3)

    return pixels


def palette_overlay(image_path: str, palette: list, output_path: str = "palette.jpg") -> None:
    """
    Overlay the color palette on the bottom of the image and save it.

    :param image_path: Path to the input image
    :type image_path: str
    :param palette: List of color information dictionaries
    :type palette: list
    :param output_path: Path to save the output image defaults to "palette.jpg"
    :type output_path: str
    """

    im = Image.open(image_path)
    width, height = im.size

    palette_height = 50
    new_im = Image.new("RGB", (width, height + palette_height))
    new_im.paste(im, (0, 0))

    draw = Image.new("RGB", (width, palette_height))
    segment_width = width // len(palette)

    for i, color_info in enumerate(palette):
        hex_color = color_info["hex"]
        segment = Image.new("RGB", (segment_width, palette_height), hex_color)
        segment_draw = ImageDraw.Draw(segment)
        font = ImageFont.load_default(size=25)
        segment_draw.text((10, 10), color_info["hex"], fill=(
            255, 255, 255), font=font, align="center")
        draw.paste(segment, (i * segment_width, 0))

    new_im.paste(draw, (0, height))
    new_im.save(output_path)
