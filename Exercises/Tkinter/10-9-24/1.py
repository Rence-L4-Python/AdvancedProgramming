import tkinter as tk
window = tk.Tk()
greetings = tk.Label(text="Hello, Wednesday")
input = tk.Entry(fg="green", bg="blue", width=50)
greetings.pack()
input.pack()
window.mainloop()