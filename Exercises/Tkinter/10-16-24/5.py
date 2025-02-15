import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
# root window
root=tk.Tk()
root.geometry('300x200')
root.resizable(False,False)
root.title('Image Button Demo')
# download button
def download_clicked():
    showinfo(
        title='Information',
        message='Download button clicked!'
    )
download_icon=tk.PhotoImage(file='Download.png')
download_button=ttk.Button(
    root,
    image=download_icon,
    command=download_clicked
)
download_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)
root.mainloop()