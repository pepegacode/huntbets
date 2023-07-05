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

    for i in range(len(wager)):
        try:
            wager[i]=float(wager[i])
        except:
            print("Invalid character, wager not accepted.")
            return "Invalid character, wager not accepted."
    
    
    if len(wager)==teamnumber:
        wagerlist[name]=wager
        #wagerlist['id']=player_id
    else:
        print("Invalid length, wager not accepted. Currently there are %s teams." % teamnumber)
        return "Invalid length, wager not accepted. Currently there are %s teams." % teamnumber
    
    submitted=0
    for i in wagerlist:
        if i ==

    trx = chip.procWager(wager,player_id)
    if trx == 'overdraft':
        return trx
    

    #print(wagerlist)
    
    playernumber+=1
    ctr=0
    teamsum=0
    sumlist=[]
    for k in wagerlist:
        
        for j in wagerlist[k]:
            
            if ctr == int(teamnumber):
                break
            for i in wagerlist:
                if ctr == int(teamnumber):
                    break
                teamsum+=wagerlist[i][ctr]
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
            winnings=round(wagerlist[i][gwinner]+wagerlist[i][gwinner]*payout[gwinner],2)
            print("\n"+str(i)+" wins "+str(winnings))
            wl=round(winnings-sum(wagerlist[i]),2)
            if wl < 0:
                print("(%s)"%round(wl,2))
            elif wl > 0:
                print("(+%s)"%round(wl,2))
            wagerlist[i]=[winnings,wl]
            chip.procWinnings(winnings,wagerlist[i]['id'])

        return wagerlist

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
            



