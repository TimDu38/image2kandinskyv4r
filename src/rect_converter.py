class RectConverter:
    def __init__(self):
        self.binary_image = None
        self.size = None
        self.rectangles = None
        self.alpha_mode = None
        self.unique_colors = None

    def _get_binary_image(self, encoder_obj, swap_colors=False):
        self.unique_colors = encoder_obj.unique_colors
        if swap_colors:
            self.unique_colors = encoder_obj.unique_colors[::-1]
        if None in self.unique_colors:
            self.binary_image = [0 if i[3] < 127 else 1 for i in list(encoder_obj.img.getdata())]
            self.alpha_mode = True
        else:
            self.binary_image = [0 if i[:3] == self.unique_colors[0] else 1 for i in list(encoder_obj.img.getdata())]
            self.alpha_mode = False
        self.binary_image = [self.binary_image[i:i+encoder_obj.size[0]] for i in range(0, len(self.binary_image), encoder_obj.size[0])]
        self.size = encoder_obj.size
    
    def _get_rectangles(self):
        used_pixels = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.rectangles = []
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.binary_image[i][j] == 1 and used_pixels[i][j] == 0:
                    x, y = j, i
                    while x < self.size[0] and self.binary_image[i][x] == 1 and used_pixels[i][x] == 0:
                        x += 1
                    while y < self.size[1] and 0 not in self.binary_image[y][j:x] and 1 not in used_pixels[y][j:x]:
                        y += 1
                    for k in range(i, y):
                        for l in range(j, x):
                            used_pixels[k][l] = 1
                    self.rectangles.append((j, i, x-j, y-i))
    
    def _merge_rectangles(self):
        merged_all = False
        destroyed = []
        while not merged_all:
            merged_all = True
            merged_rectangles = []
            for i in self.rectangles:
                for j in self.rectangles:
                    if i[0] == j[0] and i[2] == j[2] and not i == j and not i in destroyed and not j in destroyed:
                        tobe_merged = True
                        for k in range(min(i[1], j[1]), max(i[1],j[1])):
                            if 0 in self.binary_image[k][i[0]:i[0]+i[2]]:
                                tobe_merged = False
                                break
                        if tobe_merged:
                            merged_rectangles.append((i[0], min(i[1], j[1]), i[2], max(i[1]+i[3],j[1]+j[3])-min(i[3], j[3])))
                            destroyed.append(i)
                            destroyed.append(j)
                            merged_all = False
                    if i[1] == j[1] and i[3] == j[3] and not i == j and not i in destroyed and not j in destroyed:
                        tobe_merged = True
                        for k in range(min(i[0], j[0]), max(i[0],j[0])):
                            if 0 in [self.binary_image[l][k] for l in range(i[1], i[1]+i[3])]:
                                tobe_merged = False
                                break
                        if tobe_merged:
                            merged_rectangles.append((min(i[0], j[0]), i[1], max(i[0]+i[2], j[0]+j[2]) - min(i[0], j[0]), i[3]))
                            destroyed.append(i)
                            destroyed.append(j)
                            merged_all = False
            self.rectangles = [r for r in self.rectangles if r not in destroyed] + merged_rectangles
            destroyed = []

        # Remove duplicates
        self.rectangles = list(set(self.rectangles))

    def _add_background(self, encoder_obj, swap_colors=False):
        if not self.alpha_mode:
            colors = encoder_obj.unique_colors if not swap_colors else encoder_obj.unique_colors[::-1]
            self.rectangles.insert(0, (0, 0, self.size[0], self.size[1]))
        elif encoder_obj.unique_colors[1] is None:
            colors = encoder_obj.unique_colors[::-1]
        else:
            colors = self.encoder_obj.unique_colors
        return colors
 

    def convert_to_rect(self, encoder_obj):
        best_rectangles = []
        best_rectangles_count = float("inf")
        for swap_colors in [False, True]:
            if (swap_colors and not self.alpha_mode) or not swap_colors:
                self._get_binary_image(encoder_obj, swap_colors)
                self._get_rectangles()
                self._merge_rectangles()
                colors = self._add_background(encoder_obj, swap_colors)
                print(f"Rectangles count: {len(self.rectangles)}")
                if len(self.rectangles) < best_rectangles_count:
                    best_rectangles = self.rectangles.copy()
                    best_rectangles_count = len(self.rectangles)
                    colors_setting = colors.copy()
        return best_rectangles, colors_setting
    


        