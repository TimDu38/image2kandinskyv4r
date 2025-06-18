import time
class RectConverter:
    """Class to convert an image to rectangles.
    It handles the conversion of binary images to rectangles and manages the merging of rectangles.
    It also manages the colors used in the rectangles.
    Attributes:
        binary_image (list): Binary representation of the image.
        size (tuple): Size of the image.
        rectangles (list): List of rectangles representing the image.
        unique_colors (list): List of unique colors in the image.
        alpha_mode (bool): Indicates if the image has an alpha channel.
        encoder (obj): stores the parent encoder object reference.
        """
    
    def __init__(self, app, encoder):
        self.binary_image = None
        self.rectangles = None
        self.app = app
        self.encoder = encoder

    
    def _get_binary_image(self):
        """Get the binary image representation of the image.
        """
        if self.app.palette_path is None:
            self.binary_image = [self.encoder.unique_colors.index(self.encoder._rgb888_to_rgb565(i[:3])) if i[3] > 127 else -1 for i in list(self.encoder.img.getdata())]
        else:
            try:
                self.binary_image = [self.encoder.palette_unique_colors.index(self.encoder._rgb888_to_rgb565(i[:3])) if i[3] > 127 else -1 for i in list(self.encoder.img.getdata())]
            except ValueError:
                raise Exception("This image contains color(s) that are not in the loaded palette. \n Please load a compatible image with the palette, or unload the palette.")
            
        self.binary_image = [self.binary_image[i:i+self.encoder.size[0]] for i in range(0, len(self.binary_image), self.encoder.size[0])]


    def _get_rectangles(self, bg_index=None):
        """Get rectangles from the binary image.
        This method scans the binary image and identifies rectangles of 1s.
        It marks the used pixels to avoid counting them multiple times.
        Args:
            bg_color_index (int) : the color index of the background in self.unique_colors
        """
        self.rectangles = []
        used_pixels = [[0 for _ in range(self.encoder.size[0])] for _ in range(self.encoder.size[1])]
        for i in range(self.encoder.size[1]):
            for j in range(self.encoder.size[0]):
                if self.binary_image[i][j] not in [bg_index, -1] and used_pixels[i][j] == 0:
                    current_color_index = self.binary_image[i][j]
                    x, y = j, i
                    while x < self.encoder.size[0] and self.binary_image[i][x] == current_color_index and used_pixels[i][x] == 0:
                        x += 1
                    while y < self.encoder.size[1] and all(pixel == current_color_index for pixel in self.binary_image[y][j:x]) and 1 not in used_pixels[y][j:x]:
                        y += 1
                    for k in range(i, y):
                        for l in range(j, x):
                            used_pixels[k][l] = 1
                    self.rectangles.append((j, i, x-j, y-i, current_color_index))
    
    def _merge_rectangles(self):
        """Merge rectangles that are adjacent to each other.
        This method checks for rectangles that can be merged based on their positions and dimensions."
        """
        merged_all = False
        destroyed = []
        while not merged_all:
            merged_all = True
            merged_rectangles = []
            for i_index in range(len(self.rectangles)):
                i = self.rectangles[i_index]
                for j_index in range(i_index + 1, len(self.rectangles)):
                        j = self.rectangles[j_index]
                        if i[0] == j[0] and i[2] == j[2] and i[4] == j[4] and not i in destroyed and not j in destroyed:
                            tobe_merged = True
                            for k in range(min(i[1], j[1]), max(i[1],j[1])):
                                if not all(pixel == i[4] for pixel in self.binary_image[k][i[0]:i[0]+i[2]]):
                                    tobe_merged = False
                                    break
                            if tobe_merged:
                                merged_rectangles.append((i[0], min(i[1], j[1]), i[2], max(i[1]+i[3],j[1]+j[3])-min(i[3], j[3]), i[4]))
                                destroyed.append(i)
                                destroyed.append(j)
                                merged_all = False
                        elif i[1] == j[1] and i[3] == j[3] and i[4] == j[4] and not i in destroyed and not j in destroyed:
                            tobe_merged = True
                            for k in range(min(i[0], j[0]), max(i[0],j[0])):
                                if not all(row[k] == i[4] for row in self.binary_image[i[1]:i[1]+i[3]]):
                                    tobe_merged = False
                                    break
                            if tobe_merged:
                                merged_rectangles.append((min(i[0], j[0]), i[1], max(i[0]+i[2], j[0]+j[2]) - min(i[0], j[0]), i[3], i[4]))
                                destroyed.append(i)
                                destroyed.append(j)
                                merged_all = False
            self.rectangles = [r for r in self.rectangles if r not in destroyed] + merged_rectangles
            destroyed = []

 

    def convert_to_rect(self):
        """Convert the image to rectangles.
        This method tries to convert the image to rectangles with and without swapping colors.
        It returns the best rectangles and colors based on the number of rectangles.
        """
        def get_bg_index(rectangles):
            colors = {}
            for i in rectangles:
                if i[4] not in colors:
                    colors[i[4]] = 1
                colors[i[4]] += 1
            bg_index = max(colors, key=colors.get)
            return bg_index
        
        def add_bg_rectangle(rectangles, bg_index):
            new_rectangles = [(0, 0, self.encoder.size[0], self.encoder.size[1], bg_index)]
            for i in rectangles:
                if i[4] != bg_index:
                    new_rectangles.append(i)
            return new_rectangles
        

        self._get_binary_image()
        if self.encoder.alpha_mode:
            self._get_rectangles()
            self._merge_rectangles()
            self.encoder.rectangles = self.rectangles.copy()
        else:
            t1 = time.time()
            self._get_rectangles()
            #print(f"First pass took {time.time() - t1:.2f} seconds")
            t1 = time.time()
            self._merge_rectangles()
            #print(f"Second pass took {time.time() - t1:.2f} seconds")
            t1 = time.time()
            bg_index = get_bg_index(self.rectangles)
            self.rectangles = add_bg_rectangle(self.rectangles, bg_index)
            self.encoder.rectangles = self.rectangles.copy()
            #print(f"Third pass took {time.time() - t1:.2f} seconds")
    


        