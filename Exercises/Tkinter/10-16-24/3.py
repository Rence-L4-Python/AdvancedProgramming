import tkinter as tk
from tkinter import ttk
#Create the root window
root=tk.Tk()
root.geometry('300x300')
root.resizable(False,False)
root.title('Label widget Image')
#Display
photo=tk.PhotoImage(file='download.png')
image_label=ttk.Label(root,image=photo,padding=5, text='Python', compound='none')
image_label.pack()
root.mainloop()