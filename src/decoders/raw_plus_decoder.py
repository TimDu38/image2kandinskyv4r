from kandinsky import fill_rect

def show_image(palette, rectangles, pos=(0, 0)):
    pal = palette
    draw = fill_rect
    x, y, ci = pos[0], pos[1], 0
    for rect in rectangles:
        if len(rect) == 5:
            ci += rect[4]
            c = pal[ci]
        
        cx, cy, w, h = rect[:4]
        x, y,= x + cx, y + cy,
        draw(x, y, w, h, c)