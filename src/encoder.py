from PIL import Image
from rect_converter import RectConverter

class Encoder:
    """Encoder class to convert an image into rectangles and colors for Numworks.
    Attributes:
        path (str): Path to the image file.
        size (tuple): Size of the image.
        img (PIL.Image): Image object.
        unique_colors (list): List of unique colors in the image.
        converter (RectConverter): RectConverter object for converting image to rectangles.
        rectangles (list): List of rectangles representing the image.
        colors (list): List of colors corresponding to the rectangles."""
    
    def __init__(self):
        self.path = None
        self.size = None
        self.img = None
        self.unique_colors = None
        self.converter = RectConverter()
        self.rectangles = None
        self.colors = None
    
    def _open_image(self):
        """Open the image file and convert it to RGBA format.
        Raises:
            IOError: If the image cannot be opened.
            Exception: If an error occurs while opening the image.
        """
        try:
            self.img = Image.open(self.path).convert("RGBA")
            self.size = self.img.size
        except IOError:
            raise IOError(f"Cannot open image: {self.path}")
        except Exception as e:
            raise Exception(f"An error occurred while opening the image: {e}")
        
    
    def _get_colors(self):
        """Get unique colors from the image.
        Raises:
            ValueError: If the image has too many colors or if the image is not in RGBA format.
            Exception: If an error occurs while getting colors from the image.
        """

        colors = self.img.getcolors()
        if colors is None:
            raise ValueError("Image has too many colors")
        unique_colors = []
        for color in colors:
            if color[1][3] < 127:  # Check if the pixel is transparent
                if None not in unique_colors:
                    unique_colors.append(None)
            else:
                if color[1][:3] not in unique_colors:
                    unique_colors.append(color[1][:3])
        if len(unique_colors) > 2:
            raise ValueError("Image has too many colors")
        self.unique_colors = unique_colors
    
    def _write_data(self):
        """Write the rectangles and colors to a Python file.
        Raises:
            IOError: If the file cannot be written.
            Exception: If an error occurs while writing data to the file.
        """

        with open("data.py", "w") as f:
            f.write(f"colors={self.unique_colors}\n")
            f.write("rectangles = [")
            for i in self.rectangles:
                f.write(f"({i[0]},{i[1]},{i[2]},{i[3]}),")
            f.write("]\n ")

    def encode(self, mode):
        """Encode the image into rectangles and colors.
        Args:
            mode (str): Mode of encoding ("preview" or "save"). """
        
        self._open_image()
        self._get_colors()
        self.rectangles, self.unique_colors = self.converter.convert_to_rect(self)
        if mode != "preview":
            self._write_data()
        
        


