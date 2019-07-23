import tkinter as tk

def greet(name):
    popup_window = tk.Tk()
    greet_lbl = tk.Label(popup_window, text=f"Hello, {name}")
    greet_lbl.pack()
    popup_window.mainloop()

main_window = tk.Tk()

main_window.geometry("200x50")

name_lbl = tk.Label(main_window, text="Name: ")
name_lbl.pack(side=tk.LEFT)

name_entry = tk.Entry(main_window)

#name_entry.get() is retrieving the typed in string
name_entry.bind('<Return>', lambda event: greet(name_entry.get()))
name_entry.pack(side=tk.LEFT)

main_window.mainloop()
