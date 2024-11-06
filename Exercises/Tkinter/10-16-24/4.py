import tkinter as tk
from tkinter import ttk
root=tk.Tk()
root.geometry('300x200')
root.resizable(False,False)
root.title('Button Demo')
#exit button
exit.button=ttk.Button(root,text='Exit',command=lambda:root.quit())
exit.button.pack(ipadx=5,ipady=5,expand=True)
root.mainloop()