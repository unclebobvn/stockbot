import telegram

class TelegramBot:
    
    def send(msg):
        """
        Send a message to a telegram user or group specified on chatId
        chat_id must be a number!
        """
        my_token = ''
        chat_id = ''

        bot = telegram.Bot(token=my_token)
        bot.sendMessage(chat_id=chat_id, text=msg)
