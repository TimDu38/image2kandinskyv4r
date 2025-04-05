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

        def get_color_list():
            return self.encoder.unique_colors if self.app.palette_path is None else self.encoder.palette_unique_colors
        
        def get_rectangles():
            return sorted(self.encoder.rectangles, key=lambda e: e[4]) if self.encoder.alpha_mode else [self.encoder.rectangles[0]] + sorted(self.encoder.rectangles[1:], key=lambda e: e[4])
        
        if self.mode == "raw":
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
                for i in self.encoder.rectangles:
                    f_string = "("
                    for j in i:
                        f_string += f"{j},"
                    f_string = f_string[:-1]
                    f_string += "),"
                    f.write(f_string)
                f.write("]\n ")
        
        else:
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
                    
