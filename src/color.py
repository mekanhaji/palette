import numpy as np
from skimage import color


def lab_to_hex(lab_color: np.ndarray) -> str:
    """
    Convert a LAB color to its hexadecimal RGB representation.
    :param lab_color: LAB color as a numpy array
    :type lab_color: np.ndarray
    :return: Hexadecimal RGB color string
    :rtype: str
    """
    # Convert single LAB color to RGB
    rgb = color.lab2rgb(np.array([[lab_color]]))[0][0]

    # Scale to 0–255
    rgb = (rgb * 255).astype(int)

    return "#{:02x}{:02x}{:02x}".format(*rgb)


def lab_to_palette(centers: np.ndarray, labels: np.ndarray):
    unique, counts = np.unique(labels, return_counts=True)

    dominant_colors = dict(zip(unique, counts))

    pallette = sorted(
        range(len(centers)),
        key=lambda x: dominant_colors[x],
        reverse=True,
    )

    return [{
        "hex": lab_to_hex(centers[i]),
        "count": dominant_colors[i],
    } for i in pallette]
