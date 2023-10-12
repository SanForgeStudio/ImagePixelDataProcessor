import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys

# Define the image file path
image_path = "data_image.png"

window = None  # Declare the window variable

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm *.tif *.tiff")])
    if file_path:
        display_image(file_path)

def exit_viewer():
    if window:
        window.destroy()

def display_image(image_path, resize_width=None, resize_height=None):
    global window  # Use the global window variable

    # Create a new window
    window = tk.Tk()
    window.title("Pixel Data Image Viewer")

    # Set the background color to black
    window.configure(bg="black")

    # Create a menu bar
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=exit_viewer)

    # Load and display the image with transparency
    image = Image.open(image_path)

    if resize_width and resize_height:
        image = image.resize((resize_width, resize_height))
    elif resize_width:
        aspect_ratio = image.width / image.height
        new_height = int(resize_width / aspect_ratio)
        image = image.resize((resize_width, new_height))
    elif resize_height:
        aspect_ratio = image.width / image.height
        new_width = int(resize_height * aspect_ratio)
        image = image.resize((new_width, resize_height))

    # Create a transparent image with the same size
    transparent_image = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # Paste the loaded image onto the transparent image
    transparent_image.paste(image, (0, 0), image)

    photo = ImageTk.PhotoImage(transparent_image)
    label = tk.Label(window, image=photo, bg="black")
    label.image = photo  # Keep a reference to the image
    label.pack()

    window.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        image_path = sys.argv[1]

    # You can specify the desired width and height for resizing
    display_image(image_path, resize_width=700, resize_height=600)
