import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import color
from sklearn.cluster import KMeans


def load_image_as_pixels(path: str, resize: int = 200):
    im = Image.open(path)
    im.thumbnail((resize, resize))

    im_arr = np.array(im)
    # Normalize pixel values to [0, 1]
    im_arr = im_arr / 255.0
    # RGB to LAB
    im_lab = color.rgb2lab(im_arr)

    pixels = im_lab.reshape(-1, 3)

    return pixels


def cluster_pixels(pixels: np.ndarray, n_clusters: int = 6):
    print("Clustering pixels into {} clusters...".format(n_clusters))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixels)

    print("Clustering completed.")
    return kmeans.labels_, kmeans.cluster_centers_


def lab_to_hex(lab_color):
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


def palette_overlay(image_path: str, palette: list, output_path: str = "palette.jpg"):
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


def print_color_block(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    print(f"\033[48;2;{r};{g};{b}m      \033[0m {hex_color}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract color palette from an image."
    )
    parser.add_argument("--image", "-i", type=str, required=False,
                        help="Path to the input image.")
    parser.add_argument("--colors", "-c", type=int, default=6,
                        help="Number of colors to extract.")
    parser.add_argument("--resize", "-r", type=int, default=200,
                        help="Resize dimension for processing.")
    parser.add_argument("--output", "-o", type=str,
                        default="palette.jpg", help="Output image with palette overlay.")
    args = parser.parse_args()

    pixels = load_image_as_pixels(args.image, resize=args.resize)

    labels, centers = cluster_pixels(pixels, n_clusters=args.colors)

    palette = lab_to_palette(centers, labels)
    palette_overlay(args.image, palette, output_path=args.output)

    for color_info in palette:
        print_color_block(color_info["hex"])


if __name__ == "__main__":
    main()
