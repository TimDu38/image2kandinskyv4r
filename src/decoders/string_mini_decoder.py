from kandinsky import fill_rect

def show_image(palette, rectangle_string, pos=(0, 0)):
    def decode_color(color):
        r = ((ord(color[0]) - 35) * 255 + 15) // 31
        g = ((ord(color[1]) - 35) * 255 + 31) // 63
        b = ((ord(color[2]) - 35) * 255 + 15) // 31
        return (r, g, b)
    
    def decode_value(string):
            return ord(string) - 35
        
    x, y, w, h, c, f = pos[0], pos[1], 0, 0, 0, 0
    for i in rectangle_string:
        v = decode_value(i)
        if f == 4:
            if v < 0:
                f = 5
                continue
            else:
                fill_rect(x + pos[0], y + pos[1], w, h, color)
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
            c = v
            palette_index = c * 3
            color = decode_color(palette[palette_index:palette_index + 3])
        if f > 3:
            fill_rect(x + pos[0], y + pos[1], w, h, color)
            f = 0
            continue
        f += 1
        
        