#This file runs the telegram bot
import logging
import key
import betengine
import chip
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import InlineQueryHandler,filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler
import teamadder
import os
import keyboard
import sys
import json

lockedin = 0
teamnumber = 0

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message with a button that opens a the web app."""

    await update.message.reply_text(

        "Please press the button below to choose a color via the WebApp.",

        reply_markup=ReplyKeyboardMarkup.from_button(

            KeyboardButton(

                text="Open the color picker!",

                web_app=WebAppInfo(url="https://127.0.0.1:5000"),

            )

        ),

    )


async def setteams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        try:    
            newteamsize=int(context.args[0])
            betengine.setteam(newteamsize)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Team size updated to %s" % newteamsize)
            if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text="Team size updated to %s" % newteamsize)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Bad input, failed to update team size")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def addwager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if lockedin == 0:    
        wager = context.args

        for i in wager:
            if int(i) < 0:
                await context.bot.send_message(chat_id=key.group_id, text="No negatives!")

        name = update.message.from_user.first_name
        print(context._user_id)
        print("NAME HERE: "+str(name))
        print("WAGER HERE: "+str(wager))
        player_id=context._user_id
        currentpay = betengine.bookkeep(name,wager,player_id)
        if type(currentpay) == list:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
            if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="%s" % currentpay)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wagers are locked in!")

async def showpot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentpay = betengine.showpot()
    print("WAGERLIST CHECK: %s"%betengine.getwagerlist())
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Payout: %s\nPot: %s" % (currentpay[0],currentpay[1]))
    

async def endgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        global teamnumber
        global lockedin
        results=betengine.endgame(context.args[0])
        finalmessage=""
        for i in results:
            print("DICTIONARY HERE: "+str(results[i]))
            if results[i][0][1] > 0:
                finalmessage=finalmessage+"%s wins %s  (+%s)\n" % (i,results[i][0][0],results[i][0][1])
            else:
                finalmessage=finalmessage+"%s wins %s  (%s)\n" % (i,results[i][0][0],results[i][0][1])
        teamnumber = 0
        lockedin=0
        await context.bot.send_message(chat_id=update.effective_chat.id, text=finalmessage)
        if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text=finalmessage)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        betengine.reset()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Game has been reset, enter your wagers when ready.")
        global lockedin
        global teamnumber
        lockedin=0
        teamnumber=0
        if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text="Game has been reset, enter your wagers when ready.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Huntbets uses parimutuel betting, more commonly known as the style of betting used for horse racing. To place a wager, enter a bet for each team, in order, separated by spaces. For example, to bet 5 on Team 1, 0 on Team 2, and 2 on Team 3, enter '/addwager 5 0 2'. You send wagers in the groupchat, or send them directly to bet_bot to place them anonymously. The pot will update in the groupchat to display the new total to everyone participating. A team wins by extracting with the bounty of the boss target (wild targets do not count). In the event of a 'tie' or the bounty being split, the first team to extract with their bounty wins.\n\nUse /register to get started!\n\nCOMMANDS\n/addwager sets your wager for the current game.\n/retract takes back your submitted wager and refunds it to your balance, allowing you to make a new wager.\n/showpot shows the current pot and payouts per dollar for each team.\n/balance returns the balance of your account. If you would like to keep this to yourself, message betbot directly.\nADMIN COMMANDS\n/setteams sets the number of teams in play.\n/endgame ends the game, requires the number of the winning team.\n/reset resets the pot back to 0.\n/lockin Prevents new wagers from being added, or existing ones from being altered. Typically done after 2 minutes. Make sure to submit or retract your wagers before they are locked in!\n/addteam adds a team, displaying their team size, names and ranks in the groupchat\n/clearteam clears the images folder")

async def lockin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        global lockedin
        lockedin = 1
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Wagers are locked in!")
        if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text="Wagers are locked in!")
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

async def addteam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global teamnumber
    if context._user_id in key.adminlist:
        newteam = teamadder.readImages()
        size=""
        if len(newteam) == 1:
            size="SOLO"
        elif len(newteam) == 2:
            size="DUO"
        elif len(newteam) == 3:
            size="TRIO"
        else:
            size="EMPTY"
        members = ""
        for i in range(len(newteam)):
            members = members+"\n"+newteam[i]
        files = os.listdir(key.imagepath)
        for f in files:
            os.remove(key.imagepath+"/%s"%f)
        if size != "EMPTY":
            teamnumber += 1
        betengine.setteam(teamnumber)
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Team %s</b>\n\n%s\n%s"%(teamnumber,size, members),parse_mode="HTML")
        if update.effective_chat.id != key.group_id:
                await context.bot.send_message(chat_id=key.group_id, text="<b>Team %s</b>\n\n%s\n%s"%(teamnumber,size, members),parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def clearteam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        teamadder.clearImages()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Team cleared.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def binds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Keybinds:\nRight Ctrl: Add player to team\nRight Shift: Publish team to roster\nDelete: Lock in wagers\nPage Down: Check what players are in the Images folder\nHome: Clear teams from the Images folder")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in key.adminlist:
        newteam = teamadder.readImages()
        size=""
        if len(newteam) == 1:
            size="SOLO"
        elif len(newteam) == 2:
            size="DUO"
        elif len(newteam) == 3:
            size="TRIO"
        else:
            size="EMPTY"
        members = ""
        for i in range(len(newteam)):
            members = members+"\n"+newteam[i]
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Team %s</b>\n\n%s\n%s"%(teamnumber+1,size, members),parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    name = update.message.from_user.first_name
    print("ID HERE: %s"%context._user_id)
    print("NAME HERE: "+str(name))
    player_id=context._user_id
    
    lod = chip.get_players()
    regi=0
    form={'name':name,'balance':5,'id':player_id}
    for i in lod:
        if int(i['id']) == int(player_id):
            regi=1
    if regi==0:
        chip.add_player(form)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Huntbets!")

    
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Print the received data and remove the button."""

    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string

    # (see webappbot.html)

    data = json.loads(update.effective_message.web_app_data.data)
    print(data)
    await update.message.reply_html(

        text=f"You selected the color with the HEX value <code>{data['hex']}</code>. The "

        f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>.",

        reply_markup=ReplyKeyboardRemove(),

    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(key.botkey).build()
    
    start_handler = CommandHandler('start', start)
    add_wager_handler = CommandHandler('addwager', addwager)
    team_size_handler = CommandHandler('setteams', setteams)
    help_handler = CommandHandler('help', help)
    end_game_handler = CommandHandler('endgame', endgame)
    reset_handler = CommandHandler('reset', reset)
    show_pot_handler = CommandHandler('showpot', showpot)
    lock_handler = CommandHandler('lockin', lockin)
    retract_handler = CommandHandler('retract', retract)
    balance_handler = CommandHandler('balance', balance)
    team_add_handler = CommandHandler('addteam', addteam)
    team_clear_handler = CommandHandler('clearteam', clearteam)
    binds_handler = CommandHandler('binds', binds)
    check_handler = CommandHandler('check', check)
    register_handler = CommandHandler('register', register)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(add_wager_handler)
    application.add_handler(team_size_handler)
    application.add_handler(help_handler)
    application.add_handler(end_game_handler)
    application.add_handler(reset_handler)
    application.add_handler(show_pot_handler)
    application.add_handler(lock_handler)
    application.add_handler(retract_handler)
    application.add_handler(balance_handler)
    application.add_handler(team_add_handler)
    application.add_handler(team_clear_handler)
    application.add_handler(binds_handler)
    application.add_handler(check_handler)
    application.add_handler(register_handler)
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.add_handler(unknown_handler)

    application.run_polling()
    
    