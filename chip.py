#This file deals with managing player balances stored on the chips.csv file

import csv

def get_players():
    file = open('chips.csv','r')
    contents = csv.reader(file, delimiter=',')
    
    dictlist=[]
    
    for i in contents:
        x = {}
        x["name"] = i[0]
        x["balance"] = float(i[1])
        x["id"] = i[2]
        
        dictlist.append(x)
    file.close()
    return dictlist

def set_balance(form={}):
    lod = get_players()
    for i in lod:
        if int(i['id']) == int(form['id']):
            i['balance'] = form['balance']
    file = open('chips.csv','w',encoding="utf-8",newline='')
    write=csv.writer(file, delimiter=',')
    for d in range(len(lod)):
        write.writerow(lod[d].values())
    file.close()

def get_balance(form):
    lod = get_players()
    for i in lod:
        if int(i['id']) == int(form['id']):
            return i['balance']

def add_player(form={}):
    lod = get_players()
    print(lod)
    file = open('chips.csv','w',encoding="utf-8",newline='')
    write=csv.writer(file, delimiter=',')
    for d in range(len(lod)):
        write.writerow(lod[d].values())
    write.writerow(form.values())
    file.close()
    pass

def procWager(wager,id):
    lod=get_players()
    print(lod)
    name=""
    for i in lod:
        if int(i['id']) == int(id):
            name = i['name']

    expend=sum(wager)
    oldbal=0

    for i in lod:
        if int(i['id']) == int(id):
            oldbal = i['balance']

    newbal=oldbal-expend
    if newbal < 0:
        return "overdraft"
    print("FORM HERE: %s, %s, %s"%(name,newbal,id))
    form={'name':name,'balance':newbal, 'id':id}
    set_balance(form)
    return "Wager accepted"

def procWinnings(winnings,id):
    lod=get_players()
    print(lod)
    name=""
    for i in lod:
        if int(i['id']) == int(id):
            name = i['name']

    oldbal=0
    for i in lod:
        if int(i['id']) == int(id):
            oldbal = i['balance']

    newbal=oldbal+winnings
    form={'name':name,'balance':newbal,'id':id}
    set_balance(form)

