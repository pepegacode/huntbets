import math

#game info input section
playernumber = input('Enter number of players: ')
teamnumber = input('Enter number of teams')
wagerlist = {}

for i in range(int(playernumber)):
    name = input("\nEnter player name: ")
    bet = [] #clear bet
    for i in range(4):
        if i == 1:
            bet += [int(input("Enter your "+str(i)+"st bet (on team 1): "))]
        elif i == 2:
            bet += [int(input("Enter your "+str(i)+"nd bet (on team 2): "))]
        elif i == 3:
            bet += [int(input("Enter your "+str(i)+"rd bet (on team 3): "))]
    print("Your bet is "+str(bet[0])+" on Team 1, "+str(bet[1])+" on Team 2, and "+str(bet[2])+" on Team 3") 
    wagerlist[name] = bet

print("\n"+str(wagerlist))

#math section
t1sum = 0
t2sum = 0
t3sum = 0

for i in wagerlist:
    t1sum += wagerlist[i][0]
    t2sum += wagerlist[i][1]
    t3sum += wagerlist[i][2]

pot = t1sum+t2sum+t3sum
payout={"Team 1":t1sum,"Team 2":t2sum,"Team 3":t3sum}
print("\n"+"Team 1 total = "+str(t1sum)+"\nTeam 2 total = "+str(t2sum)+"\nTeam 3 total = "+str(t3sum)+"\nThe pot is "+str(pot))
for i in payout:
    pr=(pot-payout[i])/payout[i]
    payout[i]=round(pr,2)

print("Payout table: "+str(payout))
while True:  
    gwinner = input("\nWho won the game? Enter 'team1','team2', or 'team3': ")

    if gwinner == "team1":
        for i in wagerlist:
            winnings=wagerlist[i][0]+wagerlist[i][0]*payout["Team 1"]
            print("\n"+str(i)+" wins "+str(winnings))
            wl=winnings-sum(wagerlist[i])
            if wl < 0:
                print("("+str(wl)+")")
            elif wl > 0:
                print("(+"+str(wl)+")")
        break
    elif gwinner == "team2":
        for i in wagerlist:
            winnings=wagerlist[i][1]+wagerlist[i][1]*payout["Team 2"]
            print("\n"+str(i)+" wins "+str(winnings))
            wl=winnings-sum(wagerlist[i])
            if wl < 0:
                print("("+str(wl)+")")
            elif wl > 0:
                print("(+"+str(wl)+")")
        break
    elif gwinner == "team3":
        for i in wagerlist:
            winnings=wagerlist[i][2]+wagerlist[i][2]*payout["Team 3"]
            print("\n"+str(i)+" wins "+str(winnings))
            wl=winnings-sum(wagerlist[i])
            if wl < 0:
                print("("+str(wl)+")")
            elif wl > 0:
                print("(+"+str(wl)+")")
        break
    else:
        print("invalid input")
        continue

while True:
    exit=input("\n"+"Enter 'exit' to quit: ")
    if exit == 'exit':
        break
    else:
        continue

