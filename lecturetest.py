import tkinter as tk
from random import randint

def roll_dice(label):
    label.config(text=f"{randint(1, 6)}")

main_window = tk.Tk()

main_window.geometry("100x50")

label = tk.Label(main_window, text="0")
label.pack()

roll_btn = tk.Button(main_window, text="Roll Die", command=lambda: roll_dice(label))
roll_btn.pack()

main_window.mainloop()
