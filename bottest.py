import logging
import key
import betengine
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler,filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def setteams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        try:    
            newteamsize=int(context.args[0])
            betengine.setteam(newteamsize)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Team size updated to %s" % newteamsize)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Bad input, failed to update team size")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def addwager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wager = context.args
    name = context._user_id
    print("NAME HERE: "+str(name))
    print("WAGER HERE: "+str(wager))
    currentpay = betengine.bookkeep(name,wager)
    if type(currentpay) == list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="%s" % currentpay)

async def showpot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentpay = betengine.showpot()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
    

async def endgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        results=betengine.endgame(context.args[0])
        finalmessage=""
        for i in results:
            print("DICTIONARY HERE: "+str(results[i]))
            if results[i][1] > 0:
                finalmessage=finalmessage+"%s wins %s  (+%s)\n" % (i,results[i][0],results[i][1])
            else:
                finalmessage=finalmessage+"%s wins %s  (%s)\n" % (i,results[i][0],results[i][1])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=finalmessage)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        betengine.reset()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game has been reset.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/addwager sets your wager for the current game\n/showpot shows the current pot and payouts per dollar for each team\nADMIN COMMANDS\n/setteams sets the number of teams in play\n/endgame ends the game, requires the number of the winning team\n/reset resets the pot back to 0")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(key.botkey).build()
    
    start_handler = CommandHandler('start', start)
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    add_wager_handler = CommandHandler('addwager', addwager)
    team_size_handler = CommandHandler('setteams', setteams)
    help_handler = CommandHandler('help', help)
    end_game_handler = CommandHandler('endgame', endgame)
    reset_handler = CommandHandler('reset', reset)
    show_pot_handler = CommandHandler('showpot', showpot)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    #application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(add_wager_handler)
    application.add_handler(team_size_handler)
    application.add_handler(help_handler)
    application.add_handler(end_game_handler)
    application.add_handler(reset_handler)
    application.add_handler(show_pot_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
    