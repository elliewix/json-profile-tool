import tkinter as tk
import json_profile_tools as jpt
from tkinter import filedialog
import os
from pathlib import PurePath

def submit(strvar, unique_cb, numeric_cb, html_cb, excel_cb, customname_entry):
    """creates popup window content and prompts the file processing to happen."""
    popup_window = tk.Tk()
    tk.Label(popup_window, text=f"File analyzed: {strvar}").pack()

    # run the analysis now, doing this before to retrieve the results folder name for display
    resultsfolder = jpt.main_processing(meta['pathobj'], customname_entry, unique = unique_cb, numeric = numeric_cb, html = html_cb, excel = excel_cb)
    meta['results'] = resultsfolder

    # add the labels
    tk.Label(popup_window, text=f"Results saved to: {meta['results']}").pack()
    tk.Label(popup_window, text=f"Uniqueness calculation: {'ON' if unique_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Percent numeric calculation: {'ON' if numeric_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Write HTML file: {'ON' if html_cb else 'OFF'}").pack()
    tk.Label(popup_window, text=f"Write Excel file: {'ON' if html_cb else 'OFF'}").pack()
    tk.Label(popup_window, text= f"Custom name was: {meta['results']}").pack()
    popup_window.mainloop()


def browsefunc(folder_input):
    """button behavior driving the file browsing button.
    Gathers the file path from the browse dialog box, and loads the meta dict with info on the file"""

    # get the file info
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
    path = PurePath(filename)
    pathlabel.config(text=filename)

    # load the meta dict with info about the file
    meta['pathobj'] = path
    meta['file'] = filename # exploiting function namespace scope to save this file name
    meta['stem'] = path.stem
    meta['results'] = PurePath(path.parent, path.stem) # make folder
    folder_input.insert(0, meta['results'])



main_window = tk.Tk()

meta = {} # persistant data storage during execution


# tk variables to hold behavior values
str_var = tk.StringVar()
int_var = tk.IntVar()
unique_var = tk.BooleanVar()
numeric_var = tk.BooleanVar()
fname = tk.StringVar()
html_var = tk.BooleanVar()
excel_var = tk.BooleanVar()
customname_var = tk.StringVar()

# add all the labels, all in colums 0
# leaves row 0 blank to display the selected file's path
tk.Label(main_window, text="Click to select the file", anchor="e", width = 30).grid(row=1, column=0)
tk.Label(main_window, text="Calculate uniqueness?", anchor = 'e', width = 30).grid(row=2, column=0)
tk.Label(main_window, text="Calculate percent numeric?", anchor = 'e', width = 30).grid(row=3, column=0)
tk.Label(main_window, text="Write out HTML of profile?", anchor = 'e', width = 30).grid(row=4, column=0)
tk.Label(main_window, text="Write out Excel file of values and counts?", anchor = 'e', width = 30).grid(row=5, column=0)
tk.Label(main_window, text = "Create custom output folder name", anchor = 'e', width = 30).grid(row = 6, column = 0)


# create all the buttons and check boxes
folder_name_entry = tk.Entry(main_window, textvariable = customname_var)

fileselect = tk.Button(main_window, text="File browser", command=lambda: browsefunc(folder_name_entry))
unique_entry = tk.Checkbutton(main_window,  variable=unique_var)
bln_chbtn = tk.Checkbutton(main_window, variable=numeric_var)
html_chbtn = tk.Checkbutton(main_window, variable=html_var)
excel_chbtn = tk.Checkbutton(main_window, variable = excel_var)
pathlabel = tk.Label(main_window)




# displaying all the buttons and such, each in column 1

pathlabel.grid(row = 0, column = 0, columnspan = 2) # span across both columns for space
fileselect.grid(row=1, column=1)
unique_entry.grid(row=2, column=1)
bln_chbtn.grid(row=3, column=1)
html_chbtn.grid(row=4, column=1)
excel_chbtn.grid(row = 5, column = 1)
folder_name_entry.grid(row = 6, column = 1)



# controller and placement for the submit button
submit_btn = tk.Button(main_window, text="Execute analysis",
                       command=lambda: submit(meta['pathobj'], unique_var.get(), numeric_var.get(), html_var.get(), excel_var.get(), folder_name_entry.get()))
submit_btn.grid(row=7, column=1)

main_window.mainloop()
