class User:
    def __init__(self, Name, Last_Name, Phone_Number):
        self.Name = Name
        self.Last_Name = Last_Name
        self.Phone_Number = Phone_Number

    def __str__(self):
        return f"Имя пользователя: {self.Name}, Фамилия пользователя: {self.Last_Name}, Номер телефона: {self.Phone_Number}"

class Employee:
    def __init__(self,Name, Last_Name, Profession):
        self.Name = Name
        self.Last_Name = Last_Name
        self.Profession = Profession

    def __str__(self):
        return f"Имя сотрудника: {self.Name}, Фамилия сотрудника: {self.Last_Name}, Профессия сотрудника: {self.Profession}"

class Nearest_cafe:
    def __init__(self, Address, Product_id):
        self.Address = Address
        self.Product_id = Product_id

    def __str__(self):
        return f"Адрес: {self.Address}, Номер заказа: {self.Product_id}"

class Order_Information:
    def __init__(self, Id_Order, Inf_dish, Inf_drink, Inf_stock):
        self.Id_Order = Id_Order
        self.Inf_dish = Inf_dish
        self.Inf_drink = Inf_drink
        self.Inf_stock = Inf_stock

    def __str__(self):
        return f"Номер заказа: {self.Id_Order}, ID Блюда: {self.Inf_dish}, ID Напитка: {self.Inf_drink}, Номер акции:{self.Inf_stock}"

class Courier:
    def __init__(self,Name, Phone_Number, Last_Name):
        self.Name = Name
        self.Phone_Number = Phone_Number
        self.Last_Name = Last_Name

    def __str__(self):
        return f"Имя курьера: {self.Name}, Фамилия курьера: {self.Last_Name}, НОмер телефона курьера: {self.Phone_Number}"

user = User("Илюша", "Ринг", "88005553535")
emp = Employee("Егор", "Дрынов", "Менеджер, Программист, Дизайнер, Аналитик, Маркетолог")
prod = Nearest_cafe("г. Барнаул, проспект Ленина, д. 46", "01")
ord = Order_Information("12","01","03","054738210")
courier = Courier("Артур", "88005553535", "Пирожков")

print(f"{user}\n{emp}\n{prod}\n{ord}\n{courier}")