def disp_board(p1, p2, bMap, turn):
    """
takes dicts of values for each player and turn indicator (int = 1 or 2)
prints board
    """
    toprow = p2 if turn == 1 else p1
    bottomrow = p1 if turn == 1 else p2
    for x, y in reversed(sorted(bMap.items())):
        print((('p2 ' + x if turn == 1 else 'p1 ' + x) if x == 'store' else ' ') + '(' + repr(toprow[y]).rjust(2) + ')', end = '  ')
    print('------------')   
    print('------------  ', end = '')
    for x, y in (sorted(bMap.items())):
        print((('p1 ' + x if turn == 1 else 'p2 ' + x) if x == 'store' else x) + '(' + repr(bottomrow[y]).rjust(2) + ')', end = '  ')
    print('\n')

def place_bean(p1, p2, turn, opp, position, remaining, results):
    """
input
p1, p2 dicts => bin values
turn int => (1 or 2) for player
opp bool => True if opponent's side
position int => current bin position
remaining int => beans remaining to be placed
output
results dict
results['placedcnt'] int => total placed
results['goagain'] bool => True if player gets another turn for finishing in store
results['tostore'] bool => True
results['p1'] dict => p1 dict
results['p2'] dict => p2 dict
    """

    if (turn == 1 and opp == False) or (turn == 2 and opp == True):
        p1[position] += 1
    else:
        p2[position] += 1

    remaining -= 1
    if 'placedcnt' in results:
        results['placedcnt'] += 1
    else:
        results['placedcnt'] = 1

    if position == 7 and opp == False: #go again if store and final iteration
        results['goagain'] = True
    else:
        results['goagain'] = False
        if remaining == 0 and opp == False:   #check to see if send pieces to store
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
#        print(p1,p2)
        if opp == True and position == 6:
            nextPos = 1
            opp = False
        elif opp == False and position == 7:
            nextPos = 1
            opp = True
        else:
            nextPos = position + 1
            
        results = place_bean(p1, p2, turn, opp, nextPos, remaining, results)       

    return results

def remove_beans(pos, bVals):
#given a position and a dict, remove beans for position and return
    extracted = bVals[pos]
    bVals[pos] = 0
    return extracted

def is_game_over(p1, p2):
#  return true if either side has no beans    
    sumP1 = sum([p1[x] for x in p1.keys() if x < 7]) 
    sumP2 = sum([p2[x] for x in p2.keys() if x < 7])
#    return True
    return sumP1 == 0 or sumP2 == 0

def declare_winner(p1, p2):
    sumBinsP1 = sum([p1[x] for x in p1.keys() if x < 7])
    storeP1 = p1[7]
    sumBinsP2 = sum([p2[x] for x in p2.keys() if x < 7])
    storeP2 = p2[7]
    if storeP1 == 0:
        empty = '1'
        moved = '2'
        movedCnt= str(sumBinsP2)
    else:
        empty = '2'
        moved = '1'
        movedCnt= str(sumBinsP1)
    
    print('All bins are empty for player', empty)
    print('Remaining', movedCnt, 'beans moved to player', moved, 'store')
    print('Final Tally:')
    print('Player 1:', str(sumBinsP1 + storeP1))
    print('Player 2:', str(sumBinsP2 + storeP2))
    if (sumBinsP1 + storeP1) == (sumBinsP2 + storeP2):
        print('Game is a tie!')
    elif (sumBinsP1 + storeP1) > (sumBinsP2 + storeP2):
        print('Player 1 wins!')
    else:
        print('Player 2 wins!')          

def is_valid_response(r, bMap, bVals):
#  make sure response can be mapped and corresponds to an entry with  beans   
    if r == '':
        return False
    elif len(r) > 1 or r not in bMap:
        print('Error: must enter a letter between a and f')
        return False
    elif bVals[bMap[r]] <= 0:
        print('Error: must choose a bin with one or more beans')
        return False
    else:
        return True


if __name__ == '__main__':
#init values    
    p1BinValues = {1:4,2:4,3:4,4:4,5:4,6:4,7:0}
    p2BinValues = {1:4,2:4,3:4,4:4,5:4,6:4,7:0}
    binMap = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'store':7}
    turn = 1
    opp = False
    position = 0
    remaining = 0
    results = {}


    print('\n Welcome to Kalah')

    while not is_game_over(p1BinValues, p2BinValues):
        response = ''
        while not is_valid_response(response, binMap, p1BinValues if turn == 1 else p2BinValues):
            print('\n')
            disp_board(p1BinValues, p2BinValues, binMap, turn)
            response = input('Player ' + str(turn) + ': Choose a bin a through f: ')
            response = str(response).lower()
        position = binMap[response]
        remaining  = remove_beans(position, p1BinValues if turn == 1 else p2BinValues)
        results = {}
        results = place_bean(p1BinValues, p2BinValues, turn, opp, position + 1, remaining, results)
        print(str(results['placedcnt']), 'beans placed for player', str(turn))
        if 'tostore' in results:
            print(str(results['tostorecnt']), 'additional beans sent to store')
        if results['goagain'] == True:
            print('Player', str(turn), 'finished in own store')
            print('Player', str(turn), 'goes again')
        else:
# switch turns
            if turn == 1:
                turn = 2
            else:
                turn = 1
        opp = False                    
        p1BinValues = results['p1']
        p2BinValues = results['p2']


    declare_winner(p1BinValues, p2BinValues)
    print('Thanks for playing!')

                                                  
              
