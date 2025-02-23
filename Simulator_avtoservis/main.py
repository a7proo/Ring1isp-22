import random
import sqlite3
import subprocess
import sys
import time
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview


class my_button:
    def __init__(self, text, font, x, y, width, window, command):
        self.window = window
        self.command = command
        self.visible = False
        self.button = Button(text=text, font=font, activebackground="blue", activeforeground="white")
        self.button.place(x=x, y=y, width=width)
        self.button.bind('<Button-1>', lambda event: self.click(self.command))

    def click(self, command):
        if command == "enter":
            self.enter()
        elif command == "show":
            self.show()
        elif command == "lider":
            self.lider_table()
        elif command == "back":
            self.back()
        elif command == "new_user":
            self.new_user()
        elif command == "del_user":
            self.del_user()
        elif command == "update_user":
            self.update_user()

    def new_user(self):
        self.user_login = simpledialog.askstring("Добавление пользователя", "Введите логин нового пользователя:")
        self.user_password = simpledialog.askstring("Добавление пользователя", "Введите пароль новго пользователя:")
        self.db = connect_db('avtoservis_users.db')

        self.sql = self.db.select_sql(
            f"INSERT INTO users (login, password) VALUES ( '{self.user_login}', '{self.user_password}');")
        self.db.close_db()

        messagebox.showinfo("Добавление пользователя", "Пользователь добавлен!")

    def del_user(self):
        self.user_login = simpledialog.askstring("Удаление пользователя", "Введите логин пользователя:")
        result = messagebox.askyesno("Подтвержение операции", "Вы уверены?")
        if result:
            self.db = connect_db('avtoservis_users.db')
            self.sql = self.db.select_sql(f"DELETE from users WHERE login='{self.user_login}'")
            self.db.close_db()
            messagebox.showinfo("Удаление пользователя", "Пользователь удален!")

    def update_user(self):
        self.user_login = simpledialog.askstring("Удаление пользователя", "Введите логин пользователя:")
        self.user_password = simpledialog.askstring("Удаление пользователя", "Введите новый пароль пользователя:")
        result = messagebox.askyesno("Подтвержение операции", "Вы уверены?")
        if result:
            self.db = connect_db('avtoservis_users.db')
            self.sql = self.db.select_sql(
                f"UPDATE users SET password = '{self.user_password}' WHERE login='{self.user_login}' ")
            self.db.close_db()
            messagebox.showinfo("Изменение пользователя", "Пользователю " + self.user_login + " задан новый пароль!")

    def back(self):
        self.window.destroy_main_window()
        self.window.start_window = my_window("ВХОД", "400x400")
        self.window.start_window.widget_for_start_window()
        self.window.start_window.visible_window()

    def lider_table(self):
        if not self.visible:
            self.window.show_table_lider()
            self.visible = True
        else:
            self.window.delete_table_lider()
            self.visible = False

    def show(self):
        if self.window.entry_password_entry.cget('show') == '':
            self.window.entry_password_entry.config(show='*')
        else:
            self.window.entry_password_entry.config(show='')

    def enter(self):
        global id_user
        self.admin = False
        self.value_login = self.window.entry_login.value.get()
        self.value_pass = self.window.entry_password.value.get()

        self.db = connect_db('avtoservis_users.db')

        self.sql = self.db.select_sql("SELECT * from users")
        for row in self.sql:
            self.db_id = row[0]
            self.db_login = row[1]
            self.db_pass = row[2]

            if self.value_login == self.db_login and self.value_pass == self.db_pass:
                self.open = True
                id_user = self.db_id
                if self.value_login == "admin":
                    self.admin = True
                break
            else:
                self.open = False

        self.db.close_db()
        if self.open and not self.admin:
            messagebox.showinfo("Внимание!", "Доступ разрешен")
            self.window.destroy_main_window()
            self.work_window = my_window("Master car service", "800x800")
            self.work_window.canva_for_work_window()
            self.work_window.widget_for_work_window()
            self.work_window.visible_window()
        elif self.open and self.admin:
            messagebox.showinfo("Внимание!", "Доступ разрешен")
            self.window.destroy_main_window()
            self.work_window = my_window("панель управления", "400x300")
            self.work_window.widget_for_admin_window()
            self.work_window.visible_window()
        else:
            messagebox.showerror("Внимание!", "Не верный логин или пароль")


class my_entry:
    def __init__(self, font, x, y, width, mask):
        self.value = StringVar()
        if mask == True:
            show = "*"
        else:
            show = ""
        self.entry = Entry(textvariable=self.value, font=font, show=show)
        self.entry.place(x=x, y=y, width=width)


class my_label:
    def __init__(self, text, font, bg, x, y):
        self.label = Label(text=text, font=font, bg=bg)
        self.label.place(x=x, y=y)


class connect_db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def select_sql(self, sql_txt):
        self.sql_txt = sql_txt
        return self.cursor.execute(self.sql_txt)

    def insert_sql(self, sql_txt):
        self.insert_txt = sql_txt
        return self.cursor.execute(self.insert_txt)

    def close_db(self):
        self.connector.commit()
        self.cursor.close()
        self.connector.close()


class my_check_button:
    def __init__(self, text, font, bg, x, y):
        self.check_button = Checkbutton(text=text, font=font, bg=bg, state="disabled", disabledforeground="black")
        self.check_button.place(x=x, y=y)

    def set_state(self):
        self.check_button.configure(disabledforeground="green")
        self.check_button.select()


class my_window:
    def __init__(self, title, size):
        self.window = Tk()
        self.window.geometry(size)
        self.window.resizable(False, False)
        self.window.title(title)
        self.window.configure(bg="lightgray")
        self.visible = False

        self.kol_avto = 0

        self.servis_finish = False
        self.servis1_crossed = False
        self.servis2_crossed = False
        self.servis3_crossed = False
        self.servis4_crossed = False

        file_menu = Menu(tearoff=0)
        file_menu.add_command(label="список лидеров", command=self.lider_table)
        file_menu.add_command(label="о программе", command=self.about)
        file_menu.add_command(label="выход", command=self.exit)
        main_menu = Menu()
        main_menu.add_cascade(label="Файл", menu=file_menu)
        self.window.config(menu=main_menu)



    def about(self):
        file_path = "about.txt"
        subprocess.run(["start", "notepad", file_path], shell=True)

    def exit(self):
        sys.exit()

    def lider_table(self):
        if not self.visible:
            self.show_table_lider()
            self.visible = True
        else:
            self.delete_table_lider()
            self.visible = False

    def update_timer(self):
        global now_time
        now_time = int(time.time() - self.start_time)
        self.canva.itemconfigure(self.txt_timer, text="Время: " + str(now_time) + " сек.")
        if not self.servis_finish:
            self.window.after(1000, self.update_timer)

    def visible_window(self):
        self.window.mainloop()

    def destroy_main_window(self):
        self.window.destroy()

    def widget_for_start_window(self):
        self.label_title = my_label("ВХОД", "Arial 20 bold", "lightgray", 160, 80)
        self.label_login = my_label("Логин:", "Arial 15", "lightgray", 55, 150)
        self.label_password = my_label("Пароль:", "Arial 15", "lightgray", 39, 200)

        self.entry_login = my_entry("Arial 15", 130, 150, 150, False)
        self.entry_password = my_entry("Arial 15", 130, 200, 150, True)

        self.entry_password_entry = self.entry_password.entry

        self.enter_btn = my_button("ВХОД", "Arial 15", 150, 300, 100, self, "enter")
        self.show_btn = my_button("⭕", "Arial 12", 290, 198, 32, self, "show")

        self.lider_btn = my_button("список лидеров", "Arial 10", 100, 350, 200, self, "lider")
        self.create_table_lider()

    def canva_for_work_window(self):
        self.canva = Canvas(width=800, height=800, bg='lightgray')
        self.canva.pack()

        self.txt_timer = self.canva.create_text(80, 50, text="Время: 0 сек.", font="Arial 15")

        self.work_place = self.canva.create_rectangle(500, 100, 650, 300, width=3, dash=(1, 1))
        self.start_place = self.canva.create_rectangle(500, 590, 650, 790, width=3, dash=(1, 1))

        self.txt_master = self.canva.create_text(600, 320, font="Arial 15", text="мастерская")
        self.txt_garage = self.canva.create_text(600, 570, font="Arial 15", text="гараж")

        self.txt_kol_avto = self.canva.create_text(150, 570, font="Arial 15",
                                                   text="Количество машин: " + str(self.kol_avto))
        self.txt_start = self.canva.create_text(400, 450, font="Arial 20 bold", text="НАЖМИТЕ ДЛЯ НАЧАЛА РАБОТЫ",
                                                fill="black", activefill="red")

        self.canva.tag_bind(self.txt_start, '<Button-1>', lambda event, tag=self.txt_start: self.start_work())

    def start_work(self):
        self.canva.delete(self.txt_start)

        self.start_time = time.time()  # Записываем текущее время при начале работы
        self.update_timer()

        self.car_list = [
            PhotoImage(file="car1.png"),
            PhotoImage(file="car2.png"),
            PhotoImage(file="car3.png"),
            PhotoImage(file="car4.png"),
            PhotoImage(file="car5.png"),
            PhotoImage(file="car6.png"),
            PhotoImage(file="car7.png"),
            PhotoImage(file="car8.png")
        ]
        self.random_car = random.choice(self.car_list)
        self.servis1_img = PhotoImage(file="s1.png")
        self.servis2_img = PhotoImage(file="s2.png")
        self.servis3_img = PhotoImage(file="s3.png")
        self.servis4_img = PhotoImage(file="s4.png")

        self.car = self.canva.create_image(580, 690, image=self.random_car)

        self.canva.focus_set()
        self.canva.bind('<KeyPress>', self.move_car)

    def move_car(self, event):
        coords = self.canva.coords(self.car)
        if event.keysym == 'Left':
            if coords[0] >= 500:
                self.canva.move(self.car, -20, 0)
            else:
                self.canva.move(self.car, 0, 0)

        elif event.keysym == 'Right':
            if coords[0] <= 720:
                self.canva.move(self.car, 20, 0)
            else:
                self.canva.move(self.car, 0, 0)

        elif event.keysym == 'Up':
            if coords[1] >= 160:
                self.canva.move(self.car, 0, -20)
            else:
                self.canva.move(self.car, 0, 0)

        elif event.keysym == 'Down':
            if coords[1] <= 700:
                self.canva.move(self.car, 0, 20)
            else:
                self.canva.move(self.car, 0, 0)

        if 580 <= coords[0] <= 610 and 190 <= coords[1] <= 230 and self.servis_finish == False:
            messagebox.showinfo("Готово!", "Машина на месте!")
            self.step1.set_state()
            self.create_servis()
            self.canva.unbind('<KeyPress>')
        elif 560 <= coords[0] <= 610 and 670 <= coords[1] <= 750 and self.servis_finish == True:
            messagebox.showinfo("Готово!", "Ремонт окончен!")
            self.step6.set_state()
            self.canva.unbind('<KeyPress>')

            self.kol_avto += 1
            self.canva.itemconfigure(self.txt_kol_avto, text="Количество машин: " + str(self.kol_avto))

            # добавление в базу данных
            self.db = connect_db('avtoservis_users.db')
            self.db.insert_sql(
                f"INSERT INTO work_user (id_user, count_avto, sec) VALUES ('{id_user}', '{self.kol_avto}', '{now_time}');")
            self.db.close_db()

            self.otvet = messagebox.askyesno("Далее", "Готовы к следующей машине?")
            if self.otvet:
                self.reset_game()
            else:
                messagebox.showwarning("Окончание", "Рабочий день окончен! всего машин: " + str(self.kol_avto))
                self.destroy_main_window()

    def reset_game(self):
        self.servis_finish = False
        self.servis1_crossed = False
        self.servis2_crossed = False
        self.servis3_crossed = False
        self.servis4_crossed = False

        self.canva.destroy()
        self.canva_for_work_window()
        self.widget_for_work_window()

    def create_servis(self):
        self.servis1 = self.canva.create_image(400, 100, image=self.servis1_img)
        self.servis2 = self.canva.create_image(400, 250, image=self.servis2_img)
        self.servis3 = self.canva.create_image(750, 100, image=self.servis3_img)
        self.servis4 = self.canva.create_image(750, 250, image=self.servis4_img)

        self.canva.tag_bind(self.servis1, '<Button-1>', lambda event, tag=self.servis1: self.cross_servis(tag))
        self.canva.tag_bind(self.servis2, '<Button-1>', lambda event, tag=self.servis2: self.cross_servis(tag))
        self.canva.tag_bind(self.servis3, '<Button-1>', lambda event, tag=self.servis3: self.cross_servis(tag))
        self.canva.tag_bind(self.servis4, '<Button-1>', lambda event, tag=self.servis4: self.cross_servis(tag))

    def cross_servis(self, tag):
        if tag == self.servis1 and not self.servis1_crossed:
            messagebox.showinfo("Работа проведена!", "Был проведен полный осмотр!")
            self.canva.create_line(350, 50, 450, 150, fill='red', width=5)
            self.servis1_crossed = True
            self.step2.set_state()

        elif tag == self.servis2 and not self.servis2_crossed:
            messagebox.showinfo("Работа проведена!", "Машина помыта!")
            self.canva.create_line(350, 200, 450, 300, fill='red', width=5)
            self.servis2_crossed = True
            self.step3.set_state()

        elif tag == self.servis3 and not self.servis3_crossed:
            messagebox.showinfo("Работа проведена!", "Был проведен ремонт!")
            self.canva.create_line(700, 50, 800, 150, fill='red', width=5)
            self.servis3_crossed = True
            self.step4.set_state()

        elif tag == self.servis4 and not self.servis4_crossed:
            messagebox.showinfo("Работа проведена!", "Сигнализация установлена!")
            self.canva.create_line(700, 200, 800, 300, fill='red', width=5)
            self.servis4_crossed = True
            self.step5.set_state()

        if self.servis4_crossed and self.servis3_crossed and self.servis2_crossed and self.servis1_crossed:
            self.servis_finish = True
            self.canva.focus_set()
            self.canva.bind('<KeyPress>', self.move_car)

    def widget_for_work_window(self):
        self.label_title = my_label("Сервисное обслуживание автомобиля", "Arial 20 bold", "lightgray", 150, 10)

        self.step1 = my_check_button("Доставить машину в сервис", "Arial 15", "lightgray", 30, 100)
        self.step2 = my_check_button("Провести полный осмотр", "Arial 15", "lightgray", 30, 150)
        self.step3 = my_check_button("Помыть машину", "Arial 15", "lightgray", 30, 200)
        self.step4 = my_check_button("Провести ремонт", "Arial 15", "lightgray", 30, 250)
        self.step5 = my_check_button("Установить сигнализацию", "Arial 15", "lightgray", 30, 300)
        self.step6 = my_check_button("Доставить машину в гараж", "Arial 15", "lightgray", 30, 350)

        self.info = my_label("Что бы доставить машину" + "\n" + "из гаража в сервис и обратно" + "\n" +
                             " воспользуйтесь стрелками на клавиатуре", "Arial 15", "lightgray", 10, 650)

        self.back_btn = my_button("назад", "Arial 10", 10, 750, 50, self, "back")

    def widget_for_admin_window(self):
        self.label_title = my_label("Панель управления", "Arial 20 bold", "lightgray", 60, 10)

        self.enter_btn = my_button("Добавить пользователя", "Arial 15", 60, 100, 300, self, "new_user")
        self.enter_btn = my_button("Удалить пользователя", "Arial 15", 60, 150, 300, self, "del_user")
        self.enter_btn = my_button("Изменить пароль пользователю", "Arial 15", 60, 200, 300, self, "update_user")

        self.back_btn = my_button("назад", "Arial 10", 10, 250, 50, self, "back")

    def create_table_lider(self):
        # создаем таблицу
        self.tree = Treeview(columns=["user", "min"], show="headings")

        # определяем заголовки
        self.tree.heading("user", text="пользователь")
        self.tree.heading("min", text="рекорд, сек.")

        # настраиваем столбцы
        self.tree.column("user", width=100, anchor="c")
        self.tree.column("min", width=100, anchor="c")

        # подключение к базе данных
        self.db = connect_db('avtoservis_users.db')
        self.sql = self.db.select_sql("SELECT U.login, MIN(W.sec) FROM users U INNER JOIN "
                                      "work_user W ON U.id = W.id_user GROUP BY U.login ;")
        for row in self.sql:
            self.user = row[0]
            self.min_time = row[1]
            self.tree.insert("", END, values=[self.user, self.min_time])

        self.db.close_db()

    def show_table_lider(self):
        self.tree.pack()

    def delete_table_lider(self):
        self.tree.pack_forget()


start_window = my_window("ВХОД", "400x400")
start_window.widget_for_start_window()
start_window.visible_window()
