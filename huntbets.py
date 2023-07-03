import math

#game info input section
playernumber = input('Enter number of players: ')
teamnumber = input('Enter number of teams: ')
wagerlist = {}

for i in range(int(playernumber)):
    name = input("\nEnter player name: ")
    bet = [] #clear bet
    for i in range(int(teamnumber)+1):
        if i == 1:
            bet += [int(input("Enter your "+str(i)+"st bet (on team 1): "))]
        elif i == 2:
            bet += [int(input("Enter your "+str(i)+"nd bet (on team 2): "))]
        elif i == 3:
            bet += [int(input("Enter your "+str(i)+"rd bet (on team 3): "))]
        elif i == 0:
            pass
        else:
            bet += [int(input("Enter your %sth bet (on team %s): " % (i,i)))]
    
    for i in range(int(teamnumber)):
        if i == 0:
            print("Your bet is %s on team %s, " % (bet[i],i+1), end="")
        elif i < range(int(teamnumber))[-1]:
            print("%s on team %s, " % (bet[i],i+1), end="")
        else:
            print("and %s on team %s." % (bet[i],i+1))
    wagerlist[name] = bet

print("\n"+str(wagerlist))

#math section

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




payout=[]
for i in sumlist:
    payout+=[round((pot-i)/i,2)]

print("\nPayout table: ")
for i in range(len(payout)):
    print("Team %s : %s" % (i+1,payout[i]))

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
                print("("+str(wl)+")")
            elif wl > 0:
                print("(+"+str(wl)+")")
        break
    

while True:
    exit=input("\n"+"Enter 'exit' to quit: ")
    if exit == 'exit':
        break
    else:
        continue

