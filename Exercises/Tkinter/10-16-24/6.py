import tkinter as tk
root=tk.Tk()
root.title('Tkinter Pack Layout')
root.geometry('600x400')

label1=tk.Label(master=root,text='Tkinter',bg='red',fg='white')
label2=tk.Label(master=root,text='Pack Layout',bg='green',fg='white')
label3=tk.Label(master=root,text='Fill',bg='blue',fg='white')
label4=tk.Label(master=root,text='Demo',bg='purple',fg='white')

label1.pack(side=tk.TOP,expand=True,fill=tk.Y)
label2.pack(side=tk.TOP,expand=True,fill=tk.X)
label3.pack(side=tk.TOP,expand=True,fill=tk.NONE)
label4.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

root.mainloop()