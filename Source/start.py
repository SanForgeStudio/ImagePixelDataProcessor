import os
import subprocess
from PIL import Image
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the image file path
image_path = "data_image.png"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_image(image_path):
    try:
        subprocess.Popen(['python', 'image_viewer.py', image_path])
    except Exception as e:
        print("Error opening image in the viewer:", e)

def process_pixel_data():
    clear_screen()
    # Open the selected desired image
    icon = Image.open("data_image.png")

    # Resize the image to your desired pixels
    icon = icon.resize((16, 16))

    # Get pixel data
    pixels = list(icon.getdata())

    # Author and Description
    output_lines = []
    output_lines.append(Fore.RED + "Generating Pixel Data...." + Style.RESET_ALL)
    output_lines.append("")

    # Create a single line for the iconRaw vector
    icon_raw_line = "PIXEL DATA OUTPUT:  { "

    # Bit mask to extract the RGB values (8 bits for each channel)
    rgb_mask = 0xFF

    for pixel in pixels:
        r, g, b = pixel[:3]
        pixel_value = (r & rgb_mask) | ((g & rgb_mask) << 8) | ((b & rgb_mask) << 16)
        icon_raw_line += str(pixel_value) + ","
    icon_raw_line = icon_raw_line.rstrip(",") + " };"

    # Append the iconRaw line to the output lines
    output_lines.append(icon_raw_line)

    # Join the output lines into a single string
    output_str = '\n'.join(output_lines)

    # Display the output string
    print(output_str)

    # Save the output to a text file
    with open("pixel_data_output.txt", "w") as file:
        file.write(output_str)

    # Add a line break for visual separation
    print()

    # Wait for user input to keep the program active
    input("Press Enter to return to the Main Menu...")

while True:
    clear_screen()
    print(Fore.RED + "Created by: SanForge Studio" + Style.RESET_ALL)
    print()
    print(Fore.GREEN + "1.  Initialize Pixel Data Process" + Style.RESET_ALL)
    print(Fore.GREEN + "2.  View Specified Image" + Style.RESET_ALL)
    print(Fore.GREEN + "3.  Exit" + Style.RESET_ALL)
    print()
    choice = input("Select an option (1, 2, or 3): ")

    if choice == "1":
        process_pixel_data()
    elif choice == "2":
        display_image(image_path)
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please select a valid option 1, 2, or 3.")
