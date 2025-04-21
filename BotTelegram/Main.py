import time
from abc import ABC, abstractmethod

import telebot
import random
from pyexpat.errors import messages
from telebot import types


class CustomError(Exception):
    def __str__(self):
        print("Карявая ошибка")

class BalanceError(CustomError):
    def __str__(self):
        print("Баланс потеряли!!!")

class GameError(CustomError):
    def __str__(self):
        print("Всё игры накрылись.")

class ads(ABC):

    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova
        self._protected_attr = "Меня защитили"
        self.bot.callback_query_handler(func=lambda call: True)(self.osnova.handle_callback)

    def get_protected_attr(self):
        return self._protected_attr


class RSP(ads):
    try:
        def __init__(self, bot, osnova):
            super().__init__(bot, osnova)
            self.protected_attr = self.get_protected_attr()

        def CalData_RSP(self, call):
            self.bot.answer_callback_query(call.id, text="Вы выбрали игру Камень, ножницы, бумага!")
            self.bot.send_message(call.message.chat.id, "✂📃🗿Давайте сыграем в Камень, ножницы, бумага🗿📃✂")
            print(f"Я достал его: {self.protected_attr}")
            time.sleep(1)
            self.Start_RSP(call)

    except Exception as e:
        raise GameError(f"Ошибка при запуске игры Камень, ножницы, бумага: {e}")

    finally:
        print("Выполнение игры Камень, ножницы, бумага завершено.")

    def Start_RSP(self, call):
        markupRSP = types.InlineKeyboardMarkup()
        markupRSP.add(types.InlineKeyboardButton('🗿', callback_data='Stone'))
        markupRSP.add(types.InlineKeyboardButton('📃', callback_data='Paper'))
        markupRSP.add(types.InlineKeyboardButton('✂', callback_data='Scissors'))

        self.bot.send_message(call.message.chat.id, "Сделайте выбор:", reply_markup=markupRSP)

    def Start_Scissors(self, call):
        try:
            WinLose = random.randint(0, 1)
            markupRSP2 = types.InlineKeyboardMarkup()
            markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
            markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id

            if WinLose == 0:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance + 10)  # Обновляем баланс
                self.bot.send_message(call.message.chat.id, "Вы: ✂ Ведущий: 📃")
                self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс: {current_balance + 10}₽",
                                  reply_markup=markupRSP2)
            else:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance - 10)  # Обновляем баланс
                self.bot.send_message(call.message.chat.id, "Вы: ✂ Ведущий: 🗿")
                self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс: {current_balance - 10}₽",
                                  reply_markup=markupRSP2)
        except BalanceError as e:
            print(f"Ошибка баланса {e}")

        except Exception as e:
            raise GameError(f"Ошибка в игре Камень, ножницы, бумага: {e}")
        finally:
            print("Завершение игры Камень, ножницы, бумага.")

    def Start_Paper(self, call):
        try:
            WinLose = random.randint(0, 1)
            markupRSP2 = types.InlineKeyboardMarkup()
            markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
            markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id

            if WinLose == 0:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance + 10)
                self.bot.send_message(call.message.chat.id, "Вы: 📃 Ведущий: 🗿")
                self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс: {current_balance + 10}₽",
                                  reply_markup=markupRSP2)
            else:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance + 10)
                self.bot.send_message(call.message.chat.id, "Вы: 📃 Ведущий: ✂")
                self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс: {current_balance - 10}₽",
                                  reply_markup=markupRSP2)
        except BalanceError as e:
            print(f"Ошибка баланса {e}")

        except Exception as e:
            raise GameError(f"Ошибка в игре Камень, ножницы, бумага: {e}")
        finally:
            print("Завершение игры Камень, ножницы, бумага.")

    def Start_Stone(self, call):
        try:
            WinLose = random.randint(0, 1)
            markupRSP2 = types.InlineKeyboardMarkup()
            markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
            markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id

            if WinLose == 0:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance + 10)
                self.bot.send_message(call.message.chat.id, "Вы: 🗿 Ведущий: ✂")
                self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс: {current_balance + 10}₽",
                                      reply_markup=markupRSP2)
            else:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance - 10)
                self.bot.send_message(call.message.chat.id, "Вы: 🗿 Ведущий: 📃")
                self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс: {current_balance - 10}₽",
                                      reply_markup=markupRSP2)
        except BalanceError as e:
            print(f"Ошибка баланса {e}")

        except Exception as e:
            raise GameError(f"Ошибка в игре Камень, ножницы, бумага: {e}")
        finally:
            print("Завершение игры Камень, ножницы, бумага.")


class Roulettee(ads):
    try:
        def CalData_Roulette(self, call):
            self.bot.answer_callback_query(call.id, text="Вы выбрали игру Рулетка!")
            self.bot.send_message(call.message.chat.id, "🎰Давайте сыграем в Рулетку🎰")
            time.sleep(1)
            self.Start_Roulette(call)
            testMass = [[1, 2, 3],
                        [4, 5, 42],
                        [7, 8, 9]
                                ]
            print(testMass[1][2])
    except Exception as e:
        raise GameError(f"Ошибка при запуске игры руетка: {e}")

    finally:
        print("Выполнение игры Рулетка.")

    def Start_Roulette(self, call):
        try:
            Rulet_Mas = ["🍒", "🍓", "🍆", "💯"]

            Result = [random.choice(Rulet_Mas) for _ in range(3)]
            result_message = " | ".join(Result)

            user_id = call.message.chat.id

            markupRoulette = types.InlineKeyboardMarkup()
            markupRoulette.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRoulette'))
            markupRoulette.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            if Result[0] == Result[1] == Result[2]:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance + 150)
                self.bot.send_message(call.message.chat.id, "Поздравляем! Вы выиграли 150 Рублей.")
            else:
                current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
                self.osnova.set_user_balance(user_id, current_balance - 10)
                self.bot.send_message(call.message.chat.id, "Вы проиграли 10 Рублей.")
            time.sleep(1)
            self.bot.send_message(call.message.chat.id, result_message, reply_markup=markupRoulette)
        except BalanceError as e:
            print(f"Ошибка баланса {e}")

        except Exception as e:
            raise GameError(f"Ошибка в игре Рулетка: {e}")
        finally:
            print("Завершение игры Рулетка")


class Balanse(ads):
    try:
        def ShowBalans(self, call):
            markupBalans = types.InlineKeyboardMarkup()
            markupBalans.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id

            current_balance = self.osnova.get_user_balance(user_id)  # Получаем баланс пользователя
            self.bot.send_message(call.message.chat.id, f"Баланс: {current_balance}₽", reply_markup=markupBalans)
    except BalanceError as e:
        print(f"Ошибка баланса {e}")
    finally:
        print("Завершение проверки балнса.")


class Dise_Game(ads):
    try:
        def CalData_Dice(self, call):
            self.bot.answer_callback_query(call.id, text="Вы выбрали игру Кости!")
            self.bot.send_message(call.message.chat.id, "🎲Давайте сыграем в кости🎲")
            time.sleep(1)
            self.Start_Dice(call)
    except Exception as e:
        raise GameError(f"Ошибка при запуске игры Кости: {e}")

    finally:
        print("Выполнение игры Кости.")

    def Start_Dice(self, call):
        try:
            dice_Player = random.randint(1, 6)
            dice_Host = random.randint(1, 6)
            self.bot.send_message(call.message.chat.id, f"Вы:{dice_Player}, Хозяин стола:{dice_Host}")

            markupDice = types.InlineKeyboardMarkup()
            markupDice.add(types.InlineKeyboardButton('Кинуть снова', callback_data='Restart'))
            markupDice.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id

            if dice_Player > dice_Host:
                time.sleep(1)
                current_balance = self.osnova.get_user_balance(user_id)
                self.osnova.set_user_balance(user_id, current_balance + 10)
                self.bot.send_message(call.message.chat.id, f"Ура! Вы выйграли 10 Рублей. Баланс: {current_balance + 10}₽",
                                      reply_markup=markupDice)

            else:
                time.sleep(1)
                current_balance = self.osnova.get_user_balance(user_id)
                self.osnova.set_user_balance(user_id, current_balance - 10)
                self.bot.send_message(call.message.chat.id,f"Увы, вы проиграли 10 Рублей.Баланс: {current_balance - 10}₽",
                                      reply_markup=markupDice)
        except BalanceError as e:
            print(f"Ошибка баланса {e}")

        except Exception as e:
            raise GameError(f"Ошибка в игре Кости: {e}")
        finally:
            print("Завершение игры Кости.")



class Osnova:
    def __init__(self, token):
        self.user_balances = {}
        self.bot = telebot.TeleBot(token)
        self.dice_game = Dise_Game(self.bot, self)
        self.balance = Balanse(self.bot, self)
        self.roulete = Roulettee(self.bot, self)
        self.rsp = RSP(self.bot, self)

        self.bot.message_handler(commands=['start'])(self.First_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_callback)

    def get_user_balance(self, user_id):
        """Возвращает баланс пользователя, если он есть, иначе 100 по умолчанию"""
        return self.user_balances.get(user_id, 100)  # Баланс по умолчанию 100

    def set_user_balance(self, user_id, amount):
        """Устанавливает новый баланс для пользователя"""
        self.user_balances[user_id] = amount

    def First_message(self, message):
        file = "./man.png"


        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Кости', callback_data='Dice'))
        markup.add(types.InlineKeyboardButton('Баланс', callback_data='Balance'))
        markup.add(types.InlineKeyboardButton('Рулетка', callback_data='Roulette'))
        markup.add(types.InlineKeyboardButton('Камень, ножницы, бумага', callback_data='RSP'))  # Rock, scissors, paper

        with open(file, 'rb') as photo:
            self.bot.send_photo(message.chat.id, photo,
                                caption="Добро пожаловать дорогой гость, Чем желаете заняться?",
                                reply_markup=markup)

    def osnoMessage(self, call):
        self.bot.delete_message(call.message.chat.id, call.message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Кости', callback_data='Dice'))
        markup.add(types.InlineKeyboardButton('Баланс', callback_data='Balance'))
        markup.add(types.InlineKeyboardButton('Рулетка', callback_data='Roulette'))
        markup.add(types.InlineKeyboardButton('Камень, ножницы, бумага', callback_data='RSP'))  # Rock, scissors, paper

        self.bot.send_message(call.message.chat.id, "Что дальше?", reply_markup=markup)

    def handle_callback(self, call):
        """Обрабатывает данные из callback_data и передает в класс Dise_Game"""
        if call.data == 'Dice':
            self.dice_game.CalData_Dice(call)
        elif call.data == 'Back':
            self.osnoMessage(call)
        elif call.data == 'Restart':
            self.dice_game.Start_Dice(call)
        elif call.data == 'Balance':
            self.balance.ShowBalans(call)
        elif call.data == 'Roulette':
            self.roulete.CalData_Roulette(call)
        elif call.data == 'RestartRoulette':
            self.roulete.Start_Roulette(call)
        elif call.data == 'RSP':
            self.rsp.CalData_RSP(call)
        elif call.data == 'RestartRSP':
            self.rsp.Start_RSP(call)
        elif call.data == 'Scissors':
            self.rsp.Start_Scissors(call)
        elif call.data == 'Paper':
            self.rsp.Start_Paper(call)
        elif call.data == 'Stone':
            self.rsp.Start_Stone(call)

    def start_polling(self):
        self.bot.polling(none_stop=True)



# Пример использования:
if __name__ == "__main__":
    token = ""

    bot = Osnova(token)

    bot.start_polling()



    class Cell:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f"Cell({self.value})"

    rows = 3
    cols = 4

    grid = [[Cell((i, j)) for j in range(cols)] for i in range(rows)]

    for row in grid:
        print(row)
