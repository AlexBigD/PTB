import telebot
import main
from telebot import types
from decimal import Decimal

bot = telebot.TeleBot(main.token_test)

@bot.message_handler(commands=['start'])
def handle_command(message):
    markup_inline = types.InlineKeyboardMarkup()
    bt_1 = types.InlineKeyboardButton(text='Курсы Валют', callback_data='currency')
    bt_2 = types.InlineKeyboardButton(text='Купить/Продать', callback_data='op')
    markup_inline.add(bt_1, bt_2)
    bot.send_message(message.chat.id, 'Выбирай стул', reply_markup=markup_inline)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'старт' or message.text.lower() == 'привет' or message.text.lower() == "start":
        return handle_command(message)

def hello(message):
    main.sum = Decimal(message.text)
    data = main.stat()

    for key,value in data.items():
        if key == main.oper_name:
            if main.name_currency == "cny":
                main.currency = Decimal(value[main.name_currency].replace(",", '.')) / 10
            else:
                main.currency = Decimal(value[main.name_currency].replace(",", '.'))
            if main.oper_name == 'sell':
                sum_custom = main.sum * (main.currency)
                mes = "ПРОДАЖА: Операция на сумму {} {} по курсу {} за {} равна {} Р.".format(main.sum,
                                                                                          main.name_currency.upper(),
                                                                                          main.currency,
                                                                                          main.name_currency.upper(),
                                                                                          sum_custom)
                bot.send_message(message.chat.id, mes)
            elif main.oper_name == 'buy':
                sum_custom = main.sum / (main.currency)
                mes = "ПОКУПКА: Операция на сумму {} Р по курсу {} за {} равна {} {}.".format(main.sum, main.currency,
                                                                                              main.name_currency.upper(),
                                                                                              sum_custom,
                                                                                              main.name_currency.upper())
                bot.send_message(message.chat.id, mes)


@bot.callback_query_handler(lambda a: True)
def start_answer(a):
    if a.data == 'currency':
        bot.send_message(a.message.chat.id, main.edit_pars())

    if a.data == 'op':
        markup_inline = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='Купить', callback_data='buy')
        bt_2 = types.InlineKeyboardButton(text='Продать', callback_data='sell')
        markup_inline.add(bt_1, bt_2)
        bot.send_message(a.message.chat.id, 'Выбирай стул', reply_markup=markup_inline)

    if a.data == 'buy' or a.data == 'sell' :
        main.oper_name = a.data
        markup_inline = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='USD', callback_data='usd')
        bt_2 = types.InlineKeyboardButton(text='EUR', callback_data='eur')
        bt_3 = types.InlineKeyboardButton(text='CNY', callback_data='cny')
        markup_inline.add(bt_1, bt_2, bt_3)
        bot.send_message(a.message.chat.id, 'Выбирай стул', reply_markup=markup_inline)

    if a.data == 'usd' or a.data == 'eur' or a.data == 'cny':
        main.name_currency = a.data
        sent = bot.send_message(a.message.chat.id, 'Введите сумму в числовом эквиваленте без знаков')
        bot.register_next_step_handler(sent,hello)

bot.polling(none_stop=True)