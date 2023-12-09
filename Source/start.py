import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import time

# Define the image file path
image_path = "data_image.png"

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm *.tif *.tiff")])
    if file_path:
        # Save the selected image as data_image.png
        image = Image.open(file_path)
        image.save(image_path)

def view_image():
    display_image(image_path)

def display_image(image_path, resize_width=None, resize_height=None):
    # Create a new window for the image
    image_window = Tk()
    image_window.title("Pixel Data Image Viewer")

    # Set the background color to black
    image_window.configure(bg="black")

    # Prevent going full screen and leave space for the taskbar
    image_window.geometry("800x600")  # Set the initial size as needed
    image_window.minsize(400, 300)  # Set a minimum size
    image_window.maxsize(800, 600)  # Set a maximum size
    image_window.resizable(False, False)  # Disable window resizing

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
    label = Label(image_window, image=photo, bg="black")
    label.image = photo  # Keep a reference to the image
    label.pack(fill=BOTH, expand=YES)  # Make the label fill the window

    image_window.mainloop()

def process_pixel_data(output_text_widget):
    output_text_widget.config(state=NORMAL)
    output_text_widget.delete(1.0, END)  # Clear the previous output

    # Create a tag for dark blue text
    output_text_widget.tag_configure("blue", foreground="dark blue")

    # Create a tag for green text
    text_widget.tag_configure("green", foreground="green")

    # Create a tag for red text
    output_text_widget.tag_configure("red", foreground="red")

    # Display "Generating Pixel Data" in red with a delay
    output_text_widget.insert(END, "Generating Pixel Data", "red")
    output_text_widget.update()
    time.sleep(1)  # 1-second delay

    # Add a delay between displaying the dots
    for _ in range(4):
        output_text_widget.insert(END, ".", "red")
        output_text_widget.update()
        time.sleep(1)  # 1-second delay

    # Open the selected desired image
    icon = Image.open("data_image.png")

    # Resize the image to your desired pixels
    icon = icon.resize((16, 16))

    # Get pixel data
    pixels = list(icon.getdata())

    # Create a single line for the iconRaw vector
    icon_raw_line = "{ "

    # Bit mask to extract the RGB values (8 bits for each channel)
    rgb_mask = 0xFF

    for pixel in pixels:
        r, g, b = pixel[:3]
        pixel_value = (r & rgb_mask) | ((g & rgb_mask) << 8) | ((b & rgb_mask) << 16)
        icon_raw_line += str(pixel_value) + ","
    icon_raw_line = icon_raw_line.rstrip(",") + " }"

    # Append the iconRaw line to the output
    output_text_widget.insert(END, "\n\n", "blue")
    output_text_widget.insert(END, icon_raw_line + "\n\n", "blue")
    output_text_widget.insert(END, "Pixel data has been created!", "green")

    # Save the output to a text file (optional)
    with open("pixel_data_output.txt", "w") as file:
        file.write(icon_raw_line)

    # Make the text widget read-only
    output_text_widget.config(state='disabled')

# Create a new window for the main application
root = Tk()
root.title("Pixel Data Generator")

# Set the window icon
root.iconbitmap("app.ico")

# Create a menu bar
menubar = Menu(root)
root.config(menu=menubar)

# File menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Replace Image", command=open_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


# Add a new menu for Settings Size
settings_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settings_menu)


# Add a new menu for Tools Size
tool_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tools", menu=tool_menu)


# Create a frame for the side panel
side_panel = Frame(root, bg="gray", width=150)
side_panel.pack(side=LEFT, fill="y")

# Create a button to generate pixel data
generate_button = Button(side_panel, text="Generate Pixel Data", width=20, command=lambda: process_pixel_data(text_widget))
generate_button.pack(pady=5)

def return_to_menu():
    display_menu()
    

# Create a button to return to the main menu
menu_button = Button(side_panel, text="Return to Menu", width=20, command=return_to_menu)
menu_button.pack(pady=5)

def display_menu():
    text_widget.config(state='normal')  # Enable text widget for backend updates
    text_widget.delete(1.0, END)  # Clear the previous output
    
    # Set the text color to #ff3d00
    text_widget.tag_configure("info", foreground="#ff3d00")

    text_widget.insert(END, "Welcome to the Pixel Data Image Processor!\n", "info")
    text_widget.insert(END, "Created by: SanForge Studio\n", "info")
    text_widget.insert(END, "Version: 1.2\n", "info")
    text_widget.insert(END, "\n", "info")
    text_widget.insert(END, "========================================\n\n", "info")
    text_widget.insert(END, "Instructions:\n\n", "info")
    text_widget.insert(END, "1. Click on 'File' in the top left menu bar and select 'Open Image' to load your desired image.\n", "info")
    text_widget.insert(END, "2. After loading the image, you can generate the pixel data by clicking 'Generate Pixel Data'.\n", "info")
    text_widget.insert(END, "3. To return to the main menu, click 'Return to Menu'.\n\n", "info")

    text_widget.insert(END, "Have fun processing pixel data for your images!\n", "info")

    
    # Add an empty line
    text_widget.insert(END, "\n")

    # Make the text widget read-only
    text_widget.config(state='disabled')

# Create a text widget for output with a smaller font size
text_font = ('Arial', 10)  # Smaller font size
text_widget = Text(root, state='disabled', font=text_font)
text_widget.pack(fill=BOTH, expand=YES)  # Make the text widget fill the window

display_menu()

root.mainloop()
