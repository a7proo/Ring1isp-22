from tkinter import *
import random


def my_label(text, x, y, font, color):
   text = text
   x = x
   y = y
   font = font
   color = color
   label = Label(text=text, font=font, bg=color)
   label.place(x=x, y=y)


def spawn_snowflake():
   create_snowflake()
   canva.after(2000, spawn_snowflake)


def create_snowflake():
   x = random.randint(0, 600)
   y = 0
   snowflake = canva.create_image(x, y, image=image)
   snowflakes.append(snowflake)
   move_snowflake(snowflake)
def move_snowflake(snowflake):
   x, y = canva.coords(snowflake)
   canva.move(snowflake, 0, snowflake_speed)


   if y != 600:
       canva.after(50, move_snowflake, snowflake)
       check_collision()
   else:
       canva.delete(snowflake)
       snowflakes.remove(snowflake)
       create_snowflake()


def score_spawn():
   score_label = Label(text=f"SCORE: {score}", font="Arial 20", bg="white")
   score_label.place(x=30, y=30)


def korzina_move(event):
   key = event.keysym
   if key == "Left":
       canva.move(korzina, -10, 0)
   elif key == "Right":
       canva.move(korzina, 10, 0)


def increase_score():
   global score
   score += 1
   canva.config()
   score_spawn()


def check_collision():
   x, y = canva.coords(korzina)
   for snowflake in snowflakes:
       x1, y1 = canva.coords(snowflake)
       if (x <= x1 + 50 and x >= x1 - 50) and (y == y1):
           increase_score()
           canva.delete(snowflake)
           snowflakes.remove(snowflake)






window = Tk()
window.geometry("600x600")
window.title("SNEGOPAD")


snowflake_speed = 10
image = PhotoImage(file="snow.png")
canva = Canvas(window, width=600, height=600, bg="white")
canva.pack()


image_korzina = PhotoImage(file="snow.png")
korzina = canva.create_image(400, 500, image=image_korzina)


snowflakes = []


score = 0


score_spawn()


spawn_snowflake()


window.bind("<KeyPress>", korzina_move)


window.mainloop()
