import os
import tkinter as tk

def open_file():
    file_path = "srdetfgyu.py"
    os.startfile(file_path)

root = tk.Tk()

button = tk.Button(root, text="Открыть файл", command=open_file)
button.pack()

root.mainloop()
