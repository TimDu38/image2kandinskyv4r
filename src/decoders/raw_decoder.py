from kandinsky import fill_rect

def show_image(palette, rectangles, pos=(0, 0)):
    draw = fill_rect
    px, py = pos
    pal = palette
    for rect in rectangles:
        x, y, w, h, c = rect
        draw(x + px, y + py, w, h, pal[c])

