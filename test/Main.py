import telebot

bot = telebot.TeleBot("7965493672:AAFSFYz6jFT5c2TQ7UCUikMKRwiqmSa3Vqc")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()