import time
from abc import ABC, abstractmethod
import telebot
import random
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from telebot import types
import multiprocessing
import tkinter as tk
from threading import Thread


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'bot.log',
            maxBytes=1024*1024,
            backupCount=5,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CustomError(Exception):
    def __str__(self):
        return "Карявая ошибка"


class BalanceError(CustomError):
    def __str__(self):
        return "Баланс потеряли!!!"


class GameError(CustomError):
    def __str__(self):
        return "Всё игры накрылись."



class GameBase(ABC):
    def __init__(self, bot, osnova):
        self.bot = bot
        self.osnova = osnova
        self._protected_attr = "Защищенный атрибут"
        logger.info(f"Создан объект игры {self.__class__.__name__}")

    def get_protected_attr(self):
        return self._protected_attr

    @abstractmethod
    def start_game(self, call):
        """Абстрактный метод для запуска игры"""
        pass

    @abstractmethod
    def process_choice(self, call):
        """Абстрактный метод для обработки выбора"""
        pass



class DiceGame(GameBase):
    def __init__(self, bot, osnova):
        super().__init__(bot, osnova)
        self.game_name = "Кости"
        self.internal_name = "Dice"
        logger.info(f"Инициализирована игра {self.game_name}")

    def start_game(self, call):
        try:
            logger.info(f"Запуск {self.game_name} для {call.message.chat.id}")
            self.bot.answer_callback_query(call.id, text=f"Вы выбрали игру {self.game_name}!")
            self.bot.send_message(call.message.chat.id, f"🎲 Давайте сыграем в {self.game_name} 🎲")
            time.sleep(1)
            self.process_choice(call)
        except Exception as e:
            logger.error(f"Ошибка при запуске {self.game_name}: {e}")
            raise GameError(f"Ошибка при запуске {self.game_name}: {e}")

    def process_choice(self, call):
        try:
            roll_dice = lambda: random.randint(1, 6)

            player_roll = roll_dice()
            bot_roll = roll_dice()

            logger.info(f"Кости: игрок {player_roll} vs бот {bot_roll} (user: {call.message.chat.id})")

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartDice'))
            markup.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id
            current_balance = self.osnova.get_user_balance(user_id)

            get_result = lambda pr, br: (
                "win" if pr > br else
                "lose" if pr < br else
                "draw"
            )

            result = get_result(player_roll, bot_roll)
            self.osnova.update_user_stats(user_id, result)

            if result == "win":
                new_balance = current_balance + 10
                self.osnova.set_user_balance(user_id, new_balance)
                message = f"Вы: {player_roll} 🎲 Бот: {bot_roll}\nВы выиграли 10₽! Баланс: {new_balance}₽"
            elif result == "lose":
                new_balance = current_balance - 10
                self.osnova.set_user_balance(user_id, new_balance)
                message = f"Вы: {player_roll} 🎲 Бот: {bot_roll}\nВы проиграли 10₽! Баланс: {new_balance}₽"
            else:
                message = f"Вы: {player_roll} 🎲 Бот: {bot_roll}\nНичья! Баланс не изменился: {current_balance}₽"

            self.bot.send_message(call.message.chat.id, message, reply_markup=markup)

        except BalanceError as e:
            logger.error(f"Ошибка баланса в {self.game_name}: {e}")
        except Exception as e:
            logger.error(f"Ошибка в {self.game_name}: {e}")
            raise GameError(f"Ошибка в {self.game_name}: {e}")

class RSPGame(GameBase):
    def __init__(self, bot, osnova):
        super().__init__(bot, osnova)
        self.game_name = "Камень-Ножницы-Бумага"
        self.internal_name = "RSP"
        self.choices = {
            'Stone': '🗿',
            'Paper': '📃',
            'Scissors': '✂'
        }
        logger.info(f"Инициализирована игра Камень-Ножницы-Бумага")

    def start_game(self, call):
        try:
            logger.info(f"Запуск игры Камень-Ножницы-Бумага для {call.message.chat.id}")
            self.bot.answer_callback_query(call.id, text="Вы выбрали игру Камень, ножницы, бумага!")
            self.bot.send_message(call.message.chat.id, "✂📃🗿Давайте сыграем в Камень, ножницы, бумага🗿📃✂")
            time.sleep(1)
            self._show_choices(call)
        except Exception as e:
            logger.error(f"Ошибка при запуске игры: {e}")
            raise GameError(f"Ошибка при запуске игры: {e}")

    def _show_choices(self, call):
        markup = types.InlineKeyboardMarkup()
        for choice, emoji in self.choices.items():
            markup.add(types.InlineKeyboardButton(emoji, callback_data=choice))
        self.bot.send_message(call.message.chat.id, "Сделайте выбор:", reply_markup=markup)

    def process_choice(self, call):
        try:
            user_choice = call.data
            bot_choice = random.choice(list(self.choices.keys()))

            logger.info(f"Пользователь {call.message.chat.id} выбрал {user_choice}, бот выбрал {bot_choice}")

            determine_winner = lambda uc, bc: (
                "win" if (uc == 'Stone' and bc == 'Scissors') or
                         (uc == 'Scissors' and bc == 'Paper') or
                         (uc == 'Paper' and bc == 'Stone')
                else "lose" if uc != bc else "draw"
            )

            result = determine_winner(user_choice, bot_choice)
            user_id = call.message.chat.id
            self.osnova.update_user_stats(user_id, result)

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRSP'))
            markup.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            user_id = call.message.chat.id
            current_balance = self.osnova.get_user_balance(user_id)

            if result == "win":
                new_balance = current_balance + 10
                self.osnova.set_user_balance(user_id, new_balance)
                message = f"Вы: {self.choices[user_choice]} Бот: {self.choices[bot_choice]}\nВы выиграли 10₽! Баланс: {new_balance}₽"
            elif result == "lose":
                new_balance = current_balance - 10
                self.osnova.set_user_balance(user_id, new_balance)
                message = f"Вы: {self.choices[user_choice]} Бот: {self.choices[bot_choice]}\nВы проиграли 10₽! Баланс: {new_balance}₽"
            else:
                message = f"Вы: {self.choices[user_choice]} Бот: {self.choices[bot_choice]}\nНичья! Баланс не изменился: {current_balance}₽"

            self.bot.send_message(call.message.chat.id, message, reply_markup=markup)

        except BalanceError as e:
            logger.error(f"Ошибка баланса: {e}")
        except Exception as e:
            logger.error(f"Ошибка в игре: {e}")
            raise GameError(f"Ошибка в игре: {e}")


class RouletteGame(GameBase):
    def __init__(self, bot, osnova):
        super().__init__(bot, osnova)
        self.game_name = "Рулетка"
        self.internal_name = "Roulette"
        self.symbols = ["🍒", "🍓", "🍆", "💯"]
        logger.info(f"Инициализирована игра Рулетка")

    def start_game(self, call):
        try:
            logger.info(f"Запуск рулетки для {call.message.chat.id}")
            self.bot.answer_callback_query(call.id, text="Вы выбрали игру Рулетка!")
            self.bot.send_message(call.message.chat.id, "🎰Давайте сыграем в Рулетку🎰")
            time.sleep(1)
            self.process_choice(call)
        except Exception as e:
            logger.error(f"Ошибка при запуске рулетки: {e}")
            raise GameError(f"Ошибка при запуске рулетки: {e}")

    def process_choice(self, call):
        try:
            spin = lambda: [random.choice(self.symbols) for _ in range(3)]
            result = spin()
            result_message = " | ".join(result)

            logger.info(f"Рулетка для {call.message.chat.id}: {result_message}")

            user_id = call.message.chat.id
            current_balance = self.osnova.get_user_balance(user_id)

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кинуть снова', callback_data='RestartRoulette'))
            markup.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

            is_jackpot = lambda res: res[0] == res[1] == res[2]
            result = "win" if is_jackpot(result) else "lose"
            self.osnova.update_user_stats(user_id, result)

            if is_jackpot(result):
                new_balance = current_balance + 150
                self.osnova.set_user_balance(user_id, new_balance)
                self.bot.send_message(call.message.chat.id, "Поздравляем! Вы выиграли 150 Рублей.")
            else:
                new_balance = current_balance - 10
                self.osnova.set_user_balance(user_id, new_balance)
                self.bot.send_message(call.message.chat.id, "Вы проиграли 10 Рублей.")

            time.sleep(1)
            self.bot.send_message(call.message.chat.id, result_message, reply_markup=markup)

        except BalanceError as e:
            logger.error(f"Ошибка баланса: {e}")
        except Exception as e:
            logger.error(f"Ошибка в рулетке: {e}")
            raise GameError(f"Ошибка в рулетке: {e}")


class StatsWindow:
    def __init__(self, osnova):
        self.osnova = osnova
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Статистика игроков")
        self.root.geometry("500x500")
        self.root.configure(bg='#f0f0f0')


        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)

        header = tk.Label(
            main_frame,
            text="Статистика игроков",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        header.pack(pady=(0, 10))

        canvas = tk.Canvas(main_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_refresh = tk.Button(
            main_frame,
            text="Обновить",
            command=self.update_stats,
            bg='#2FBA3B',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        btn_refresh.pack(pady=10)

        self.scrollable_frame = scrollable_frame
        self.update_stats()

    def create_player_card(self, user_id, stats):
        card = tk.Frame(
            self.scrollable_frame,
            bg='white',
            padx=10,
            pady=8,
            relief='groove',
            bd=1
        )

        tk.Label(
            card,
            text=f"Игрок {user_id}",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333333'
        ).pack(anchor='w')


        tk.Label(
            card,
            text=f"Побед: {stats.get('wins', 0)}",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#009E0D'
        ).pack(anchor='w')

        tk.Label(
            card,
            text=f"Поражений: {stats.get('losses', 0)}",
            font=('Arial', 10),
            bg='white',
            fg='#B81919'
        ).pack(anchor='w')

        tk.Label(
            card,
            text=f"Ничьих: {stats.get('draws', 0)}",
            font=('Arial', 10),
            bg='white',
            fg='#B81919'
        ).pack(anchor='w')

        return card

    def update_stats(self):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


        sorted_players = sorted(
            self.osnova.user_stats.items(),
            key=lambda x: x[1].get('wins', 0),
            reverse=True
        )


        for user_id, stats in sorted_players:
            card = self.create_player_card(user_id, stats)
            card.pack(fill='x', pady=5, ipadx=5, ipady=5)


        tk.Label(
            self.scrollable_frame,
            text=f"Всего игроков: {len(self.osnova.user_stats)}",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        ).pack(pady=10)

class Osnova:
    def __init__(self, token):
        self.user_balances = {}
        self.user_stats = {}
        self.stats_window = StatsWindow(self)

        self.root = tk.Tk()
        self.root.withdraw()


        self.stats_window.root.deiconify()

        self.bot = telebot.TeleBot(token)


        self.games = [
            DiceGame(self.bot, self),
            RSPGame(self.bot, self),
            RouletteGame(self.bot, self)
        ]


        self.get_game_buttons = lambda: [
            (game.game_name, game.internal_name) for game in self.games
        ]
        self.get_game_names = lambda: list(self.games.keys())
        self.get_game_stats = lambda: {name: game.get_protected_attr() for name, game in self.games.items()}

        self.bot.message_handler(commands=['start'])(self.first_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_callback)

        logger.info("Бот инициализирован")


    def get_user_balance(self, user_id):
        balance = self.user_balances.get(user_id, 100)
        logger.debug(f"Баланс пользователя {user_id}: {balance}₽")
        return balance

    def set_user_balance(self, user_id, amount):
        self.user_balances[user_id] = amount
        logger.debug(f"Установлен баланс {user_id}: {amount}₽")

    def update_user_stats(self, user_id, result):
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {'wins': 0, 'losses': 0, 'draws': 0}

        if result == "win":
            self.user_stats[user_id]['wins'] += 1
        elif result == "lose":
            self.user_stats[user_id]['losses'] += 1
        else:
            self.user_stats[user_id]['draws'] += 1

    def first_message(self, message):
        try:
            file = "./man.png"

            markup = types.InlineKeyboardMarkup()
            for game_name, callback_data in self.get_game_buttons():
                markup.add(types.InlineKeyboardButton(game_name, callback_data=callback_data))
            markup.add(types.InlineKeyboardButton('Баланс', callback_data='Balance'))

            with open(file, 'rb') as photo:
                self.bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Добро пожаловать! Выберите игру:",
                    reply_markup=markup
                )

            logger.info(f"Показано стартовое сообщение для {message.chat.id}")
        except Exception as e:
            logger.error(f"Ошибка в стартовом сообщении: {e}")

    def handle_callback(self, call):
        try:
            logger.info(f"Обработка callback от {call.message.chat.id}: {call.data}")

            if call.data == 'Back':
                self.show_main_menu(call)
            elif call.data == 'Balance':
                self.show_balance(call)
            else:
                for game in self.games:
                    if call.data == game.internal_name:
                        game.start_game(call)
                        break
                    elif call.data in ['Stone', 'Paper', 'Scissors']:
                        next(g for g in self.games if g.internal_name == 'RSP').process_choice(call)
                        break
                    elif call.data.startswith('Restart'):
                        game_name = call.data.replace('Restart', '')
                        next(g for g in self.games if g.internal_name == game_name).process_choice(call)
                        break
        except Exception as e:
            logger.error(f"Ошибка обработки callback: {e}")
            self.bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

    def show_main_menu(self, call):
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.first_message(call.message)
        logger.info(f"Показано главное меню для {call.message.chat.id}")

    def show_balance(self, call):
        user_id = call.message.chat.id
        current_balance = self.get_user_balance(user_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='Back'))

        self.bot.send_message(
            call.message.chat.id,
            f"Ваш баланс: {current_balance}₽",
            reply_markup=markup
        )
        logger.info(f"Показан баланс для {user_id}")

    def start_polling(self):
        logger.info("Бот запущен и ожидает сообщений")
        self.bot.polling(none_stop=True)


from multiprocessing import Process

if __name__ == "__main__":
    token = ""


    bot = Osnova(token)



    def run_bot():
        bot.start_polling()



    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()


    bot.stats_window.root.mainloop()