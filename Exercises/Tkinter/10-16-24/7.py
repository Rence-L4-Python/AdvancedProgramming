import tkinter as tk

root=tk.Tk()
root.title('Tkinter Pack Layout')
root.geometry('600x400')

label1=tk.Label(master=root,text='Pack',bg='red',fg='white')
label2=tk.Label(master=root,text='Pack',bg='green',fg='white')
label3=tk.Label(master=root,text='Pack',bg='blue',fg='white')
label4=tk.Label(master=root,text='Pack',bg='purple',fg='white')

label1.pack(side=tk.LEFT)
label2.pack(side=tk.LEFT, ipadx=40)
label3.pack(side=tk.LEFT, ipady=40)
label4.pack(side=tk.LEFT, ipadx=80, ipady=80)

root.mainloop()