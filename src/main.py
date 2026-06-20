import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from encoder import Encoder
from ui_previewer import Previewer
from file_writer import FileWriter


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
        self.file_writer = FileWriter(self)
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

        self.style = ttk.Style(self)
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#444444")
        self.style.configure("TLabel", background="#444444", foreground="white")

        self.frame = ttk.Frame(self, style="TFrame")
        self.frame.pack(fill="both", expand=True)

        self.title_label = ttk.Label(self.frame, text="Image to Numworks (V4r)", font=("Arial", 20, "bold"), style="TLabel")
        self.title_label.pack(pady=5)

        self.image_label = ttk.Label(self.frame, text="Preview", font=("Arial", 16, "bold"), style="TLabel")
        self.image_label.pack(pady=5)

        self.canvas = Previewer(self.frame,self,  width=320, height=224, bg="#000000", highlightthickness=2, highlightbackground="#FFFFFF")
        self.canvas.pack()

        self.rectangle_count_label = ttk.Label(self.frame, text="Rectangles count: - | Colors - | Size: -", font=("Arial", 11, "bold"), style="TLabel")
        self.rectangle_count_label.pack()

        self.file_path_label = ttk.Label(self.frame, text="No image selected", font=("Arial", 10, "bold"), style="TLabel")
        self.file_path_label.pack(pady=5)


        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.pack(pady=5)

        self.style.configure("select.TButton", background="#4CAF50", foreground="white")
        self.select_button = ttk.Button(button_frame, text="Select Image", command=self.select_image, style="select.TButton")
        self.select_button.pack(padx=5, side=tk.LEFT)

        self.style.configure("preview.TButton", background="#FF9800", foreground="white")
        self.preview_button = ttk.Button(button_frame, text="Preview", command=lambda: self.convert_image("preview"), style="preview.TButton")
        self.preview_button.pack(padx=5, side=tk.LEFT)

        self.style.configure("convert.TButton", background="#2196F3", foreground="white")
        self.convert_button = ttk.Button(button_frame, text="Convert (Raw)", command=self.convert_image, style="convert.TButton")
        self.convert_button.pack(padx=(5, 0), side=tk.LEFT)

        self.convert_type_menu = tk.Menu(button_frame, tearoff=0, bg="#444444", fg="white")
        for mode_name in ["Raw", "Raw+", "Hex", "String", "String mini"]:
            self.convert_type_menu.add_command(label=mode_name, command=lambda m=mode_name: (self.file_writer.set_mode(m.lower()), self.convert_button.config(text=f"Convert ({m})")))



        def show_menu(event):
            self.dropdown_btn.config(relief="sunken", background="#FFFFFF", foreground="black")
            self.convert_type_menu.post(event.x_root, event.y_root)
            self.dropdown_btn.config(relief="raised", background="#2196F3", foreground="white")

        self.style.configure("dropdown.TLabel", background="#2196F3", foreground="white", bd=2, relief="raised", cursor="hand2")
        self.dropdown_btn = ttk.Label(button_frame, text="▼", style="dropdown.TLabel")
        self.dropdown_btn.pack(padx=(0, 5), side=tk.LEFT, ipady=4) # Its a pixel too small at the bottom and i hate it but im clueless on how to fix it
        self.dropdown_btn.bind("<Button-1>", show_menu)

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
            self.encoder.converted_flag = False
            self.file_path = file_path
            self.file_path_label.config(text=f"Image selected: {self.file_path}")
    

    def reset_palette(self):
        self.palette_path = None
        self.palette_path_label.config(text=f"No custom palette selected")
        self.encoder.converted_flag = False


    def select_palette(self):
        """Open a file dialog to select a palette image file.
        The selected file path is stored in self.palette_path."""
        palette_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*webp;*.bmp;*.gif")])
        if palette_path != "":
            self.palette_path = palette_path
            self.encoder.converted_flag = False
            try:
                self.encoder._open_palette_image()
                self.encoder._get_palette_colors()
                self.palette_path_label.config(text=f"Custom palette selected: {self.palette_path}")
            except Exception as e:
                self.reset_palette()
                messagebox.showerror("Error", str(e))
        else:
            self.reset_palette()

    
    def convert_image(self, mode=None):
        """Convert the selected image to rectangles and display them in the preview canvas.
        Args:
            mode (str): The mode of conversion. If "preview", only preview the image."""
        
        if self.file_path is not None:
            try:
                if not self.encoder.converted_flag:
                    self.encoder.encode()
                    self.canvas.load_data()
                if mode != "preview":
                    self.file_writer.write()
                    messagebox.showinfo("Success", f"Image converted successfully! ({self.file_writer.mode}) \n Character count: {self.file_writer.get_char_count()}")
                    if not self.encoder.converted_flag and self.canvas.frame == 0:
                        self.canvas.enable()
                else:
                    self.canvas.enable()
                self.encoder.converted_flag = True

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
        