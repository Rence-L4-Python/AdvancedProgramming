import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

container = tk.Frame(self)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1) 

self.frames = {}

for F in (StartPage, Page1, Page2):
    frame = F(container, self)
    self.frames[F] = frame
    frame.grid(row=0, column=0, sticky="nsew") 

self.show_frame(StartPage)

def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()

class BasePage(tk.Frame):
    def __init__(self, parent, controller, title):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text=title, font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

    def create_button(self, text, row, column, target_frame):
        button = ttk.Button(self, text=text, command=lambda: self.controller.show_frame(target_frame))
        button.grid(row=row, column=column, padx=10, pady=10)

class StartPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "StartPage")
        self.create_button("Page 1", 1, 0, Page1)
        self.create_button("Page 2", 2, 0, Page2)

class Page1(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Page 1")
        self.create_button("StartPage", 1, 0, StartPage)
        self.create_button("Page 2", 2, 0, Page2)

class Page2(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Page 2")
        self.create_button("Page 1", 1, 0, Page1)
        self.create_button("StartPage", 2, 0, StartPage)

# Driver code
app = tkinterApp()
app.mainloop()
