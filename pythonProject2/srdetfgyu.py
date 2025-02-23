from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

class my_combobox:
    def __init__(self, list, font, x, y, width, window):
        self.x = x
        self.y = y
        self.list = list
        self.font = font
        self.width = width

        self.combobox = Combobox(values=self.list, font=self.font, state="readonly")
        self.combobox.place(x=self.x, y=self.y,width=self.width)
        self.combobox.bind('<<ComboboxSelected>>', lambda event: self.select())

    def select(self):
        global price, servis_combobox
        if self.combobox.get() == self.list[0]:
            self.price = 1000
        elif self.combobox.get() == self.list[1]:
            self.price = 1001
        elif self.combobox.get() == self.list[2]:
            self.price = 8420
        elif self.combobox.get() == self.list[3]:
            self.price = 5236
        elif self.combobox.get() == self.list[4]:
            self.price = 3213
        elif self.combobox.get() == self.list[5]:
            self.price = 9724
        elif self.combobox.get() == self.list[6]:
            self.price = 8763
        else:
            self.price = 0

        price = self.price
        servis_combobox = self.combobox.get()

        self.new_label = my_label("Цена: " + str(self.price) + "руб.", "Arial 15", "red", 470, 300)


class my_window:
    def __init__(self):

        self.window=Tk()
        self.window.geometry("700x700")
        self.window.title("Автосервис")
        self.window.configure(bg="gray")
        self.window.resizable(width=False, height=False)

        self.__my_canva()
        self.__new_label()
        self.__new_entry()
        self.__new_button()
        self.__new_combobox()


        self.window.mainloop()

    def __my_canva(self):
        self.canva = Canvas(width=650, height=650, bg="lightgray")
        self.canva.pack()
    def __new_label(self):
        self.label_title = my_label("Автосервис", "Arial 30", "lightgray", 235, 50)
        self.label_marka = my_label("Марка Автомобиля:", "Arial 15", "lightgray", 50, 200)
        self.label_model = my_label("Модель Автомобиля:","Arial 15", "lightgray", 50, 250)
        self.label_color = my_label("Цвет Автомобиля:", "Arial 15", "lightgray", 50, 300)
        self.year_Build = my_label("Год Сборки:", "Arial 15", "lightgray", 50, 350)
        self.Number_Car = my_label("Номер Автомобиля:", "Arial 15", "lightgray", 50, 400)

        self.Yslyga_Label = my_label("Наименование услуги:", "Arial 15","lightgray", 465,200)


    def __new_entry(self):
        self.entry_marka = my_entry("Arial 15", 300, 200, 150)
        self.entry_model = my_entry("Arial 15", 300, 250, 150)
        self.entry_color_car = my_entry("Arial 15", 300, 300, 150)
        self.entry_year_build = my_entry("Arial 15", 300, 350, 150)
        self.entry_number_car = my_entry("Arial 15", 300, 400, 150)

    def __new_button(self):
        self.write_btn_button = my_button("Записать", "Arial 20", 400, 550,200)

    def __new_combobox(self):
        self.list = [
            'Замена машины',
            'Технический разбор атомабиля',
            'Технический сбор автомобиля',
            'Уронить машину с подъёмника',
            'Искать поршень сутки',
            'Обсудить политику с мастером',
            'Показать мастеру как надо'
        ]
        self.servis_combobox = my_combobox(self.list, "Arial 13", 470, 250, 200,self)



class my_label:
    def __init__(self, text, font, color, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color

        self.label = Label(text=self.text, font=self.font, bg=color)
        self.label.place(x=self.x, y=self.y)

class my_entry:
    def __init__(self,font,x,y,width):
        self.x = x
        self.y = y
        self.font = font
        self.width = width

        self.entry = Entry(font=self.font)
        self.entry.place(x=self.x, y=self.y, width=self.width)


class my_button:
    def __init__(self, text, font, x, y, width):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.width = width

        self.button = Button(text=self.text, font=self.font, command=self.click)
        self.button.place(x=self.x, y=self.y, width=self.width)




    def click(self):
        pass







new_window=my_window()