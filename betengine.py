import chip

wagerlist={}
playernumber=0
teamnumber=3
pot=0
payout=[]

#set the number of teams
def setteam(x):
    global teamnumber
    teamnumber=x

#adds a wager to the wagerlist and returns the payout table. Takes a name and a list, returns a list with current payout and pot.
def bookkeep(name,wager,player_id):
    global playernumber
    global pot

    lod = chip.get_players()
    regi=0
    form={'name':name,'balance':0,'id':player_id}
    for i in lod:
        if int(i['id']) == int(player_id):
            regi=1
    if regi==0:
        chip.add_player(form)

    print("WAGERLIST HERE: %s"%wagerlist)

    for i in range(len(wager)):
        try:
            wager[i]=float(wager[i])
        except:
            print("Invalid character, wager not accepted.")
            return "Invalid character, wager not accepted."
    
    submitted=0
    for i in wagerlist:
        if wagerlist[i][1] == player_id:
            submitted=1
            return "Wager already submitted"

    
    
    #WAGER ENTERED INTO WAGERLIST HERE
    if len(wager)!=teamnumber:
        print("Invalid length, wager not accepted. Currently there are %s teams." % teamnumber)
        return "Invalid length, wager not accepted. Currently there are %s teams." % teamnumber
    
    trx = chip.procWager(wager,player_id)
    if trx == 'overdraft':
        return trx

    wagerlist[name]=[wager,player_id]

    #print(wagerlist)
    
    playernumber+=1
    ctr=0
    teamsum=0
    sumlist=[]
    for k in wagerlist:
        
        for j in wagerlist[k][0]:
            
            if ctr == int(teamnumber):
                break
            for i in wagerlist:
                if ctr == int(teamnumber):
                    break
                teamsum+=wagerlist[i][0][ctr]
                #print("ts: "+str(teamsum))
            
            sumlist+=[teamsum]
            #print("sl: "+str(sumlist))
            
            ctr+=1
            teamsum=0
    pot=sum(sumlist)
    global payout
    payout=[]
    for i in sumlist:
        payout+=[round((pot-i)/i,2)]
    print("payout: "+str(payout))
    print("pot: "+str(pot))
    return [payout,pot]

def endgame(gwinner):
    
    try:
            gwinner=int(gwinner)-1
    except:
        print("'%s' is not a number asshole" % (gwinner))
        return "'%s' is not a number asshole" % gwinner
        
    
    if gwinner in range(len(payout)):
        pass
    else:
        print("not a valid team")
        return "not a valid team"


    if type(gwinner) == type(1):
    
        for i in wagerlist:
            winnings=round(wagerlist[i][0][gwinner]+wagerlist[i][0][gwinner]*payout[gwinner],2)
            print("\n"+str(i)+" wins "+str(winnings))
            wl=round(winnings-sum(wagerlist[i][0]),2)
            if wl < 0:
                print("(%s)"%round(wl,2))
            elif wl > 0:
                print("(+%s)"%round(wl,2))
            wagerlist[i][0]=[winnings,wl]
            chip.procWinnings(winnings,wagerlist[i][1])

        return wagerlist

def retract(player_id):
    removewager=0
    for i in wagerlist:
        if wagerlist[i][1] == player_id:
            removewager=i
    chip.procWinnings(sum(wagerlist[removewager][0]),player_id)
    wagerlist.pop(removewager)

    pass

def showpot():
    return [payout,pot]

def reset():
    global wagerlist
    global playernumber
    global teamnumber
    global pot
    wagerlist={}
    playernumber=0
    teamnumber=3
    pot=0
            



