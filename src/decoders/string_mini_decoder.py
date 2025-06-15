from kandinsky import fill_rect

def show_image(palette, rectangle_string, pos=(0, 0)):
    draw = fill_rect
    pal = palette
    x, y, w, h, c, f = 0, 0, 0, 0, 0, 0
    px, py = pos
    px, py = px - 35, py - 35
    o = ord
    for i in rectangle_string:
        v = o(i)
        if f == 4:
            if v < 35:
                f = 5
                continue
            else:
                draw(x + px, y + py, w - 35, h - 35, color)
                f = 0
        if f == 0:
             x = v
        elif f == 1:
             y = v
        elif f == 2:
             w = v
        elif f == 3:
             h = v
        elif f == 5:
            c = v * 3 - 105
            color_str = pal[c:c + 3]
            color = ((ord(color_str[0]) * 255 - 8910) // 31, (ord(color_str[1]) * 255 - 8894) // 63, (ord(color_str[2]) * 255 - 8910) // 31)
            draw(x + px, y + py, w - 35, h - 35, color)
            f = 0
            continue
        f += 1
        
        