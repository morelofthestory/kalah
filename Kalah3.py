p1BinValues = {1:4,2:4,3:4,4:4,5:4,6:4,7:0}
p2BinValues = {1:4,2:4,3:4,4:4,5:4,6:4,7:0}
binMap = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'STORE':7}
turn = 1

def dispBoard(p1, p2, turn):

    toprow = p2 if turn == 1 else p1
    bottomrow = p1 if turn == 1 else p2
    for x, y in reversed(sorted(binMap.items())):
        print(x+ '(' + repr(toprow[y]).rjust(2) + ')', end = '  ')
    print('---------')   
    print('---------  ', end = '')
    for x, y in (sorted(binMap.items())):
        print(x+ '(' + repr(bottomrow[y]).rjust(2) + ')', end = '  ')
    print('\n')

def placeBean(p1, p2, turn, opp, position, remaining, results):

    if (turn == 1 and opp == False) or (turn == 2 and opp == True):
        p1[position] += 1
    else:
        p2[position] += 1

    remaining -= 1
    if 'placed' in results:
        results['placed'] += 1
    else:
        results['placed'] = 1

    if position == 7 and opp == False: #go again if store and final iteration
        results['goagain'] = True
    else:
        results['goagain'] = False
                
    if remaining == 0 and opp == False:  #check to see if send pieces to store
        if turn == 1 and p1[position] == 1 and p2[7 - position] > 0:
            results['tostore'] = True
            results['tostorecnt'] = (1 + p2[7 - position])
            p1[7] += results['tostorecnt']
            p1[position] = 0
            p2[7-position] = 0
        elif turn == 2 and p2[position] == 1 and p1[7 - position] > 0:
            results['tostore'] = True
            results['tostorecnt'] = (1 + p1[7 - position])
            p2[7] += results['tostorecnt'] 
            p2[position] = 0
            p1[7-position] = 0

    results['p1'] = p1
    results['p2'] = p2

    if remaining > 0: #recursive call
        if opp == True and position == 6:
            nextPos = 1
            opp = False
        elif opp == False and position == 7:
            nextPos = 1
            opp = True
        else:
            nextPos = position + 1
            
        results = placeBean(p1, p2, turn, opp, nextPos, remaining, results)       

    return results


def gameover(p1, p2):
    sumr1 = sum([p1[x] for x in p1.keys() if x < 7]) 
    sumr2 = sum([p2[x] for x in p2.keys() if x < 7])
    return sumr1 == 0 or sumr2 == 0

turn = 1
opp = False
position = 5
remaining = 4
results = {}

dispBoard(p1BinValues, p2BinValues, 1)

results = placeBean(p1BinValues, p2BinValues, turn, opp, position, remaining, results)
p1BinValues = results['p1']
p2BinValues = results['p2']

dispBoard(p1BinValues, p2BinValues, 1)

print(gameover(p1BinValues, p2BinValues))

                                                  
              
