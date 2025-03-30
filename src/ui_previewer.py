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
        self.rectangles_list = encoder_obj.rectangles
        self.rectangles_count = len(self.rectangles_list)
        self.frame = 0 if encoder_obj.converter.alpha_mode else 1
        self.enabled = True
        self.cooldown = 5 / len(self.rectangles_list)
        self.timestamp = time.monotonic()
        self.scaling_factor = max(math.floor(min(256 / encoder_obj.size[0], 224 / encoder_obj.size[1])),1)
        self.img_size = encoder_obj.size
        self.colors_count = len(encoder_obj.unique_colors)
        self.offset = (256 - self.img_size[0] * self.scaling_factor) // 2, (224- self.img_size[1] * self.scaling_factor) // 2
        bg_color = encoder_obj.unique_colors[0]
        if bg_color is not None:
            self.config(bg=self.convert_to_hex(bg_color))
            self.config(highlightbackground=self.convert_to_hex(encoder_obj.unique_colors[1]))
        else:
            self.config(bg="#000000" if sum(encoder_obj.unique_colors[1]) > 382 else "#FFFFFF")
            self.config(highlightbackground="#FFFFFF" if sum(encoder_obj.unique_colors[1]) > 382 else "#000000")
        

    def step_render_rectangles(self, encoder_obj):
        """Render rectangles step by step.
        Args: 
        encoder_obj (Encoder): Encoder object containing image data and rectangles."""
        while self.enabled and time.monotonic() - self.timestamp >= self.cooldown:
            self.timestamp += self.cooldown
            if self.frame < len(self.rectangles_list):
                rect = list(self.rectangles_list[self.frame])
                rect = [i * self.scaling_factor for i in rect]
                x, y, w, h= rect
                x2 = x + w + self.offset[0]
                y2 = y + h + self.offset[1]
                x += self.offset[0]
                y += self.offset[1]
                self.create_rectangle(x, y, x2, y2, fill=self.convert_to_hex(encoder_obj.unique_colors[1]), outline="")
                self.frame += 1
                scale_text = f" (x{self.scaling_factor} scaled)" if self.scaling_factor != 1 else ""
                self.parent.rectangle_count_label.config(text=f"Rectangles count: {self.frame}/{self.rectangles_count} | Colors: {self.colors_count} | Size: {self.img_size[0]}x{self.img_size[1]}{scale_text}")
            else:
                self.enabled = False
        self.after(16, lambda: self.step_render_rectangles(encoder_obj))

