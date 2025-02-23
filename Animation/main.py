from tkinter import *

window = Tk()

window.geometry("500x500")

canva = Canvas(width=500, height=500, bg="lightgreen")
canva.pack()

rect1 = canva.create_rectangle(50,50,100,100,fill="blue")

canva.itemconfig(rect1, tags=("rect"))
canva.tag_bind('rect', '<Button-1>')
window.mainloop()