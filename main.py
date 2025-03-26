from PIL import Image
import kandinsky as kd


path = input("Enter file name + extension: ")
img = Image.open(path).convert("RGBA")
size = img.size

new_img = [1 if sum(i[0:3])/3 > 127 else 0 for i in list(img.getdata())]
new_img = [new_img[i:i+size[0]] for i in range(0, len(new_img), size[0])]

used_pixels = [[0 for _ in range(size[0])] for _ in range(size[1])]
rectangles = []

# Find rectangles
for i in range(size[1]):
    for j in range(size[0]):
        if new_img[i][j] == 1 and used_pixels[i][j] == 0:
            x, y = j, i
            while x < size[0] and new_img[i][x] == 1 and used_pixels[i][x] == 0:
                x += 1
            while y < size[1] and 0 not in new_img[y][j:x] and 1 not in used_pixels[y][j:x]:
                y += 1
            for k in range(i, y):
                for l in range(j, x):
                    used_pixels[k][l] = 1
            rectangles.append((j, i, x-j, y-i))

# Merge rectangles
merged_all = False
next_cycle_rectangles = rectangles
destroyed = []
while not merged_all:
    merged_all = True
    for i in rectangles:
        for j in rectangles:
            if i[0] == j[0] and i[2] == j[2] and not i == j and not i in destroyed and not j in destroyed:
                tobe_merged = True
                for k in range(min(i[1], j[1]), max(i[1],j[1])):
                    if 0 in new_img[k][i[0]:i[0]+i[2]]:
                        tobe_merged = False
                        break
                if tobe_merged:
                    next_cycle_rectangles.remove(i)
                    next_cycle_rectangles.remove(j)
                    next_cycle_rectangles.append((i[0], min(i[1], j[1]), i[2], max(i[1]+i[3],j[1]+j[3])-min(i[3], j[3])))
                    destroyed.append(i)
                    destroyed.append(j)
                    merged_all = False
            if i[1] == j[1] and i[3] == j[3] and not i == j and not i in destroyed and not j in destroyed:
                tobe_merged = True
                for k in range(min(i[0], j[0]), max(i[0],j[0])):
                    if 0 in [new_img[l][k] for l in range(i[1], i[1]+i[3])]:
                        tobe_merged = False
                        break
                if tobe_merged:
                    next_cycle_rectangles.remove(i)
                    next_cycle_rectangles.remove(j)
                    next_cycle_rectangles.append((min(i[0], j[0]), i[1], max(i[0]+i[2], j[0]+j[2]) - min(i[0], j[0]), i[3]))
                    destroyed.append(i)
                    destroyed.append(j)
                    merged_all = False
    rectangles = next_cycle_rectangles
    destroyed = []
    
# Draw rectangles
print(rectangles)
print(len(rectangles))
for i in rectangles:
    kd.fill_rect(*(j * 1 for j in i), (0, 255, 255))
