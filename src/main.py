import tkinter as tk
import time
import math
from tkinter import messagebox, filedialog
from encoder import Encoder


class Previewer(tk.Canvas):
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
    
    def convert_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    

    def enable(self, encoder_obj):

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
        self.step_render_rectangles(encoder_obj)
        

    def step_render_rectangles(self, encoder_obj):
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
                self.parent.rectangle_count_label.config(text=f"Rectangles count: {self.frame}/{self.rectangles_count} | Colors: {self.colors_count} | Size: {self.img_size[0]}x{self.img_size[1]} (x{self.scaling_factor} scaled)")
            else:
                self.enabled = False
        self.after(10, lambda: self.step_render_rectangles(encoder_obj))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.encoder = Encoder()
        self.configure_root()
        self.create_widgets()

    def configure_root(self):
        self.title("Image to Numworks")
        self.geometry("560x420")
        self.resizable(False, False)
        self.configure(bg="#444444")
        self.protocol("WM_DELETE_WINDOW", self.quit)
    
    def create_widgets(self):
        self.title_label = tk.Label(self, text="Image to Numworks (V4r)", font=("Arial", 20, "bold"), bg="#444444", fg="white")
        self.title_label.pack(pady=5)

        self.image_label = tk.Label(self, text="Preview", font=("Arial", 16, "bold"), bg="#444444", fg="white")
        self.image_label.pack(pady=5)

        self.canvas = Previewer(self, width=256, height=224, bg="#000000", highlightthickness=2, highlightbackground="#FFFFFF")
        self.canvas.pack()

        self.rectangle_count_label = tk.Label(self, text="Rectangles count: - | Colors - | Size: -", font=("Arial", 10, "bold"), bg="#444444", fg="white")
        self.rectangle_count_label.pack()

        self.file_path_label = tk.Label(self, text="No image selected", font=("Arial", 10, "bold"), bg="#444444", fg="white")
        self.file_path_label.pack(pady=5)

        button_frame = tk.Frame(self, bg="#444444")
        button_frame.pack(pady=5)

        self.select_button = tk.Button(button_frame, text="Select Image", command=self.select_image, bg="#4CAF50", fg="white")
        self.select_button.pack(padx=5, side=tk.LEFT)

        self.preview_button = tk.Button(button_frame, text="Preview", command=self.preview_image, bg="#FF9800", fg="white")
        self.preview_button.pack(padx=5, side=tk.LEFT)

        self.convert_button = tk.Button(button_frame, text="Convert", command=self.convert_image, bg="#2196F3", fg="white")
        self.convert_button.pack(padx=5, side=tk.LEFT)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.on_closing, bg="#F44336", fg="white")
        self.quit_button.pack(padx=5, side=tk.LEFT)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*webp;*.bmp;*.gif")])
        if file_path != "":
            self.file_path = file_path
            self.encoder.path = self.file_path
            if self.file_path:
                self.file_path_label.config(text=f"Selected: {self.file_path}")
    
    def preview_image(self):
        self.convert_image("preview")
    
    
    def convert_image(self, mode=None):
        if hasattr(self, 'file_path'):
            try:
                self.encoder.encode(mode)
                if mode != "preview":
                    messagebox.showinfo("Success", "Image converted successfully!")
                else:
                    self.canvas.enable(encoder_obj=self.encoder)

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            except IOError:
                messagebox.showerror("Error", "Cannot open image. Please check the file path.")
                return
            except Exception as e:
                messagebox.showerror("Error", e)
                return
        else:
            messagebox.showwarning("Warning", "Please select an image first.")
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
        