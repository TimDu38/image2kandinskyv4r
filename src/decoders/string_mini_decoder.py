from kandinsky import fill_rect

def show_image(palette, rectangle_string, pos=(0, 0)):
    draw = fill_rect
    pal = palette
    f,x,y,w,h,color = 4, 0, 0, 0, 0, (0, 0, 0)
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
                f = 1
                x = v
                continue
        if f == 1:
            y = v
            f = 2
            continue
        if f == 2:
            w = v
            f = 3
            continue
        if f == 3:
            h = v
            f = 4
            continue
        if f == 5:
            c = v * 3 - 105
            color_str = pal[c:c + 3]
            color = ((ord(color_str[0]) * 255 - 8910) // 31, (ord(color_str[1]) * 255 - 8894) // 63, (ord(color_str[2]) * 255 - 8910) // 31)
            draw(x + px, y + py, w - 35, h - 35, color)
            f = 4
        
        