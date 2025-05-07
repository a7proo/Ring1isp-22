import time
from abc import ABC, abstractmethod
import telebot
import random
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from telebot import types


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


class Osnova:
    def __init__(self, token):
        self.user_balances = {}
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


if __name__ == "__main__":
    token = ""
    bot = Osnova(token)
    bot.start_polling()