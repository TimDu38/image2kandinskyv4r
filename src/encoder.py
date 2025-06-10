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
        self.converted_flag = False
    

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

    @staticmethod
    def _rgb888_to_rgb565(rgb):
        """Convert RGB888 color to RGB565 format.
        
        Args:
            rgb (tuple): A tuple representing the RGB color (R, G, B).
        
        Returns:
            tuple: The RGB565 representation of the color.
        """
        r, g, b = rgb
        r = ( r *  31 + 127) // 255
        g = ( g *  63 + 127) // 255
        b = ( b *  31 + 127) // 255
        return (r, g, b)
    
    @staticmethod
    def _rgb565_to_rgb888(rgb565):
        """Convert RGB565 color to RGB888 format.
        
        Args:
            rgb565 (tuple): A tuple representing the RGB565 color (R, G, B).
        
        Returns:
            tuple: The RGB888 representation of the color.
        """
        r, g, b = rgb565
        r = (r * 255 + 15) // 31
        g = (g * 255 + 31) // 63
        b = (b * 255 + 15) // 31
        return (r, g, b)

    
    def _get_colors(self):
        """Get unique colors from the image.
        Raises:
            ValueError: If the image has too many colors or if the image is not in RGBA format.
        """

        colors = self.img.getcolors(maxcolors=2**16)
        unique_colors = []
        alpha_mode = False
        for color in colors:
            if color[1][3] > 127:  # Check if the pixel is not transparent
                reduced_color = self._rgb888_to_rgb565(color[1][:3])
                if reduced_color not in unique_colors:
                    unique_colors.append(reduced_color)
                    if len(unique_colors) > 1024:
                        raise ValueError("Image has too many colors (max 1024)")
            else:
                alpha_mode = True

        unique_colors.sort(key=lambda e: e[0] * 256 ** 2 + e[1] * 256 + e[2])
        self.unique_colors = unique_colors
        self.alpha_mode = alpha_mode
    
    def _get_palette_colors(self):
        colors = self.palette_img.getcolors(maxcolors=2**16)
        unique_colors = []
        for color in colors:
            if color[1][3] > 127:  # Check if the pixel is not transparent
                reduced_color = self._rgb888_to_rgb565(color[1][:3])
                if reduced_color not in unique_colors:
                    unique_colors.append(reduced_color)
                    if len(unique_colors) > 1024:
                        raise ValueError("Palette has too many colors (max 1024)")
        unique_colors.sort(key= lambda e: e[0] * 256 ** 2 + e[1] * 256 + e[2])

        self.palette_unique_colors = unique_colors


    def encode(self):
        """Encode the image into rectangles and colors.
        """
        self._open_main_image()
        self._get_colors()
        self.converter.convert_to_rect()
        
        


