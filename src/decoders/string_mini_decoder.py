from kandinsky import fill_rect

def show_image(palette, rectangle_string, pos=(0, 0)):
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
                fill_rect(x + px, y + py, w - 35, h - 35, color)
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
            c = (v - 35) * 3
            color_str = palette[c:c + 3]
            color = (((ord(color_str[0]) - 35) * 255 + 15) // 31, ((ord(color_str[1]) - 35) * 255 + 31) // 63, ((ord(color_str[2]) - 35) * 255 + 15) // 31)
        if f > 3:
            fill_rect(x + px, y + py, w - 35, h - 35, color)
            f = 0
            continue
        f += 1
        
        