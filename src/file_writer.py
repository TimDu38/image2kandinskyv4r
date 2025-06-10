class FileWriter():
    def __init__(self, app):
        self.app = app
        self.encoder = app.encoder
        self.mode = "raw"

    
    def set_mode(self, mode):
        self.mode = mode

    @staticmethod
    def get_char_count():
        with open("data.py", "r") as f:
            data = f.read()
            return len(data)


    def write(self):

        def get_color_list(rescale=True):
            color_lst = self.encoder.unique_colors if self.app.palette_path is None else self.encoder.palette_unique_colors
            return color_lst if not rescale else [self.encoder._rgb565_to_rgb888(color) for color in color_lst]
        
        def get_rectangles():
            if self.encoder.alpha_mode:
                return sorted(
                    self.encoder.rectangles,
                    key=lambda e: e[4]
                )
            else:
                return [self.encoder.rectangles[0]] + sorted(
                    self.encoder.rectangles[1:],
                    key=lambda e: e[4]
                )

        def get_rectangles_2():
            if self.encoder.alpha_mode:
                return sorted(
                    self.encoder.rectangles,
                    key=lambda e: (e[4], e[0], e[1], e[2], e[3])
                )
            else:
                return [self.encoder.rectangles[0]] + sorted(
                    self.encoder.rectangles[1:],
                    key=lambda e: (e[4], e[0], e[1], e[2], e[3])
                )
            
        def get_deltas():
            deltas = []
            last_x, last_y, last_xs, last_ys, last_color = 0, 0, 0, 0, -1
            for rect in get_rectangles_2():
                x, y, xs, ys, color = rect[0], rect[1], rect[2], rect[3], rect[4]
                dx, dy = x - last_x, y - last_y,
                if color != last_color:
                    deltas.append((dx, dy, xs, ys, color))
                else:
                    deltas.append((dx, dy, xs, ys))
                last_x, last_y, last_color = x, y, color
            return deltas   


        if self.mode in ["raw", "raw+"]:
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
                rectangles = get_rectangles() if self.mode == "raw" else get_deltas()
                for i in rectangles:
                    f_string = "("
                    for j in i:
                        f_string += f"{j},"
                    f_string = f_string[:-1]
                    f_string += "),"
                    f.write(f_string)
                f.write("]\n ")
        
        elif self.mode == "hex":
            for i in self.encoder.rectangles:
                for j in i[:4]:
                    if j >= 255:
                        raise ValueError("Maximum image size for hex mode is 254x254")
            with open("data.py", "w") as f:
                f.write(f"colors='")
                hex_string = ""
                for i in get_color_list():
                    hex_string += f"{i[0]:02x}{i[1]:02x}{i[2]:02x}"
                f.write(hex_string)
                f.write("'\n")
                f.write("rectangles='")
                last_color_index = -1
                hex_string = ""
                for i in get_rectangles():
                    if i[4] != last_color_index:
                        last_color_index = i[4]
                        hex_string += f"ff{i[4]:02x}"
                    hex_string += f"{i[0]:02x}{i[1]:02x}{i[2]:02x}{i[3]:02x}"
                f.write(hex_string)
                f.write("'\n")
                    
