#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we choose to stop or win the game.
Usage:
Game based in a Telegram conversation.
Send /start to initiate the conversation.
"""

import logging, random

from config.auth import *

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PREGUNTA, COMPRUEBO = range(2)

reply_keyboard = [['Si', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# Función que valida el número generado o introducido
def validNumber(number):
    print(number)
    notValid = 0
    for i in range(len(number)):
        for j in range(len(number)):
            if i != j and str(number)[i] == str(number)[j]:
                notValid = 1
    if len(number) != 4:
        notValid = 1
    return notValid


# Genera el número secreto aleatoriamente
def numberGeneration():
    notValid = 1
    while notValid == 1:
        number = random.randrange(1023,9876)
        notValid = validNumber(str(number))
    return number


def juego(number):      
        # Borro los valores de heridos y muertos
        muertos = 0
        heridos = 0
        # Comienza un bucle for para calcular los heridos y muertos
        for index,dig in enumerate(str(number)):
            if dig == str(secretNumber)[index]:
                muertos +=1
            elif dig in str(secretNumber):
                heridos +=1
        return muertos, heridos


def start(update, context):
    secretNumber = numberGeneration()
    update.message.reply_text(
        'Hola! Soy el Profesor Bot.\n'
        'Te planteo un reto. Deberás adivinar un número de 4 cifras cuyos digitos no se repitan. '
        'Para ayudarte en cada intento te indicaré el número de muertos y de heridos.\n'
        'Un muerto indica que uno de los dígitos es correcto y la posición es correcta también.\n'
        'Un herido indica que uno de los dígitos es correcto pero la posición no.\n'
        '¿Aceptas el reto?',
        reply_markup=markup)
    return PREGUNTA


def pregunta(update, context):
    update.message.reply_text('¿Cuál crees que es el número?')
    return COMPRUEBO

def compruebo(update,context):
    myNumber = update.message.text
    notValid = validNumber(str(myNumber))
    print(notValid)
    if notValid == 1:
        update.message.reply_text(
            'El número no cumple las normas\n'
            '¿Quieres volver a intentarlo?',
            reply_markup=markup)
        return PREGUNTA

    else:
        muertos, heridos = juego(myNumber)
        # Aumento los intentos
        # intentos +=1
        if muertos == 4:
            update.message.reply_text(
                '¡Enhorabuena!\n'
                'Has acertado el número\n')
            return ConversationHandler.END    
        
        else:
            update.message.reply_text(
                'No has acertado el número\n'
                'El número de muertos es {} y el número de heridos es: {}.\n' 
                '¿Quieres volver a intentarlo?'.format(str(muertos), str(heridos)),
                reply_markup=markup)
            return PREGUNTA

def cancelar(update, context):
    update.message.reply_text('¡Hasta la próxima vez!')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Genero el número secreto
secretNumber = numberGeneration()
intentos = 0

def main():
    # Genero el número secreto
    # secretNumber = numberGeneration()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PREGUNTA: [MessageHandler(Filters.regex('^Si$'),
                                      pregunta),
                       ],
            
            COMPRUEBO: [MessageHandler(Filters.text,
                                      compruebo),
                       ],
        },

        fallbacks=[MessageHandler(Filters.regex('^No$'), cancelar)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
