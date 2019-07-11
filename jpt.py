import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

def submit(strvar, unique_cb, numeric_cb):
    popup_window = tk.Tk()
    tk.Label(popup_window, text=f"File analyzed: {strvar}").pack()
    tk.Label(popup_window, text=str(unique_cb) + str(numeric_cb) + "hello").pack()
    tk.Label(popup_window, text = "Results written to folder." )

    path = PurePath(strvar)
    jpt.main_processing(str(path), path.stem)

    popup_window.mainloop()

def browsefunc():
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)
    analyse.append(filename)


main_window = tk.Tk()

analyse = [] # super hack to create a persistance that I can use later
str_var = tk.StringVar()
int_var = tk.IntVar()
unique_var = tk.BooleanVar()
numeric_var = tk.BooleanVar()
fname = tk.StringVar()

tk.Label(main_window, text="").grid(row=1, column=0)
tk.Label(main_window, text="Calculate uniqueness?:").grid(row=2, column=0)
tk.Label(main_window, text="Calculate percent numeric?:").grid(row=3, column=0)


int_entry = tk.Entry(main_window, textvariable=int_var)
fileselect = tk.Button(main_window, text="Select the file", command=lambda: browsefunc())

#Notice, instead of text variable, I am using variable for Checkbutton widget.
unique_entry = tk.Checkbutton(main_window,  variable=unique_var)
bln_chbtn = tk.Checkbutton(main_window, variable=numeric_var)
pathlabel = tk.Label(main_window)

pathlabel = tk.Label(main_window)
# pathlabel.pack()


fileselect.grid(row=1, column=1)
unique_entry.grid(row=2, column=1)
bln_chbtn.grid(row=3, column=1)
pathlabel.grid(row = 0, column = 0)

submit_btn = tk.Button(main_window, text="Click submit to execute the analysis.", command=lambda: submit(analyse[0], \
                                                                                                         unique_var.get(), numeric_var.get()))
submit_btn.grid(row=4, column=1)

main_window.mainloop()
