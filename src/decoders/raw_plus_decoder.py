from kandinsky import fill_rect

def show_image(palette, rectangles, pos=(0, 0)):
    x, y, w, h, c = pos[0], pos[1], 0, 0, 0
    for rect in rectangles:
        if len(rect) == 5:
            c = palette[rect[4]]
        
        cx, cy, cw, ch = rect[:4]
        x, y, w, h = x + cx, y + cy, w + cw, h + ch
        fill_rect(x, y, w, h, c)