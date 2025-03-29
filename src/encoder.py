from PIL import Image
from rect_converter import RectConverter

class Encoder:
    def __init__(self):
        self.path = None
        self.size = None
        self.img = None
        self.unique_colors = None
        self.converter = RectConverter()
        self.rectangles = None
    
    def _open_image(self):
        try:
            self.img = Image.open(self.path).convert("RGBA")
            self.size = self.img.size
        except IOError:
            raise IOError(f"Cannot open image: {self.path}")
        except Exception as e:
            raise Exception(f"An error occurred while opening the image: {e}")
        
    
    def _get_colors(self):
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
        self.unique_colors = unique_colors
        if len(unique_colors) > 2:
            raise ValueError("Image has too many colors")
    
    def _write_data(self):
        with open("data.py", "w") as f:
            f.write("rectangles = [")
            for i in self.rectangles:
                f.write(f"({i[0]},{i[1]},{i[2]},{i[3]}),")
            f.write("]")

    def encode(self, mode):
        self._open_image()
        self._get_colors()
        self.rectangles = self.converter.convert_to_rect(self)
        if mode == "preview":
            pass
        else:
            self._write_data()
        
        


