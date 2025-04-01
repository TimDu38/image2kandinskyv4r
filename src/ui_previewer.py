import tkinter as tk
import time
import math
class Previewer(tk.Canvas):
    """Previewer class to display the image preview and rectangles count.
    Inherits from tk.Canvas.
    Attributes:
        parent (tk.Tk): Parent window.
        rectangles_list (list): List of rectangles to be rendered.
        rectangles_count (int): Total number of rectangles.
        img_size (tuple): Size of the image.
        colors_count (int): Number of unique colors in the image.
        scaling_factor (int): Scaling factor for rendering rectangles.
        frame (int): Current frame being rendered.
        enabled (bool): Indicates if the previewer is enabled.
        cooldown (float): Time interval between rendering frames.
        timestamp (float): Timestamp for the last rendered frame.
        offset (tuple): Offset for positioning rectangles on the canvas.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.rectangles_list = None
        self.rectangles_count = None
        self.img_size = None
        self.colors_count = None
        self.scaling_factor = None
        self.frame = None
        self.enabled = False
        self.cooldown = None
        self.timestamp = None
        self.offset = None
        self.step_render_rectangles(self.parent.encoder)

    @staticmethod
    def convert_to_hex(rgb):
        """Convert RGB tuple to hex string."""
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    

    def enable(self, encoder_obj):
        """Enable the previewer and start rendering rectangles. Args:
        encoder_obj (Encoder): Encoder object containing image data and rectangles."""

        self.delete("all")
        self.rectangles_list = list(set(encoder_obj.rectangles.copy())) if self.parent.encoder.alpha_mode in encoder_obj.palette else [encoder_obj.rectangles[0]] + list(set(encoder_obj.rectangles.copy()[1:]))
        self.rectangles_count = len(self.rectangles_list)
        self.frame = 0 
        self.enabled = True
        self.cooldown = 5 / self.rectangles_count
        self.timestamp = time.monotonic()
        self.scaling_factor = max(math.floor(min(256 / encoder_obj.size[0], 224 / encoder_obj.size[1])),1)
        self.img_size = encoder_obj.size
        self.colors_count = len(encoder_obj.palette)
        self.offset = (256 - self.img_size[0] * self.scaling_factor) // 2, (224 - self.img_size[1] * self.scaling_factor) // 2
        self.config(highlightbackground="#000000")
        self.config(bg="#222222")
        if encoder_obj.alpha_mode:
            switch = False
            square_size = self.scaling_factor
            for y in range(self.offset[1], self.img_size[1] * self.scaling_factor + self.offset[1], square_size):
                for x in range(self.offset[0], self.img_size[0] * self.scaling_factor + self.offset[0], square_size):
                    color = "#BFBFBF" if switch else "#808080"
                    self.create_rectangle(x, y, x + square_size, y + square_size, fill=color, outline="")
                    switch = not switch
                switch = not switch
    

    def step_render_rectangles(self, encoder_obj):
        """Render rectangles step by step.
        Args: 
        encoder_obj (Encoder): Encoder object containing image data and rectangles."""
        while self.enabled and time.monotonic() - self.timestamp >= self.cooldown:
            self.timestamp += self.cooldown
            if self.frame < len(self.rectangles_list):
                rect = list(self.rectangles_list[self.frame])
                rect = [i * self.scaling_factor for i in rect[:-1]] + [rect[-1]]
                x, y, w, h, c = rect
                x2 = x + w + self.offset[0]
                y2 = y + h + self.offset[1]
                x += self.offset[0]
                y += self.offset[1]
                self.create_rectangle(x, y, x2, y2, fill=self.convert_to_hex(encoder_obj.palette[c]), outline="")
                self.frame += 1
                scale_text = f" (x{self.scaling_factor} scaled)" if self.scaling_factor != 1 else ""
                self.parent.rectangle_count_label.config(text=f"Rectangles count: {self.frame}/{self.rectangles_count} | Colors: {self.colors_count} | Size: {self.img_size[0]}x{self.img_size[1]}{scale_text}")
            else:
                self.enabled = False
        self.after(16, lambda: self.step_render_rectangles(encoder_obj))

