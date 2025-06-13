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
            
        def get_deltas(second_mode=False):
            deltas = []
            last_x, last_y, last_color = 0, 0, 0
            for rect in get_rectangles_2():
                x, y, xs, ys, color = rect[0], rect[1], rect[2], rect[3], rect[4]
                dx, dy, dcolor = x - last_x, y - last_y, color - last_color
                if second_mode:
                    if dx < 0: # if negative, write the absolute value instead of delta and add 1M (to flag it later) (its fucking stupid, but works)
                        dx = x + 1_000_000 # use a large value to indicate absolute position
                    if dy < 0:
                        dy = y + 1_000_000 # use a large value to indicate absolute position 
                    if dcolor < 0:
                        dcolor = color + 1_000_000 # use a large value to indicate absolute position
                if dcolor != 0:
                    deltas.append((dx, dy, xs, ys, dcolor))
                else:
                    deltas.append((dx, dy, xs, ys))
                last_x, last_y, last_color = x % 1_000_000, y % 1_000_000, color % 1_000_000
            return deltas   

        def convert_value_to_string(value):
            if value >= 1_000_000: # if value is equal or larger than 1E6, it is an absolute position
                value -= 1_000_000 # no way you can write numbers with underscores i learned ts only now
                reset_track_flag = "!"
            else:
                reset_track_flag = ""
            msb = value // 64
            lsb = value % 64
            if msb == 0:
                return reset_track_flag + chr(lsb + 35)
            else:
                return reset_track_flag + chr(msb + 104) + chr(lsb + 35)

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
                for j in i:
                    if j >= 255:
                        raise ValueError("Maximum image size/unique colors count for hex mode is 254x254 / 255 colors")
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
        
        elif self.mode == "string":
            
            for i in self.encoder.rectangles:
                for j in i:
                    if j >= 1024:
                        raise ValueError("Maximum image size/unique colors count for string mode is 1023x1023 / 1024 colors")
            
            with open("data.py", "w") as f:
                f.write(f'colors=r"')
                color_list_string = ""
                for i in get_color_list(rescale=False):
                    for j in i:
                        color_list_string += convert_value_to_string(j)
                f.write(color_list_string)
                f.write('"\nrectangles=r"')
                rectangles = get_deltas(second_mode=True)
                rectangles_string = ""
                for rect in rectangles:
                    for k, j in enumerate(rect):
                        if k == 4:
                            rectangles_string += " " # special character for color index change
                        rectangles_string += convert_value_to_string(j)
                f.write(rectangles_string)
                f.write('"\n')

        elif self.mode == "string mini":
            for i in self.encoder.rectangles:
                for j in i:
                    if j >= 92:
                        raise ValueError("Maximum image size/unique colors count for string mini mode is 91x91 / 92 colors")
            with open("data.py", "w") as f:
                f.write(f'colors=r"')
                color_list_string = ""
                for i in get_color_list(rescale=False):
                    for j in i:
                        color_list_string += convert_value_to_string(j)
                f.write(color_list_string)
                f.write('"\nrectangles=r"')
                rectangles = get_rectangles_2()
                new_rectangles = []
                last_color = -1
                for rect in rectangles:
                    if rect[4] != last_color:
                        last_color = rect[4]
                        new_rectangles.append((rect[0], rect[1], rect[2], rect[3], last_color))
                    else:
                        new_rectangles.append((rect[0], rect[1], rect[2], rect[3]))

                rectangles_string = ""
                for rect in new_rectangles:
                    for k, j in enumerate(rect):
                        if k == 4:
                            rectangles_string += " "
                        rectangles_string += convert_value_to_string(j)
                f.write(rectangles_string)
                f.write('"\n')

