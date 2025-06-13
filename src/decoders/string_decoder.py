from kandinsky import fill_rect

def show_image(palette, rect_str, pos=(0, 0)):

    def decode_color(color):
        r = ((ord(color[0]) - 35) * 255 + 15) // 31
        g = ((ord(color[1]) - 35) * 255 + 31) // 63
        b = ((ord(color[2]) - 35) * 255 + 15) // 31
        return (r, g, b)
    
    def decode_value(string):
        chr1 = ord(string[0])
        if chr1 < 104:  # single character value
            return (chr1 - 35), 1
        return ((ord(string[0]) - 104) << 6) + (ord(string[1]) - 35), 2
    
    x, y, c, w, h = pos[0], pos[1], 0, 0, 0
    color = decode_color(palette[0:3])
    i = 0
    field = 0
    while i < len(rect_str):
        if field == 4:
            if not rect_str[i] == " ":
                field = 0
                fill_rect(x, y, w, h, color)
                continue
            else:
                i += 1
        absolute_flag = False
        if field not in (2,3):
            if rect_str[i] == "!":
                i += 1
                absolute_flag = True
        value, length = decode_value(rect_str[i:i+2])
        i += length
        if absolute_flag:
            if field == 0:
                x = value + pos[0]
            elif field == 1:
                y = value + pos[1]
            elif field == 4:
                c = value
                palette_index = c * 3
                color = decode_color(palette[palette_index:palette_index + 3])
        else:
            if field == 0:
                x += value
            elif field == 1:
                y += value
            elif field == 2:
                w = value
            elif field == 3:
                h = value
            elif field == 4:
                c += value
                palette_index = c * 3
                color = decode_color(palette[palette_index:palette_index + 3])
        if field == 4:
            fill_rect(x, y, w, h, color)
            field = 0
        else:
            field += 1