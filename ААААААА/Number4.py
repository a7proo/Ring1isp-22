from tkinter import *
class My_Window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("700x700")
        self.window.title("My OKNO")
        self.window.configure(bg="white")
        self.window.resizable(width=False, height=False)
        self.__my_canva()
        self.window.mainloop()
    def __my_canva(self):
        self.canva = Canvas(width=650, height=650, bg="blue")
        self.canva.pack()
        for i in range(10):
            if i % 3 == 0:
                color = "white"
            elif i == 2 or i == 5 or i == 8:
                color = "red"
            else:
                color = "green"
            self.canva.create_rectangle(150 + i * 10, 150 + i * 10, 350 - i * 10, 350 - i * 10,
                                        fill=color, outline="black", width=1)
new_window = My_Window()
