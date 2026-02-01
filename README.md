# Palette

Simple cli tool for extracting color palettes from images.

## Features

- Extract dominant colors from images
- Get color palette on your images.

## Example Usage

```bash
uv run app.py -i ./examples/image1.jpg -c 5 -r 300
```

This will extract 5 dominant colors from `image1.jpg`, resizing the image to 300 pixels for processing.

### Arguments

- `--image` or `-i`: Path to the input image.
- `--colors` or `-c`: Number of colors to extract (default is 6).
- `--resize` or `-r`: Resize dimension for processing (default is 200).
- `--output` or `-o`: Path to save the output image with palette overlay (default is `palette.jpg`).

## Setup

### 1. Clone the repository.

I haven’t published this yet, so you’ll need to clone it for now.

```bash
git clone https://github.com/yourusername/palette.git

cd palette
```

### 2. Install dependencies.

I’m using **uv** to manage dependencies, it’s a great tool for managing Python projects.

```bash
uv synch
```

```bash
uv run app.py -i ./examples/image1.jpg -c 5 -r 300 -o ./examples/output_with_palette.jpg
```

If you find any mistakes or bugs, please create an issue. I’m also open to any suggestions or improvements. happy coding `:)`
