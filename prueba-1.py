import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Reemplaza 'YOUR_TOKEN' con el token que obtuviste de BotFather.
TOKEN = 'YOUR_TOKEN'

# URL base de la API de Nager.at para los días festivos de España
BASE_URL = 'https://date.nager.at/Api/v2/PublicHoliday'

# Configura la instancia del bot de Telegram
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text("¡Hola! Soy tu bot de días festivos en España. Escribe /festivos seguido del año para obtener la lista de días festivos.")

def festivos(update, context):
    try:
        year = int(context.args[0])
        # Consulta la API de Nager.at para obtener los días festivos de España para el año especificado
        response = requests.get(f"{BASE_URL}/{year}/ES")
        if response.status_code == 200:
            holidays = response.json()
            if holidays:
                message = "\n".join([f"{holiday['date']} - {holiday['localName']}" for holiday in holidays])
                update.message.reply_text(f"Los días festivos en España para el año {year} son:\n{message}")
            else:
                update.message.reply_text(f"No se encontraron días festivos para el año {year}.")
        else:
            update.message.reply_text("Hubo un problema al obtener los días festivos. Inténtalo de nuevo más tarde.")
    except (IndexError, ValueError):
        update.message.reply_text("Por favor, proporciona un año válido después de /festivos. Ejemplo: /festivos 2023")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define los manejadores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("festivos", festivos, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

