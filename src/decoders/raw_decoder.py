from kandinsky import fill_rect

def show_image(palette, rectangles, pos=(0, 0)):
    for rect in rectangles:
        x, y, w, h, c = rect
        fill_rect(x + pos[0], y + pos[1], w, h, palette[c])

