import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду бота в следующем формате:\n<имя исходной валюты> \
<имя валюты, в которую перевести> \
<количество конвертируемой исходной валюты>\nУвидеть список всех достуных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(command=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def handle_convert(message: telebot.types.Message):
    try:
        check_val = message.text.split(' ')

        if len(check_val) != 3:
            if len(check_val) < 3:
                raise APIException('Слишком мало параметров, введите 3 значения!')
            elif len(check_val) > 3:
                raise APIException('Слишком много параметров, введите 3 значения!')

        curr_in, curr_out, amount = check_val
        curr_new = CryptoConverter.get_price(curr_in, curr_out, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {curr_in} в {curr_out} - {curr_new}'
        bot.send_message(message.chat.id, text)

bot.polling()
