import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

def submit(strvar, unique_cb, numeric_cb):
    popup_window = tk.Tk()
    tk.Label(popup_window, text=f"File analyzed: {strvar}").pack()
    tk.Label(popup_window, text=f"Results saved to: {meta['results']}").pack()
    tk.Label(popup_window, text=f"Uniqueness calculation: {'ON' if unique_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Percent numeric calculation: {'ON' if numeric_cb else 'OFF'}").pack()

    jpt.main_processing(meta['pathobj'], meta['stem'], unique = unique_cb, numeric = numeric_cb)

    popup_window.mainloop()

def browsefunc():
    filename = filedialog.askopenfilename()
    print(filename)
    path = PurePath(filename)
    pathlabel.config(text=filename)
    meta['pathobj'] = path
    meta['file'] = filename # exploiting function namespace scope to save this file name
    meta['stem'] = path.stem
    meta['results'] = PurePath(path.parent, path.stem) # make folder

main_window = tk.Tk()

meta = {} # super hack to create a persistance outside of the function

str_var = tk.StringVar()
int_var = tk.IntVar()
unique_var = tk.BooleanVar()
numeric_var = tk.BooleanVar()
fname = tk.StringVar()

tk.Label(main_window, text="Click to select the file", anchor="e", width = 20).grid(row=1, column=0)
tk.Label(main_window, text="Calculate uniqueness?", anchor = 'e', width = 20).grid(row=2, column=0)
tk.Label(main_window, text="Calculate percent numeric?", anchor = 'e', width = 20).grid(row=3, column=0)


fileselect = tk.Button(main_window, text="File browser", command=lambda: browsefunc())

unique_entry = tk.Checkbutton(main_window,  variable=unique_var)
bln_chbtn = tk.Checkbutton(main_window, variable=numeric_var)
pathlabel = tk.Label(main_window)

pathlabel = tk.Label(main_window)



fileselect.grid(row=1, column=1)
unique_entry.grid(row=2, column=1)
bln_chbtn.grid(row=3, column=1)
pathlabel.grid(row = 0, column = 0, columnspan = 2)

submit_btn = tk.Button(main_window, text="Execute analysis",
                       command=lambda: submit(meta['pathobj'], unique_var.get(), numeric_var.get()))
submit_btn.grid(row=4, column=1)

main_window.mainloop()
