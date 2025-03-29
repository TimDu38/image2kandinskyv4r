import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
from encoder import Encoder

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
        self.configure(bg="#2E2E2E")
        self.protocol("WM_DELETE_WINDOW", self.quit)
    
    def create_widgets(self):
        self.title_label = tk.Label(self, text="Image to Numworks (V4r)", font=("Arial", 20, "bold"), bg="#2E2E2E", fg="white")
        self.title_label.pack(pady=5)

        self.image_label = tk.Label(self, text="Preview", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="white")
        self.image_label.pack(pady=5)

        self.canvas = tk.Canvas(self, width=256, height=224, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.file_path_label = tk.Label(self, text="No image selected", font=("Arial", 10, "bold"), bg="#2E2E2E", fg="white")
        self.file_path_label.pack(pady=5)

        button_frame = tk.Frame(self, bg="#2E2E2E")
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
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            except IOError:
                messagebox.showerror("Error", "Cannot open image. Please check the file path.")
                return
            #except Exception as e:
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
        