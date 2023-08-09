import os
import random
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Directory path where flag images are stored
flags_directory = "flags"

# Dictionary to store counters for each flag file
counters = {}

# Function to handle the "Yes" button click event
def on_yes_click():
    global random_image_file
    if random_image_file:
        file_path = os.path.join(flags_directory, random_image_file)
        os.remove(file_path)
        print(f"Removed file: {random_image_file}")
        random_image_file = None
        show_random_image()

# Function to handle the "No" button click event
def on_no_click():
    global random_image_file
    counter = counters.get(random_image_file, 0)
    if counter > 0:
        counter = 0
        counters[random_image_file] = counter
        print(f"Counter for {random_image_file} reset to zero")
    random_image_file = None
    show_random_image()

# Function to handle the "+1" button click event
def on_plus_one_click():
    global random_image_file
    if random_image_file:
        counter = counters.get(random_image_file, 0)
        counter += 1
        counters[random_image_file] = counter
        print(f"Counter for {random_image_file}: {counter}")

        if counter >= 5:
            file_path = os.path.join(flags_directory, random_image_file)
            os.remove(file_path)
            print(f"Removed file: {random_image_file}")
            del counters[random_image_file]
        random_image_file = None
        show_random_image()

# Function to handle the "Show name" button click event
def on_show_name_click():
    global random_image_file
    if random_image_file:
        country_name = random_image_file.replace("flag_of_Flag of", "").replace(".png", "").strip()
        image = Image.open(os.path.join(flags_directory, random_image_file))

        # Convert image to RGB mode
        image = image.convert("RGBA")

        draw = ImageDraw.Draw(image)

        # Define text properties
        font_color = (255, 255, 255)  # White
        font_style = "arial.ttf"
        text_alignment = "center"
        border_color = (0, 0, 0)  # Black
        border_width = 2

        # Calculate the maximum font size that fits within the image width
        font_size = 40
        font = ImageFont.truetype(font_style, font_size)
        while draw.textbbox((0, 0), country_name, font=font)[2] > image.width:
            font_size -= 2
            font = ImageFont.truetype(font_style, font_size)

        # Calculate the position for the text
        text_bbox = draw.textbbox((0, 0), country_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        position = ((image.width - text_width) // 2, 0)

        # Adjust the position for horizontal alignment
        if text_alignment == "left":
            position = (0, position[1])
        elif text_alignment == "right":
            position = (image.width - text_width, position[1])

        # Add a border to the text
        border_box = (position[0] - border_width, position[1] - border_width,
                      position[0] + text_width + border_width, position[1] + font_size + border_width)
        draw.rectangle(border_box, fill=border_color)

        # Write the country name on the image
        draw.text(position, country_name, fill=font_color, font=font)

        # Convert modified image to PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Update the image in the image label
        image_label.configure(image=photo)
        image_label.image = photo

# Function to show a random flag image
def show_random_image():
    global random_image_file
    flag_files = [f for f in os.listdir(flags_directory) if f.endswith(".png")]
    if flag_files:
        random_image_file = random.choice(flag_files)
        image_path = os.path.join(flags_directory, random_image_file)
        image = Image.open(image_path)
        image = image.resize((300, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo
    else:
        random_image_file = None
        image_label.configure(image=None)

# Create the main window
root = Tk()
root.title("Flag Quiz")

# Create an image label to display the flag image
image_label = Label(root)
image_label.pack()

# Create a "Yes" button
yes_button = Button(root, text="Yes, I know it!", command=on_yes_click)
yes_button.pack(side=LEFT, padx=10, pady=10)

# Create a "No" button
no_button = Button(root, text="No, I do not know it.", command=on_no_click)
no_button.pack(side=LEFT, padx=10, pady=10)

# Create a "+1" button
plus_one_button = Button(root, text="+1", command=on_plus_one_click)
plus_one_button.pack(side=LEFT, padx=10, pady=10)

# Create a "Show name" button
show_name_button = Button(root, text="Show name", command=on_show_name_click)
show_name_button.pack(side=LEFT, padx=10, pady=10)

# Show the initial random image
random_image_file = None
show_random_image()

# Start the main event loop
root.mainloop()
