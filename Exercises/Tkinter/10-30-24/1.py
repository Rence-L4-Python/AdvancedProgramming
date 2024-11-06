from tkinter import *

main = Tk()
txtarea = Text(main, width=40, height=10)
txtarea.place(x=20, y=40, height=125, width=200)

def openFile():
    with open('Readfile1.txt') as file_handler:
        contents = file_handler.read()
        txtarea.insert(END, contents)
        print(contents)

txtarea.delete("1.0","end")

Button(
    main,
    text="Open File",
    command=openFile).place(x=20,y=200,height=25,width=200)

main.update()
main.mainloop()



