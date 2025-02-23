import random
from tkinter import *
from tkinter import messagebox

def start():
    for ball in balls:
        step = random.randint(1, 20)
        canva.move(ball, step, 0)
        if canva.coords(ball)[2] >= 500:
            winner_color = canva.itemcget(ball, 'fill')
            messagebox.showinfo("Победа!", f"Выиграл шар цвета: {winner_color}")
            return
    canva.after(50, start)

def reset():
    for ball in balls:
        canva.move(ball, -canva.coords(ball)[0] + 50, -canva.coords(ball)[1] + 50)

window = Tk()
window.geometry("500x500")

canva = Canvas(width=500, height=500, bg="lightgreen")
canva.pack()
balls = [
    canva.create_oval(50, 50, 100, 100, fill="red"),
    canva.create_oval(50, 150, 100, 200, fill="green"),
    canva.create_oval(50, 250, 100, 300, fill="blue"),
    canva.create_oval(50, 350, 100, 400, fill="white")
]

btn_start = Button(text="Старт", font="Arial 15", command=start)
btn_start.place(x=400, y=10)

btn_reset = Button(text="Reset", font="Arial 15", command=reset)
btn_reset.place(x=400, y=50)

window.mainloop()