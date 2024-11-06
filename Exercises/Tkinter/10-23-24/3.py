from tkinter import *
from tkinter import filedialog

def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
    pathh.insert(END, tf)
    tf = open(tf)  # or tf = open(tf, 'r')
    data = tf.read()
    txtarea.insert(END, data)
    tf.close()

tk = Tk()
tk.title("PythonGuides")
tk.geometry("400x450")
tk['bg']='#fb0'

txtarea = Text(tk, width=40, height=20)
txtarea.pack(pady=20)

pathh = Entry(tk)
pathh.pack(side=LEFT, expand=True, fill=X, padx=20)


Button(
    tk, 
    text="Open File", 
    command=openFile
    ).pack(side=RIGHT, expand=True, fill=X, padx=20)

tk.mainloop()
