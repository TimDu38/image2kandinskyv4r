import kandinsky as kd
import time
import data

t1 = time.monotonic()
if data.colors[0] is not None:
    first_rect = data.rectangles[0]
    kd.fill_rect(first_rect[0], first_rect[1], first_rect[2], first_rect[3], data.colors[0])
    for i in range(1, len(data.rectangles)):
        rect = data.rectangles[i]
        kd.fill_rect(rect[0], rect[1], rect[2], rect[3], data.colors[1])
print("Time taken:", time.monotonic() - t1)

