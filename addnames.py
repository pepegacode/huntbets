import keyboard
import time
from PIL import Image
import pygetwindow
import pyautogui
import key
import os
import keyboard
import sys
import assistantbot as bot

#takes a screenshot of the part of the screen with the username and saves it in the Images folder
def addImage():
    if len(os.listdir(key.imagepath)) < 3:
        path = key.imagepath+"/result%s.png"%(len(os.listdir(key.imagepath))+1)
    else:
        print("team full")
        return "team full"
    titles = pygetwindow.getAllTitles()
    try:
        window = pygetwindow.getWindowsWithTitle('Hunt: Showdown')[0]
    except:
        print("Hunt is not open")

    left, top = window.topleft
    right, bottom = window.bottomright
    pyautogui.screenshot(path)
    im = Image.open(path) #this might need adjusting
    im = im.crop((left+1500,top+920,right-20,bottom-50))
    im.save(path)
    #im.show(path)
    print(left,right,top,bottom)
    pass


while True:
    press=keyboard.read_key()
    klist=["right ctrl","right shift","delete","page down","home"]
    if press in klist:
        print(press)
    if press=="right ctrl":
        addImage()
        time.sleep(.2)
    elif press=="right shift":
        bot.msg("/addteam")
        print("player added")
        time.sleep(.2)
    elif press=="delete":
        bot.msg("/lockin")
        print("wagers locked")
        time.sleep(.2)
    elif press=="page down":
        bot.msg("/check")
        time.sleep(.2)
    elif press=="home":
        time.sleep(.2)
        press2=keyboard.read_key()
        if press2=="home":
            print(press2)
            print("clearing team")
            bot.msg("/clearteam")
            time.sleep(.2)
        else:
            time.sleep(.2)
