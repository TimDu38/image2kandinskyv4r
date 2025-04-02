from PIL import Image
from rect_converter import RectConverter

class Encoder:
    """Encoder class to convert an image into rectangles and colors for Numworks.
    Attributes:
        app (obj): Instance of the main app.
        size (tuple): Size of the image.
        img (PIL.Image): Image object.
        unique_colors (list): List of unique colors in the image.
        alpha_mode (bool): Indicates if the image has an alpha channel.
        converter (RectConverter): RectConverter object for converting image to rectangles.
        rectangles (list): List of rectangles representing the image.
        palette (list): List of colors corresponding to the rectangles."""
    
    def __init__(self, app):
        self.app = app
        self.size = None
        self.img = None
        self.unique_colors = None
        self.palette_img = None
        self.palette_unique_colors = None
        self.alpha_mode = None
        self.converter = RectConverter(self.app, self)
        self.rectangles = None
    

    def _open_image(self, file_path, attr_name):
        """Open an image file and convert it to RGBA format.
        
        Args:
            file_path (str): The path to the image file.
            attr_name (str): The attribute name to store the opened image.
        
        Raises:
            IOError: If the image cannot be opened.
            Exception: If an error occurs while opening the image.
        """
        try:
            img = Image.open(file_path).convert("RGBA")
            setattr(self, attr_name, img)
            if attr_name == "img":  # Only update size for the main image
                self.size = img.size
        except IOError:
            raise IOError(f"Cannot open image: {file_path}")
        except Exception as e:
            raise Exception(f"An error occurred while opening the image: {e}")

    def _open_main_image(self):
        self._open_image(self.app.file_path, "img")

    def _open_palette_image(self):
        self._open_image(self.app.palette_path, "palette_img")

    
    def _get_colors(self):
        """Get unique colors from the image.
        Raises:
            ValueError: If the image has too many colors or if the image is not in RGBA format.
        """

        colors = self.img.getcolors()
        if colors is None:
            raise ValueError("Image has too many colors")
        unique_colors = []
        self.alpha_mode = False
        for color in colors:
            if color[1][3] > 127:  # Check if the pixel is not transparent
                if color[1][:3] not in unique_colors:
                    unique_colors.append(color[1][:3])
            else:
                self.alpha_mode = True

        unique_colors.sort(key=lambda e: e[0] * 256 ** 2 + e[1] * 256 + e[2])
        self.unique_colors = unique_colors
    
    def _get_palette_colors(self):
        colors = self.palette_img.getcolors()
        if colors is None:
            raise ValueError("Palette has too many colors")
        unique_colors = []
        self.alpha_mode = False
        for color in colors:
            if color[1][3] > 127:  # Check if the pixel is not transparent
                if color[1][:3] not in unique_colors:
                    unique_colors.append(color[1][:3])
        unique_colors.sort(key= lambda e: e[0] * 256 ** 2 + e[1] * 256 + e[2])
        self.palette_unique_colors = unique_colors

    
    def _write_data(self):
        """Write the rectangles and colors to a Python file.
        Raises:
            IOError: If the file cannot be written.
            Exception: If an error occurs while writing data to the file.
        """
        def get_color_list():
            return self.unique_colors if self.app.palette_path is None else self.palette_unique_colors

        with open("data.py", "w") as f:
            f.write(f"colors=[")
            for i in get_color_list():
                f_string = "("
                for j in i:
                    f_string += f"{j},"
                f_string = f_string[:-1]
                f_string += "),"
                f.write(f_string)
            f.write("]\n")
            f.write("rectangles = [")
            for i in self.rectangles:
                f_string = "("
                for j in i:
                    f_string += f"{j},"
                f_string = f_string[:-1]
                f_string += "),"
                f.write(f_string)
            f.write("]\n ")

    def encode(self, mode):
        """Encode the image into rectangles and colors.
        Args:
            mode (str): Mode of encoding ("preview" or "save"). """
        
        self._open_main_image()
        self._get_colors()
        self.converter.convert_to_rect()
        if mode != "preview":
            self._write_data()
        
        


