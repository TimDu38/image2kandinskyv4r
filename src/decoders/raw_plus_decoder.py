from kandinsky import fill_rect

def show_image(palette, rectangles, pos=(0, 0)):
    x, y, c = pos[0], pos[1], 0
    for rect in rectangles:
        if len(rect) == 5:
            c = palette[rect[4]]
        
        cx, cy, w, h = rect[:4]
        x, y,= x + cx, y + cy,
        fill_rect(x, y, w, h, c)