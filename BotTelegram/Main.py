import time
import telebot
import random

from pyexpat.errors import messages
from telebot import types

class RSP:
    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova

        self.bot.callback_query_handler(func=lambda call: True)(self.osnova.handle_callback)

    def CalData_RSP(self, call):
        self.bot.answer_callback_query(call.id, text="Вы выбрали игру Камень, ножницы, бумага!")
        self.bot.send_message(call.message.chat.id, "✂📃🗿Давайте сыграем в Камень, ножницы, бумага🗿📃✂")
        time.sleep(1)
        self.Start_RSP(call)

    def Start_RSP(self,call):
        markupRSP = types.InlineKeyboardMarkup()
        markupRSP.add(types.InlineKeyboardButton('🗿', callback_data='Stone'))
        markupRSP.add(types.InlineKeyboardButton('📃', callback_data='Paper'))
        markupRSP.add(types.InlineKeyboardButton('✂', callback_data='Scissors'))

        self.bot.send_message(call.message.chat.id, "Сделайте выбор:", reply_markup=markupRSP)

    def Start_Scissors(self, call):
        WinLose = random.randint(0,1)
        markupRSP2 = types.InlineKeyboardMarkup()
        markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
        markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        if WinLose == 0:
            self.osnova.Money += 10
            self.bot.send_message(call.message.chat.id, "Вы: ✂ Ведущий: 📃")
            self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)
        else:
            self.osnova.Money -= 10
            self.bot.send_message(call.message.chat.id, "Вы: ✂ Ведущий: 🗿")
            self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)

    def Start_Paper(self, call):
        WinLose = random.randint(0,1)
        markupRSP2 = types.InlineKeyboardMarkup()
        markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
        markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        if WinLose == 0:
            self.osnova.Money += 10
            self.bot.send_message(call.message.chat.id, "Вы: 📃 Ведущий: 🗿")
            self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)
        else:
            self.osnova.Money -= 10
            self.bot.send_message(call.message.chat.id, "Вы: 📃 Ведущий: ✂")
            self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)

    def Start_Stone(self, call):
        WinLose = random.randint(0,1)
        markupRSP2 = types.InlineKeyboardMarkup()
        markupRSP2.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
        markupRSP2.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        if WinLose == 0:
            self.osnova.Money += 10
            self.bot.send_message(call.message.chat.id, "Вы: 🗿 Ведущий: ✂")
            self.bot.send_message(call.message.chat.id, f"Вы выйграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)
        else:
            self.osnova.Money -= 10
            self.bot.send_message(call.message.chat.id, "Вы: 🗿 Ведущий: 📃")
            self.bot.send_message(call.message.chat.id, f"Вы проиграли 10 Рублей Баланс:{self.osnova.Money}₽", reply_markup=markupRSP2)




class Roulettee:
    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova

        self.bot.callback_query_handler(func=lambda call: True)(self.osnova.handle_callback)

    def CalData_Roulette(self, call):
        self.bot.answer_callback_query(call.id, text="Вы выбрали игру Рулетка!")
        self.bot.send_message(call.message.chat.id, "🎰Давайте сыграем в Рулетку🎰")
        time.sleep(1)
        self.Start_Roulette(call)

    def Start_Roulette(self, call):
        Rulet_Mas = ["🍒","🍓","🍆","💯"]
        Result = [random.choice(Rulet_Mas) for _ in range(3)]
        result_message = " | ".join(Result)

        markupRoulette = types.InlineKeyboardMarkup()
        markupRoulette.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRoulette'))
        markupRoulette.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        if Result[0] == Result[1] == Result[2]:
            self.osnova.Money += 50
            result_message += f"\nПоздравляем! Вы выиграли 50 Рублей. Ваш баланс: {self.osnova.Money}"
        else:
            self.osnova.Money -= 10
            result_message += f"\nУвы, вы проиграли 10 Рублей. Ваш баланс: {self.osnova.Money}"
        time.sleep(1)
        self.bot.send_message(call.message.chat.id, result_message, reply_markup=markupRoulette)


class Balanse:
    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova

    def ShowBalans(self, call):
        markupBalans = types.InlineKeyboardMarkup()
        markupBalans.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        self.bot.send_message(call.message.chat.id, f"Баланс: {self.osnova.Money}₽", reply_markup=markupBalans)


class Dise_Game:
    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova

        self.bot.callback_query_handler(func=lambda call: True)(self.osnova.handle_callback)


    def CalData_Dice(self, call):
        self.bot.answer_callback_query(call.id, text="Вы выбрали игру Кости!")
        self.bot.send_message(call.message.chat.id, "🎲Давайте сыграем в кости🎲")
        time.sleep(1)
        self.Start_Dice(call)

    def Start_Dice(self,call):
        dice_Player = random.randint(1,6)
        dice_Host = random.randint(1,6)
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.bot.send_message(call.message.chat.id, f"Вы:{dice_Player}, Хозяин стола:{dice_Host}")

        markupDice = types.InlineKeyboardMarkup()
        markupDice.add(types.InlineKeyboardButton('Кинуть снова', callback_data='Restart'))
        markupDice.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        if dice_Player > dice_Host:
            time.sleep(1)
            self.osnova.Money += 10
            self.bot.send_message(call.message.chat.id, f"Ура! Вы выйграли 10 Рублей. Ваш баланс: {self.osnova.Money})", reply_markup=markupDice)

        else:
            time.sleep(1)
            self.osnova.Money -= 10
            self.bot.send_message(call.message.chat.id, f"Увы, вы проиграли 10 Рублей. Ваш баланс: {self.osnova.Money})", reply_markup=markupDice)



class Osnova:
    def __init__(self, token):
        self.Money = 100

        self.bot = telebot.TeleBot(token)
        self.dice_game = Dise_Game(self.bot, self)
        self.balance = Balanse(self.bot, self)
        self.roulete = Roulettee(self.bot, self)
        self.rsp = RSP(self.bot, self)

        self.bot.message_handler(commands=['start'])(self.First_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_callback)

    def First_message(self,messsgae):
        file = "./man.png"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Кости', callback_data='Dice'))
        markup.add(types.InlineKeyboardButton('Баланс', callback_data='Balance'))
        markup.add(types.InlineKeyboardButton('Рулетка', callback_data='Roulette'))
        markup.add(types.InlineKeyboardButton('Камень, ножницы, бумага', callback_data='RSP'))#Rock, scissors, paper

        with open(file, 'rb') as photo:
            self.bot.send_photo(messsgae.chat.id, photo, caption="Добро пожаловать дорогой гость, Чем желаете заняться?",
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
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'Back':
            self.osnoMessage(call)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'Restart':
            self.dice_game.Start_Dice(call)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'Balance':
            self.balance.ShowBalans(call)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == 'Roulette':
            self.roulete.CalData_Roulette(call)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
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

    token = "7965493672:AAFSFYz6jFT5c2TQ7UCUikMKRwiqmSa3Vqc"

    bot = Osnova(token)


    bot.start_polling()