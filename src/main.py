import tkinter as tk
from tkinter import messagebox, filedialog
from encoder import Encoder
from ui_previewer import Previewer


class App(tk.Tk):
    """Main application class for the Image to Numworks converter.
    Inherits from tk.Tk.
    Attributes:
        encoder (Encoder): Encoder object for converting images to rectangles.
        title_label (tk.Label): Label for the title of the application.
        image_label (tk.Label): Label for the preview section.
        canvas (Previewer): Canvas for rendering the image preview and rectangles.
        rectangle_count_label (tk.Label): Label for displaying the rectangles count and image size.
        file_path_label (tk.Label): Label for displaying the selected image file path.
        select_button (tk.Button): Button for selecting an image file.
        preview_button (tk.Button): Button for previewing the image.
        convert_button (tk.Button): Button for converting the image to rectangles.
        quit_button (tk.Button): Button for quitting the application.
        file_path (str): Path to the selected image file.
    """
    def __init__(self):
        super().__init__()
        self.encoder = Encoder(self)
        self.file_path = None
        self.palette_path = None
        self.configure_root()
        self.create_widgets()

    def configure_root(self):
        """"Configure the main window of the application."""

        self.title("Image to Numworks")
        self.geometry("640x480")
        self.resizable(False, False)
        self.configure(bg="#444444")
        self.protocol("WM_DELETE_WINDOW", self.quit)
    
    def create_widgets(self):
        """Create and place all widgets in the main window.
        This includes labels, buttons, and the preview canvas."""

        self.title_label = tk.Label(self, text="Image to Numworks (V4r)", font=("Arial", 20, "bold"), bg="#444444", fg="white")
        self.title_label.pack(pady=5)

        self.image_label = tk.Label(self, text="Preview", font=("Arial", 16, "bold"), bg="#444444", fg="white")
        self.image_label.pack(pady=5)

        self.canvas = Previewer(self, width=256, height=224, bg="#000000", highlightthickness=2, highlightbackground="#FFFFFF")
        self.canvas.pack()

        self.rectangle_count_label = tk.Label(self, text="Rectangles count: - | Colors - | Size: -", font=("Arial", 11, "bold"), bg="#444444", fg="white")
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

        button_frame_2 = tk.Frame(self, bg="#444444")
        button_frame_2.pack(pady=5)

        self.load_palette_button = tk.Button(button_frame_2, text="Load Palette", command=self.select_palette, bg="#CC00FF", fg="white")
        self.load_palette_button.pack(padx=5, side=tk.LEFT)

        self.unload_palette_button = tk.Button(button_frame_2, text="Unload Palette", command=self.reset_palette, bg="#B3B300", fg="white")
        self.unload_palette_button.pack(padx=5, side=tk.LEFT)

        self.palette_path_label = tk.Label(self, text="No custom palette selected", font=("Arial", 9, "bold"), bg="#444444", fg="white")
        self.palette_path_label.pack(pady=5)

    def select_image(self):
        """Open a file dialog to select an image file.
        The selected file path is stored in self.file_path."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*webp;*.bmp;*.gif")])
        if file_path != "":
            self.file_path = file_path
            self.encoder.path = self.file_path
            self.file_path_label.config(text=f"Image selected: {self.file_path}")
    

    def reset_palette(self):
        self.palette_path = None
        self.palette_path_label.config(text=f"No custom palette selected")


    def select_palette(self):
        """Open a file dialog to select a palette image file.
        The selected file path is stored in self.palette_path."""
        palette_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*webp;*.bmp;*.gif")])
        if palette_path != "":
            self.palette_path = palette_path
            try:
                self.encoder._open_palette()
                self.encoder._get_palette_colors()
                self.palette_path_label.config(text=f"Custom palette selected: {self.palette_path}")
            except Exception as e:
                self.reset_palette()
                messagebox.showerror("Error", str(e))
        else:
            self.reset_palette()


    def preview_image(self):
        """Preview the selected image by calling the convert_image method with "preview" mode."""
        self.convert_image("preview")
    
    
    def convert_image(self, mode=None):
        """Convert the selected image to rectangles and display them in the preview canvas.
        Args:
            mode (str): The mode of conversion. If "preview", only preview the image."""
        
        if self.file_path is not None:
            try:
                self.encoder.encode(mode)
                if mode != "preview":
                    messagebox.showinfo("Success", "Image converted successfully!")
                else:
                    self.canvas.enable()

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
        """Handle the closing event of the application."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
        