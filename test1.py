import json
import ccxt
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
okx=ccxt.okx()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    okx_json = json.loads(json.dumps(okx.fetch_ticker('TON/USDT')))
    text_prices = okx_json.get('last')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_prices)

def getKey():
    f = open("apikey.dat", "r")
    key = f.readline().replace('\n','')
    print('token = ' + key)
    f.close()
    return key

if __name__ == '__main__':
    token=getKey()
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    prices_handler = CommandHandler('prices', prices)



    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(prices_handler)

    application.run_polling()