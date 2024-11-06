import tkinter as tk
from tkinter import filedialog


def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get("1.0", tk.END))


root = tk.Tk()
root.title("Save As Example")


text_area = tk.Text(root, wrap='word')
text_area.pack(expand=1, fill='both')


save_button = tk.Button(root, text="Save As", command=save_file)
save_button.pack()


root.mainloop()
