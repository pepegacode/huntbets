#takes screenshots of the usernames and coverts them to strings using Tesseract
from PIL import Image
import pytesseract
import numpy
import key
import os




#reads images in the images folder, then returns a list of usernames
def readImages():
    plist=[]
    scrn = os.listdir(key.imagepath)
    for f in scrn:
        img = numpy.array(Image.open(key.imagepath+'/'+f))
        read = pytesseract.image_to_string(img)
        plist += [read]
    print("Complete HERE: %s"%plist)
    return plist
    pass

#clears the images folder
def clearImages():
    files = os.listdir(key.imagepath)
    for f in files:
        os.remove(key.imagepath+"/%s"%f)




        