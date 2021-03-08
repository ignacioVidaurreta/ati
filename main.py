import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

# This method is just a POC and will be replaced
def do_useless_thing(img):
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 250), Image.ANTIALIAS)

    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)

    # create a label
    panel = tk.Label(top, image = img)

    # set the image as img
    panel.image = img
    panel.grid(row = 1)

def get_image():
    # Select imagename from folder
    img_name = fd.askopenfilenames()
    if len(img_name) == 0:
        print("No image selected")
        return

    img_name = img_name[0]
    # Open image
    img = Image.open(img_name)

    do_useless_thing(img)

# Creates the window
top = tk.Tk()

top.title("Image uploader - ATI")
top.geometry("550x300")
top.resizable(width= True, height=True)
top.grid_columnconfigure(2, weight=0)
top.grid_rowconfigure(1, weight=1)
top.grid_rowconfigure(2, weight=0)

btn = tk.Button(top, text="upload image", command=get_image).grid(row=4, column=2, columnspan=2)

top.mainloop()