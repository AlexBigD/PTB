from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import main
updater = Updater(main.token_test, use_context=True)

#########################################
def start(update,context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, "Выбирай стул", reply_markup=main_menu_keyboard())

def first_sub_menu(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, main.edit_pars())

#def second_sub_menu(update, context):

#########################################
def main_menu_keyboard():
    markup_inline = [[InlineKeyboardButton(text='Курсы Валют', callback_data='currency')],
                      [InlineKeyboardButton(text='Купить/Продать', callback_data='op')]]
    return InlineKeyboardMarkup(markup_inline)

#def first_sub_menu():

#########################################
updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CallbackQueryHandler(first_sub_menu,pattern="currency"))


updater.start_polling()
updater.idle()