import tkinter as tk
root = tk.Tk()
from tkinter import filedialog

def browsefunc():
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)
    with open(filename, 'r') as foo:
        print(foo.read())

browsebutton = tk.Button(root, text="Browse", command=browsefunc)
browsebutton.pack()

pathlabel = tk.Label(root)
pathlabel.pack()


tk.mainloop()
