import tkinter as tk
from tkinter import ttk
root = tk.Tk()
def button_clicked():
    print('Button clicked')
button = ttk.Button(root, text="Click Me", command=button_clicked)
button.pack()
root.mainloop()