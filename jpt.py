import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

def submit(strvar, unique_cb, numeric_cb, html_cb, excel_cb):
    popup_window = tk.Tk()
    tk.Label(popup_window, text=f"File analyzed: {strvar}").pack()

    resultsfolder = jpt.main_processing(meta['pathobj'], meta['stem'], unique = unique_cb, numeric = numeric_cb, html = html_cb, excel = excel_cb)
    meta['results'] = resultsfolder

    tk.Label(popup_window, text=f"Results saved to: {meta['results']}").pack()
    tk.Label(popup_window, text=f"Uniqueness calculation: {'ON' if unique_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Percent numeric calculation: {'ON' if numeric_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Write HTML file: {'ON' if html_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Write Excel file: {'ON' if html_cb else 'OFF'}").pack()


    popup_window.mainloop()

def browsefunc():
    filename = filedialog.askopenfilename()
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
html_var = tk.BooleanVar()
excel_var = tk.BooleanVar()

tk.Label(main_window, text="Click to select the file", anchor="e", width = 30).grid(row=1, column=0)
tk.Label(main_window, text="Calculate uniqueness?", anchor = 'e', width = 30).grid(row=2, column=0)
tk.Label(main_window, text="Calculate percent numeric?", anchor = 'e', width = 30).grid(row=3, column=0)
tk.Label(main_window, text="Write out HTML of profile?", anchor = 'e', width = 30).grid(row=4, column=0)
tk.Label(main_window, text="Write out Excel file of values and counts?", anchor = 'e', width = 30).grid(row=5, column=0)



fileselect = tk.Button(main_window, text="File browser", command=lambda: browsefunc())

unique_entry = tk.Checkbutton(main_window,  variable=unique_var)
bln_chbtn = tk.Checkbutton(main_window, variable=numeric_var)
html_chbtn = tk.Checkbutton(main_window, variable=html_var)
excel_chbtn = tk.Checkbutton(main_window, variable = excel_var)
pathlabel = tk.Label(main_window)

pathlabel = tk.Label(main_window)



fileselect.grid(row=1, column=1)
unique_entry.grid(row=2, column=1)
bln_chbtn.grid(row=3, column=1)
html_chbtn.grid(row=4, column=1)
excel_chbtn.grid(row = 5, column = 1)
pathlabel.grid(row = 0, column = 0, columnspan = 2)

submit_btn = tk.Button(main_window, text="Execute analysis",
                       command=lambda: submit(meta['pathobj'], unique_var.get(), numeric_var.get(), html_var.get(), excel_var.get()))
submit_btn.grid(row=6, column=1)

main_window.mainloop()
