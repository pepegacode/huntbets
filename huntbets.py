import math

global np
global ng

ng=0
np=0
wagerlist = {}
playernumber=0
teamnumber=0

#player info input section
def playerinput():
    global playernumber
    while True:
        
        playernumber = input('Enter number of players: ')
        try:
            playernumber=int(playernumber)
        except:
            print("'%s' is not a number asshole" % (playernumber))
            continue

        if type(playernumber) == type(1):
            break    

#game info input section
def gameinput():
    global teamnumber
    global wagerlist

    while True:

        teamnumber = input('Enter number of teams: ')
        try:
            teamnumber=int(teamnumber)
        except:
            print("'%s' is not a number asshole" % (teamnumber))
            continue

        if type(teamnumber) == type(1):
            break    
    
    for i in range(int(playernumber)):    
        name = input("\nEnter player name: ")
        bet = [] #clear bet
        for i in range(int(teamnumber)+1):
            while True:
                if i == 1:
                    bet += [input("Enter your %sst bet (on team 1): "%i)]
                elif i == 2:
                    bet += [input("Enter your %snd bet (on team 2): "%i)]
                elif i == 3:
                    bet += [input("Enter your %srd bet (on team 3): "%i)]
                elif i == 0:
                    pass
                else:
                    bet += [input("Enter your %sth bet (on team %s): " % (i,i))]
                
                if i!=0:
                    try:
                        bet[i-1]=int(bet[i-1])
                    except:
                        print("%s is not a number"%bet[i-1])

                    if type(bet[i-1]) != type(1):
                        bet=[]
                        continue
                    else:
                        break
                else:
                    break
                
                

        print(bet)
        for i in range(int(teamnumber)):
            if i == 0:
                print("%s's wager is %s on team %s, " % (name,bet[i],i+1), end="")
            elif i < range(int(teamnumber))[-1]:
                print("%s on team %s, " % (bet[i],i+1), end="")
            else:
                print("and %s on team %s." % (bet[i],i+1))
        wagerlist[name] = bet

        bookkeep()

    print("\n"+str(wagerlist))

#math section
def bookkeep():
    pot=0
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
            
            sumlist+=[teamsum]
            pot+=teamsum
            ctr+=1
            teamsum=0
    global payout
    payout=[]
    for i in sumlist:
        payout+=[round((pot-i)/i,2)]

    print("\nPayout table: ")
    for i in range(len(payout)):
        print("Team %s : %s" % (i+1,payout[i]))

def winner():
    while True:  
        gwinner = input("\nWho won the game? Enter the number of the winning team (eg '1'): ")

        try:
            gwinner=int(gwinner)-1
        except:
            print("'%s' is not a number asshole" % (gwinner))
            continue
        
        if gwinner in range(len(payout)):
            pass
        else:
            print("not a valid team")
            continue

        if type(gwinner) == type(1):
        
            for i in wagerlist:
                winnings=wagerlist[i][gwinner]+wagerlist[i][gwinner]*payout[gwinner]
                print("\n"+str(i)+" wins "+str(winnings))
                wl=winnings-sum(wagerlist[i])
                if wl < 0:
                    print("(%s)"%round(wl,2))
                elif wl > 0:
                    print("(+%s)"%round(wl,2))
            break
    

while True:
    if np==0:
        playerinput()
    gameinput()
    bookkeep()
    winner()
    while True:
        
        newgame=input("Enter 'game' to start a new game, or 'exit' to quit: ")
        if newgame == 'game':
            ng = 1
            newplayers=input("Press enter to continue with current players or type 'player' to change player info: ")
            if newplayers=='player':
                break
            else:
                np=1
                break
        elif newgame == 'exit':
            ng = 0
            break
        else:
            continue
    
    if ng == 1:
        continue
    else:
        break

