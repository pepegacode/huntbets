import logging
import key
import betengine
import chip
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler,filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler

lockedin=0

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
    if lockedin == 0:    
        wager = context.args
        name = update.message.from_user.first_name
        print(context._user_id)
        print("NAME HERE: "+str(name))
        print("WAGER HERE: "+str(wager))
        player_id=context._user_id
        currentpay = betengine.bookkeep(name,wager,player_id)
        if type(currentpay) == list:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
            if update.effective_chat.id != -702820687:
                await context.bot.send_message(chat_id=-702820687, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="%s" % currentpay)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wagers are locked in!")

async def showpot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentpay = betengine.showpot()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
    

async def endgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        results=betengine.endgame(context.args[0])
        finalmessage=""
        for i in results:
            print("DICTIONARY HERE: "+str(results[i]))
            if results[i][0][1] > 0:
                finalmessage=finalmessage+"%s wins %s  (+%s)\n" % (i,results[i][0][0],results[i][0][1])
            else:
                finalmessage=finalmessage+"%s wins %s  (%s)\n" % (i,results[i][0][0],results[i][0][1])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=finalmessage)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        betengine.reset()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game has been reset, enter your wagers when ready.")
        global lockedin
        lockedin=0
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Huntbets uses parimutuel betting, more commonly known as the style of betting used for horse racing. To place a wager, enter a bet for each team, in order, separated by spaces. For example, to bet 5 on Team 1, 0 on Team 2, and 2 on Team 3, enter '/addwager 5 0 2'. You send wagers in the groupchat, or send them directly to bet_bot to place them anonymously. The pot will update in the groupchat to display the new total to everyone participating.\n\nCOMMANDS\n/addwager sets your wager for the current game.\n/retract takes back your submitted wager and refunds it to your balance, allowing you to make a new wager.\n/showpot shows the current pot and payouts per dollar for each team.\n/balance returns the balance of your account. If you would like to keep this to yourself, message betbot directly.\nADMIN COMMANDS\n/setteams sets the number of teams in play.\n/endgame ends the game, requires the number of the winning team.\n/reset resets the pot back to 0.\n/lockin Prevents new wagers from being added, or existing ones from being altered. Typically done after 2 minutes. Make sure to submit or retract your wagers before they are locked in!")

async def lockin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        global lockedin
        lockedin = 1
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wagers are locked in!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def retract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if lockedin==0:
        betengine.retract(context._user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wager retracted")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wagers are locked in!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form={'id':context._user_id}
    bal=chip.get_balance(form)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Your balance is %s" % bal)

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
    lock_handler = CommandHandler('lockin', lockin)
    retract_handler = CommandHandler('retract', retract)
    balance_handler = CommandHandler('balance', balance)
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
    application.add_handler(lock_handler)
    application.add_handler(retract_handler)
    application.add_handler(balance_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
    