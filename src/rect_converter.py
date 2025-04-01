class RectConverter:
    """Class to convert an image to rectangles.
    It handles the conversion of binary images to rectangles and manages the merging of rectangles.
    It also manages the colors used in the rectangles.
    Attributes:
        binary_image (list): Binary representation of the image.
        size (tuple): Size of the image.
        rectangles (list): List of rectangles representing the image.
        unique_colors (list): List of unique colors in the image.
        alpha_mode (bool): Indicates if the image has an alpha channel."""
    
    def __init__(self):
        self.binary_image = None
        self.size = None
        self.rectangles = None
        self.unique_colors = None
        self.alpha_mode = None


    def _initialize(self, encoder_obj):
        """Add background color to the rectangles.
        This method adds a background rectangle if the image is not transparent.
        Also swaps the colors if specified.
        Args:
            encoder_obj (Encoder): Encoder object containing image data.
        """
        self.rectangles = []
        self.unique_colors = encoder_obj.unique_colors.copy()
        self.size = encoder_obj.size
        self.alpha_mode = encoder_obj.alpha_mode

    
    def _get_binary_image(self, encoder_obj):
        """Get the binary image representation of the image.
        Args:
            encoder_obj (Encoder): Encoder object containing image data.
        """
        self.binary_image = [self.unique_colors.index(i[:3]) if i[3] > 127 else -1 for i in list(encoder_obj.img.getdata())]
        self.binary_image = [self.binary_image[i:i+self.size[0]] for i in range(0, len(self.binary_image), encoder_obj.size[0])]


    def _get_rectangles(self, bg_index=None):
        """Get rectangles from the binary image.
        This method scans the binary image and identifies rectangles of 1s.
        It marks the used pixels to avoid counting them multiple times.
        Args:
            bg_color_index (int) : the color index of the background in self.unique_colors
        """
        if not self.alpha_mode:
            self.rectangles.append((0, 0, self.size[0], self.size[1], bg_index))
        used_pixels = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.binary_image[i][j] not in [bg_index, -1] and used_pixels[i][j] == 0:
                    current_color_index = self.binary_image[i][j]
                    x, y = j, i
                    while x < self.size[0] and self.binary_image[i][x] == current_color_index and used_pixels[i][x] == 0:
                        x += 1
                    while y < self.size[1] and all(pixel == current_color_index for pixel in self.binary_image[y][j:x]) and 1 not in used_pixels[y][j:x]:
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
            for i in self.rectangles:
                for j in self.rectangles:
                    if len(i) > 4 and len(j) > 4:
                        if i[0] == j[0] and i[2] == j[2] and i[4] == j[4] and not i == j and not i in destroyed and not j in destroyed:
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
                        elif i[1] == j[1] and i[3] == j[3] and i[4] == j[4] and not i == j and not i in destroyed and not j in destroyed:
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

 

    def convert_to_rect(self, encoder_obj):
        """Convert the image to rectangles.
        This method tries to convert the image to rectangles with and without swapping colors.
        It returns the best rectangles and colors based on the number of rectangles.
        Args:
            encoder_obj (Encoder): Encoder object containing image data.
        """
        if encoder_obj.alpha_mode:
            self._initialize(encoder_obj)
            self._get_binary_image(encoder_obj)
            self._get_rectangles()
            self._merge_rectangles()
            rectangles = self.rectangles
            colors = self.unique_colors
            return rectangles, colors
        else:
            best_rectangles = []
            best_rectangles_count = float("inf")
            best_colors_palette = []
            for i in range(max(len(encoder_obj.unique_colors), 10)):
                self._initialize(encoder_obj)
                self._get_binary_image(encoder_obj)
                self._get_rectangles(i)
                self._merge_rectangles()
                if len(self.rectangles) < best_rectangles_count:
                    best_rectangles = self.rectangles.copy()
                    best_rectangles_count = len(self.rectangles)
                    best_colors_palette = self.unique_colors.copy()
        return best_rectangles, best_colors_palette
    


        