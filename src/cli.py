def print_color_block(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    print(f"\033[48;2;{r};{g};{b}m      \033[0m {hex_color}")
