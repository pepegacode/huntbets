import csv

def get_players():
    file = open('chips.csv','r')
    contents = csv.reader(file, delimiter=',')
    
    dictlist=[]
    ctr=0
    for i in contents:
        x = {}
        x["name"] = i[0]
        x["balance"] = float(i[1])
        x["id"] = ctr
        ctr+=1
        dictlist.append(x)
    file.close()
    return dictlist

def set_balance(form={},player_id=None):
    lod = get_players()
    file = open('chips.csv','w',encoding="utf-8",newline='')
    write=csv.writer(file, delimiter=',')
    for d in range(len(lod)):
        if d == int(player_id):
            write.writerow(form.values())
        else:
            write.writerow(lod[d].values())
    file.close()

def add_player(form={}):
    lod = get_players()
    print(lod)
    file = open('chips.csv','w',encoding="utf-8",newline='')
    write=csv.writer(file, delimiter=',')
    for d in range(len(lod)):
        write.writerow(lod[d])
    write.writerow(form.values())
    file.close()
    pass

def procWager(wager,id):
    lod=get_players()
    print(lod)
    name=lod[id]['name']
    expend=sum(wager)
    oldbal=lod[id]['balance']
    newbal=oldbal-expend
    if newbal < 0:
        return "overdraft"
    form={'name':name,'balance':newbal}
    set_balance(form,id)
    return "Wager accepted"

def procWinnings(winnings,id):
    lod=get_players()
    print(lod)
    name=lod[id]['name']
    oldbal=lod[id]['balance']
    newbal=oldbal+winnings
    form={'name':name,'balance':newbal}
    set_balance(form,id)

