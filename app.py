import argparse

from src.image import load_image_as_pixels, palette_overlay
from src.color import lab_to_palette
from src.extract import cluster_pixels
from src.cli import print_color_block


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
