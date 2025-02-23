from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

import sqlite3


list = []

file = open("BaseCarServis.db.sql", "r", encoding="utf-8")
build_db = file.read()
file.close()

connector = sqlite3.connect('BaseCarServis.db')

cursor = connector.cursor()

cursor.executescript(build_db)

sql_services = cursor.execute("Select * from Services")

for row in sql_services:
    list.append(row[1])

connector.commit()
cursor.close()
connector.close()


class my_combobox:
    global price, servis
    price = 0
    servis = ""

    def __init__(self, list, font, x, y, width, window):
        self.x = x
        self.y = y
        self.list = list
        self.font = font
        self.width = width

        self.combobox = Combobox(values=self.list, font=self.font, state="readonly")
        self.combobox.place(x=self.x, y=self.y, width=self.width)
        self.combobox.bind('<<ComboboxSelected>>', lambda event: self.select())

    def select(self):
        global price, servis

        servis = self.combobox.get()

        connector = sqlite3.connect("BaseCarServis.db")
        cursor = connector.cursor()
        sql_services = cursor.execute(f"Select * from Services where name ='{servis}'")

        for row in sql_services:
            price = row[2]

        connector.commit()
        cursor.close()
        connector.close()

        self.new_label = my_label("Цена: " + str(price) + "руб.", "Arial 15", "#011b4c", 470, 300, fg="white")


class my_window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("700x700")
        self.window.title("Автосервис")

        self.window.resizable(width=False, height=False)

        background_image = PhotoImage(file="Fone.png")
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #img = PhotoImage(file='mark_auto.png')
        #Label(self.window,image=img).place(x=50,y=150)


        #self.__my_canva()
        self.__new_label()
        self.__new_entry()
        self.new_button()
        self.__new_combobox()

        self.window.mainloop()

    def __my_canva(self):
        self.canva = Canvas(width=650, height=650, bg="black")
        self.canva.pack()

    def __new_label(self):
        self.label_marka = my_label("Марка Автомобиля:", "Tahoma 15 bold", "#011b4c", 50, 150, fg="white")
        self.label_model = my_label("Модель Автомобиля:", "Tahoma 15 bold", "#011b4c", 50, 200, fg="white")
        self.label_color = my_label("Цвет Автомобиля:", "Tahoma 15 bold", "#011b4c", 50, 250, fg="white")
        self.year_Build = my_label("Год Сборки:", "Tahoma 15 bold", "#011b4c", 50, 300, fg="white")
        self.Number_Car = my_label("Номер Автомобиля:", "Tahoma 15 bold", "#011b4c", 50, 350, fg="white")
        self.Text_you = my_label("Данные для связи с вами:", "Tahoma 20 bold", "#011b4c", 180, 400, fg="white")

        self.Yslyga_Label = my_label("Наименование услуги:", "Tahoma 15 bold", "#011b4c", 465, 200, fg="white")

        self.Surname = my_label("Фамилия:", "Tahoma 15 bold", "#011b4c", 70, 500, fg="white")
        self.Name = my_label("Имя:", "Tahoma 15 bold", "#011b4c", 70, 450, fg="white")
        self.phone_number = my_label("Номер телефона:", "Tahoma 15 bold", "#011b4c", 70, 550, fg="white")


    def __new_entry(self):
        self.entry_marka = my_entry("Tahoma 15 bold", 300, 150, 150, fg="black")
        self.entry_model = my_entry("Tahoma 15 bold", 300, 200, 150, fg="black")
        self.entry_color_car = my_entry("Tahoma 15 bold", 300, 250, 150, fg="black")
        self.entry_year_build = my_entry("Tahoma 15 bold", 300, 300, 150, fg="black")
        self.entry_number_car = my_entry("Tahoma 15 bold", 300, 350, 150, fg="black")

        self.entry_surname = my_entry("Tahoma 15 bold", 300, 500, 150, fg="black")
        self.entry_name = my_entry("Tahoma 15 bold", 300, 450, 150, fg="black")
        self.entry_number_phone = my_entry("Tahoma 15 bold", 300, 550, 150, fg="black")

    def new_button(self):
        self.write_btn_button = my_button("Записать", "Tahoma 20 bold", 465, 600, 200, self)

    def __new_combobox(self):
        global list
        self.servis = my_combobox(list, "Tahoma 13 bold", 470, 250, 200, self)


class my_label:
    def __init__(self, text, font, color, x, y, fg):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.fg = fg

        self.label = Label(text=self.text, font=self.font, bg=color, fg=fg)
        self.label.place(x=self.x, y=self.y)


class my_entry:
    def __init__(self, font, x, y, width, fg):
        self.x = x
        self.y = y
        self.font = font
        self.width = width
        self.fg = fg

        self.value = StringVar()

        self.entry = Entry(textvariable=self.value, font=self.font, fg=fg)
        self.entry.place(x=self.x, y=self.y, width=self.width)


class my_button:
    def __init__(self, text, font, x, y, width, window):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.width = width
        self.window = window


        self.button = Button(text=self.text, font=self.font, command=self.click, bg="#3e81f4",fg="white")
        self.button.place(x=self.x, y=self.y, width=self.width)

    def check_entry(self):
        global price, servis
        if not self.value_marka or \
                not self.value_model \
                or not self.value_color \
                or not self.value_year_build \
                or not self.value_number \
                or not servis \
                or not self.value_surname \
                or not self.value_name \
                or not self.value_number_phone:
            return False
        else:
            return True

    def click(self):
        self.value_marka = self.window.entry_marka.value.get()
        self.value_model = self.window.entry_model.value.get()
        self.value_color = self.window.entry_color_car.value.get()
        self.value_year_build = self.window.entry_year_build.value.get()
        self.value_number = self.window.entry_number_car.value.get()

        self.value_surname = self.window.entry_surname.value.get()
        self.value_name = self.window.entry_name.value.get()
        self.value_number_phone = self.window.entry_number_phone.value.get()

        if self.check_entry():
            messagebox.showinfo("Сообщение", "Ваша заявка в обработке")

            connector = sqlite3.connect("BaseCarServis.db")
            cursor = connector.cursor()

            cursor.execute(f"INSERT INTO auto(model, marka, Color, Year_building, Number)"
                           f"VALUES ('{self.value_model}','{self.value_marka}','{self.value_color}',"
                           f"'{self.value_year_build}','{self.value_number}')")

            sql = cursor.execute(f"select max(id) from auto")
            for row in sql:
                id_auto = row[0]

            cursor.execute(f"INSERT into customer (surname, name, num_phone, id_auto)"
                           f"VALUES('{self.value_surname}','{self.value_name}','{self.value_number_phone}','{id_auto}')")

            sql = cursor.execute(f"Select max(id) from customer")
            for row in sql:
                id_customer = row[0]

            global servis
            sql = cursor.execute(f"Select id from Services WHERE name = '{servis}'")
            for row in sql:
                id_services = row[0]
            cursor.execute(f"INSERT into zakaz (id_custemer, id_services)"
                           f"VALUES ('{id_customer}','{id_services}')")
            connector.commit()
            cursor.close()
            connector.close()

            self.print_file()

        else:
            messagebox.showerror("Ошибка", "Не все поля были заполнены")

    def print_file(self):
        global servis, price
        connector = sqlite3.connect("BaseCarServis.db")
        cursor = connector.cursor()
        sql_services = cursor.execute("SELECT C_A.surname, C_A.name, C_A.model, C_A.marka, S.name, S.price"
                                      " FROM zakaz as Z"
                                      " INNER JOIN Services as S on Z.id_services = S.id"
                                      " INNER JOIN (SELECT * FROM customer as C INNER JOIN auto as A on C.id_auto=A.id)"
                                      " as C_A on Z.id_custemer = C_A.id")
        for row in sql_services:
            txt_surname = row[0]
            txt_name = row[1]
            txt_model = row[2]
            txt_marka = row[3]
            txt_servis = row[4]
            txt_price = row[5]

            file = open('new_Otchet.txt', 'a', encoding="utf8")
            file.write("НОВЫЙ ЗАКАЗ" + "\n")
            file.write("Фамилия, имя: " + txt_surname + " " + txt_name + "\n")
            file.write("Данные машины: " + txt_model + " " + txt_marka + "\n")
            file.write("Услуга: " + txt_servis + " Стоимоть: " + str(txt_price) + " руб. " + "\n")
            file.write(" -----------------------" + "\n")
            file.close()

        connector.commit()
        cursor.close()
        connector.close()


new_window = my_window()
