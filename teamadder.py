#takes screenshots of the usernames and coverts them to strings using Tesseract
from PIL import Image
import pytesseract
import numpy
import pygetwindow
import pyautogui
import key
import os
import glob


#takes a screenshot of the part of the screen with the username and saves it in the Images folder
def addImage():
    if len(os.listdir(key.imagepath)) < 3:
        path = key.imagepath+"/result%s.png"%(len(os.listdir(key.imagepath))+1)
    #elif len(os.listdir(key.imagepath)) == 1:
    #    path = key.imagepath+"/result2.png"
    #elif len(os.listdir(key.imagepath)) == 2:
    #    path = key.imagepath+"/result3.png"
    else:
        print("team full")
        return "team full"
    titles = pygetwindow.getAllTitles()

    window = pygetwindow.getWindowsWithTitle('Hunt: Showdown')[0]

    left, top = window.topleft
    right, bottom = window.bottomright
    pyautogui.screenshot(path)
    im = Image.open(path) #this might need adjusting
    im = im.crop((left+1200,top+800,right,bottom-50))
    im.save(path)
    im.show(path)
    print(left,right,top,bottom)
    pass

#reads images in the images folder, then returns a list of usernames
def readImages():
    plist=[]
    scrn = os.listdir(key.imagepath)
    for f in scrn:
        img = numpy.array(Image.open(key.imagepath+'/'+f))
        plist += pytesseract.image_to_string(img)
    print(plist)
    return plist
    pass

addImage()
print(os.listdir(key.imagepath))
readImages()