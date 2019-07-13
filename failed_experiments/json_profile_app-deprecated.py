import json_profile_tools as  jpt
import json
from tkinter import filedialog
import tkinter as tk
import os

infile = ""



def get_input_file(root):
    root.filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
    infile = root.filename
    label = tk.Label(root, text=f"You entered: " + infile + "\nLoading file and writing results")
    label.pack()
    jpt.main_processing(infile, 'testout')

    return root.filename

#Create the Tk object (or our main window object)
main_window = tk.Tk()

#Set our window to be 400 pixels (width) by 100 pixels (height)
#Try changing these values to see the effects.
main_window.geometry("400x400")

#Set the title of our window.
main_window.title("JSON Profiling Tool")

north_lbl = tk.Label(main_window, text="Create a JSON profile\nSelect the file source below.")
north_lbl.pack()

roll_btn = tk.Button(main_window, text="Select a file", command=lambda: get_input_file(main_window))
roll_btn.pack()

uniqueness_var = tk.BooleanVar()
percent_numeric_var = tk.BooleanVar()

uniqueness_cb = tk.Checkbutton(main_window, text="Pepperoni", variable=uniqueness_var, onvalue="Pepperoni", offvalue="None")
percent_numeric_cb = tk.Checkbutton(main_window, text="Sausage", variable=percent_numeric_var, onvalue="Sausage", offvalue="None")

# When any of the checkbuttons get turned on or off, the corresponding string variable objects
# will be set to the respective state value (onvalue and offvalue).
label1 = tk.Label(main_window, text="Compute uniqueness")
label2 = tk.Label(main_window, text="Compute percent numeric")

# label1.grid(row=0, column=1)
# label2.grid(row=1, column=1)

unique_chbtn = tk.Checkbutton(main_window, variable=uniqueness_var)
pernumeric_chbtn = tk.Checkbutton(main_window, variable=percent_numeric_var)

print("unique", uniqueness_var, 'percent', percent_numeric_var)

#Start our window
main_window.mainloop()


# jex = """{
#     "glossary": {
#         "title": "example glossary",
# 		"GlossDiv": {
#             "title": "S",
# 			"GlossList": {
#                 "GlossEntry": {
#                     "ID": "SGML",
# 					"SortAs": "SGML",
# 					"GlossTerm": "Standard Generalized Markup Language",
# 					"Acronym": "SGML",
# 					"Abbrev": "ISO 8879:1986",
# 					"GlossDef": {
#                         "para": "A meta-markup language, used to create markup languages such as DocBook.",
# 						"GlossSeeAlso": ["GML", "XML"]
#                     },
# 					"GlossSee": "markup"
#                 }
#             }
#         }
#     }
# }"""
#
# # example on one record
# sample = json.loads(jex)
#
# # print(process_record(sample))
#
# # example on a file of records
#

