from kandinsky import fill_rect

def show_image(palette_hex, rectangles_hex, pos=(0, 0)):
    current_color = (0, 0, 0)
    i = 0
    block_size = 32  # You can tune this for performance
    while i < len(rectangles_hex):
        chunk = rectangles_hex[i:i + block_size]
        num = int(chunk, 16)
        bits = len(chunk) * 4  # Each hex char = 4 bits
        while bits >= 32:
            rect = num >> (bits - 32) & 0xFFFFFFFF
            if (rect >> 24) == 0xFF:
                color_index = rect & 0xFF
                color_start = color_index * 6
                color_hex = palette_hex[color_start:color_start + 6]
                current_color = tuple(int(color_hex[j:j+2], 16) for j in (0, 2, 4))
            else:
                x = rect >> 24 & 0xFF
                y = rect >> 16 & 0xFF
                w = rect >> 8 & 0xFF
                h = rect & 0xFF
                fill_rect(pos[0] + x, pos[1] + y, w, h, current_color)
            bits -= 32
        i += block_size
