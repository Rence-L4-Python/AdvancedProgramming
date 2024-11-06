import tkinter as tk
window = tk.Tk()
entry = tk.Entry(bg="blue", fg="green")
name = entry.get()
Label = tk.Label(text=name)
entry.pack()
Label.pack()
entry.delete(0,tk.END)
window.mainloop()