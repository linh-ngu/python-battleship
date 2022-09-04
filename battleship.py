import copy as c
import random as rd
import numpy as np
import time

possible = [[] for i in range(9)]
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
mode = 'targeting'
coords = [0, 0]
prev_coords = [0, 0]

def num_player(num_player): #creates boards based on which mode the player chose
    if(num_player == 2):
        global playerboard, ai_board, player_gameboard, ai_gameboard, player_ships_remaining, ai_ships_remaining, player_placement, ai_placement
        playerboard = [(['░'] * 10) for i in range(10)]
        ai_board = [(['░'] * 10) for i in range(10)]
        player_gameboard = [(['░'] * 10) for i in range(10)]
        ai_gameboard = [(['░'] * 10) for i in range(10)] #board that ai plays on
        player_ships_remaining = [int(i) for i in range(len(numship), 0, -1)] #how many ships the player has remaining, used by ai
        ai_ships_remaining = [int(i) for i in range(len(numship), 0, -1)]
        player_placement = {}
        ai_placement = {}
    else:
        global playerboard1, playerboard2, main_gameboard1, main_gameboard2, player1_ships_remaining, player2_ships_remaining, player1_placement, player2_placements
        playerboard1 = [(['░'] * 10) for i in range(10)]
        playerboard2 = [(['░'] * 10) for i in range(10)]
        main_gameboard1 = [(['░'] * 10) for i in range(10)] #board that player 1 plays on
        main_gameboard2 = [(['░'] * 10) for i in range(10)] #board that player 2 plays on
        player1_ships_remaining = [int(i) for i in range(len(numship), 0, -1)]
        player2_ships_remaining = [int(i) for i in range(len(numship2), 0, -1)]
        player1_placement = {}
        player2_placements = {}

def print_board(pb): #prints inputed board
    print('')
    for i in range(len(pb)):
        print(nums[i], end = '   ')
        for j in range(len(pb[i])):
            print(pb[i][j], end = '  ')
        print('')
    print('\n    A  B  C  D  E  F  G  H  I  J')
    print('\n=======================================')

def instructions(): #prints instructions
    print("\nWhile I am setting up the boards, here are some basic information:\n"
      "\nInstructions:\n"
      " - The board is arranged in a 10 by 10 grid\n"
      " - Each player will start out with " + str(len(numship)) + " ships and will each arrange them on their respective boards\n"
      " - Once the game has start, each player will take turn firing shots at the other's board\n"
      " - Mark every shot as either a hit on an enemy ship, or a miss in the water\n"
      " - The game ends once either player loses all of their ships\n"
      "\nLegend :\n"
      " - ░ marks a square as empty\n"
      " -   marks a square as a miss\n"
      " - X marks a square as a hit\n"
      " - C marks a square for confirmation\n"
      " - S marks a square as sink")
    input("Press enter to continue")
    print('\n=======================================')
  
def placement_info(ns, pb): #asks player for ship placement information. if information invalid, recurse. ns stands for number of ships, pb stands for playerboard
    print_board(pb)
    shiplen = input('Enter which ship you wish to place ' + str(ns) + ': ')
    while shiplen not in [str(i) for i in range(1,10)] or int(shiplen) not in ns:
        shiplen = input('Invalid ship. Enter which ship you wish to place ' + str(ns) + ': ')
    shiplen = int(shiplen)
    orientation = input('Enter your ship orientation (H/V): ')
    placerow = input('Enter your row: ')
    placecol = input('Enter your column: ')
    print('\n=======================================')
    placement(orientation, placerow, placecol, shiplen, pb, ns)

def placement(ori, r, c, s, pb, ns): #checks the validity of the information and places down ship.
    if ori.upper() == 'H':
        if(r in nums):
            if(c.upper() in letters):
                c = letters.index(c.upper())
                if(c + s <= 10):
                    if(check_placement(ori, r, c, s, pb)):   
                        for i in range(c, c + s):
                            pb[int(r)][i] = s
                        if(confirm_placement(pb)):
                            if(setting == '2'):
                                player_placement[s] = (int(r), c, 'h')
                            else:
                                if(pb == playerboard2):
                                    player2_placements[s] = (int(r), c, 'h')
                                elif(pb == playerboard1):
                                    player1_placement[s] = (int(r), c, 'h')
                            ns.remove(s)
                            print('\n=======================================')
                        else:
                            for i in range(c, c + s):
                                pb[int(r)][int(i)] = '░'
                    else:
                        print('\nInvalid placement. Ship already located there.')
                        placement_info(ns, pb)
                else:
                    print('\nInvalid placement. Out of bounds')
                    placement_info(ns, pb)
            else:
                print('\nInvalid placement. Incorrect input for column.')
                placement_info(ns, pb)
        else:
            print('\nInvalid placement. Incorrect input for row.')
            placement_info(ns, pb)
    elif ori.upper() == 'V':
        if(r in nums):
            r = int(r)
            if(c.upper() in letters):
                c = letters.index(c.upper())
                if(r + s <= 10):
                    if(check_placement(ori, r, c, s, pb)):
                        for i in range(r, r + s):
                            pb[i][c] = s
                        if(confirm_placement(pb)):
                            if(setting == '2'):
                                player_placement[s] = (int(r), c, 'v')
                            else:
                                if(pb == playerboard1):
                                    player1_placement[s] = (int(r), c, 'h')
                                elif(pb == playerboard2):
                                    player2_placements[s] = (int(r), c, 'h')
                            ns.remove(s)
                            print('\n=======================================')
                        else:
                            for i in range(c, c + s):
                                pb[r][i] = '░'
                    else:
                        print('\nInvalid placement. Ship already located there.')
                        placement_info(ns, pb)
                else:
                    print('\nInvalid placement. Out of bounds')
                    placement_info(ns, pb)
            else:
                print('\nInvalid placement. Incorrect input for column.')
                placement_info(ns, pb)
        else:
            print('\nInvalid placement. Incorrect input for row.')
            placement_info(ns, pb)
    else:
        print('\nInvalid orientation.')
        placement_info(ns, pb)

def check_placement(ori, r, c, s, pb): #checks if selected ship intercepts with placed ships
    temp = []
    if ori == 'h':
        for i in range(c, c + s):
            if(pb[int(r)][i] == '░'):    
                temp.append(False)
            else:
                temp.append(True)
        if sum(temp) == 0:
            return True
        else:
            return False
    elif ori == 'v':
        for i in range(r, r + s):
            if(pb[i][c] == '░'):    
                temp.append(False)
            else:
                temp.append(True)
        if sum(temp) == 0:
            return True
        else:
            return False

def confirm_placement(pb): #confirm ship placement
    print_board(pb)
    Flag = True
    while Flag:
        confirm = input('Is this correct? (Y/N): ')    
        if confirm not in ['N', 'n', 'Y', 'y']:
            print('\nEnter Y or N.')
            print('\n=======================================')          
        elif confirm.upper() == 'Y':
            Flag = False
            return True
        elif confirm.upper() == 'N':
            Flag = False
            return False
    
def check_shooting(r, c, pb, opb, sr, pp): #checks if shoot position is valid
    if(r in nums):
        r = int(r)
        if(c.upper() in letters):
            c = letters.index(c.upper())
            if(pb[r][c] == '░'):
                pb[r][c] = 'C'
                if(confirm_placement(pb)):
                    print('\n=======================================')
                    return True
                else:
                    pb[r][c] = '░'
                    player_shooting(pb, opb, sr, pp)
                    return False
            else:
                print('\n=======================================')
                print('\nInvalid placement. The square you picked has already been revealed.')
                player_shooting(pb, opb, sr, pp)
        else:
            print('\n=======================================')
            print('\nInvalid placement. Incorrect input for column.')
            player_shooting(pb, opb, sr, pp)
    else:
        print('\n=======================================')
        print('\nInvalid placement. Incorrect input for row.')
        player_shooting(pb, opb, sr, pp)

def check_hit(r,c, mg2): #checks if shot hit ship
    if(mg2[r][c] != '░'):
        return True

def ai_ship_placement(shipl, counter): #algorithm for ai ship placement
    
    #condition to stop recursion after placing the last ship
    if(shipl == 0):
        return True
    
    #check if placing a ship at that square is possible and append to list if possible
    for i in range(10):
        for j in range(10):
            if(j + shipl <= 10):
                possible[counter].append((i, j, 'h'))
            if(i + shipl <= 10):
                possible[counter].append((i, j, 'v'))
    
    #removes ships that are not possible after the ship before it was placed
    possible[counter] = [x for x in possible[counter] if check_placement(x[2], x[0], x[1], shipl, ai_board)]
    
    #randomly chooses the position of the ship
    choose = rd.randint(0, len(possible[counter]) - 1)        
    
    #placing down ship on the board
    for j in range(len(possible[counter])):
        if(possible[counter][choose][2] == 'h'):
            for k in range(shipl):
                ai_board[possible[counter][choose][0]][possible[counter][choose][1] + k] = shipl
        elif(possible[counter][choose][2] == 'v'):
            for k in range(shipl):
                ai_board[possible[counter][choose][0] + k][possible[counter][choose][1]] = shipl
    
    ai_placement[shipl] = possible[counter][choose]
    
    #calls the next recursion
    ai_ship_placement(shipl - 1, counter + 1)
   
def player_shooting(pb, opb, sr, pp): #player guess, enters player board then opponent
    print('\nEnemy\'s board')
    print_board(pb)
    guessrow = input('Enter the row you wish to shoot: ')
    guesscol = input('Enter the column you wish to shoot: ')
    print('\n=======================================')
    if(check_shooting(guessrow, guesscol, pb, opb, sr, pp)):
        guessrow = int(guessrow)
        guesscol = letters.index(guesscol.upper())
        if(check_hit(guessrow, guesscol, opb)):
            pb[guessrow][guesscol] = 'X'
            opb[guessrow][guesscol] = 'X'
            if(check_sink(opb, pb, sr, pp)):
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nYou sunk a boat!')
                time.sleep(.8)
                print('\n=======================================')
                print_board(pb)
            else:
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nIt\'s a hit!')
                time.sleep(.8)
                print('\n=======================================')
                print_board(pb)
        else:
            pb[guessrow][guesscol] = ' '
            for i in range(3):
                time.sleep(.8)
                print("...")
            print('\nYou missed.')
            time.sleep(.8)
            print('\n=======================================')
            print_board(pb)

def check_sink(pb, opb, sr, pp):
    pbs = sum(pb, [])
    for i in sr:
        if i not in pbs:
            if(pp[i][2] == 'h'):
                for j in range(i):
                    pb[pp[i][0]][pp[i][1] + j] = 'S'
                    opb[pp[i][0]][pp[i][1] + j] = 'S'
            elif(pp[i][2] == 'v'):
                for j in range(i):
                    pb[pp[i][0] + j][pp[i][1]] = 'S'
                    opb[pp[i][0] + j][pp[i][1]] = 'S'
            pp.pop(i)
            sr.remove(i)
            return True



def probability_board_targeting(ships_remaining, prob, counter):
    if(counter == len(player_ships_remaining)):
        return np.max(prob)
    for i in range(10):
        for j in range(10):
            if(j + ships_remaining[counter] <= 10 and check_placement('h', i, j, ships_remaining[counter], ai_gameboard)): #horizontal
                for k in range(ships_remaining[counter]):
                    prob[i][j + k] += 1
            
            if(i + ships_remaining[counter] <= 10 and check_placement('v', i, j, ships_remaining[counter], ai_gameboard)): #vertical 
                for k in range(ships_remaining[counter]):
                    prob[i + k][j] += 1
                           
    return probability_board_targeting(ships_remaining, prob, counter + 1)

def probability_board_hunting(pc, co, prob, ct):
    global prev_coords, coords
    
    try:
        if(ai_gameboard[co[0] - 1][co[1]] != 'X' and ai_gameboard[co[0] - 1][co[1]] != ' ' and ai_gameboard[co[0] - 1][co[1]] != 'S'):
            prob[co[0] - 1][co[1]] += 1
            if(co[0] + 1 == pc[0]):
                prob[co[0] - 1][co[1]] += 8
    except IndexError:
        pass
    try:
        if(ai_gameboard[co[0] + 1][co[1]] != 'X' and ai_gameboard[co[0] + 1][co[1]] != ' ' and ai_gameboard[co[0] + 1][co[1]] != 'S'):
            prob[co[0] + 1][co[1]] += 1
            if(co[0] - 1 == pc[0]):
                prob[co[0] + 1][co[1]] += 8
    except IndexError:
        if(co[0] - 1 == pc[0]):
            for i in reversed(range(pc[0])):
                if(ai_gameboard[i][co[1]] != 'X'):
                    prob[i][co[1]] += 8
                    break
    try:
        if(ai_gameboard[co[0]][co[1] - 1] != 'X' and ai_gameboard[co[0]][co[1] - 1] != ' ' and ai_gameboard[co[0]][co[1] - 1] != 'S'):
            prob[co[0]][co[1] - 1] += 1
            if(co[1] + 1 == pc[1]):
                prob[co[0]][co[1] - 1] += 8
    except IndexError: 
        pass
    try:
        if(ai_gameboard[co[0]][co[1] + 1] != 'X' and ai_gameboard[co[0]][co[1] + 1] != ' ' and ai_gameboard[co[0]][co[1] + 1] != 'S'):
            prob[co[0]][co[1] + 1] += 1
            if(co[1] - 1 == pc[1]):
                prob[co[0]][co[1] + 1] += 8
    except IndexError:
        if(co[1] - 1 == pc[1]):
            for i in reversed(range(pc[1])):
                if(ai_gameboard[co[0]][i] != 'X'):
                    prob[co[0]][i] += 8
                    break

    try:
        if((ai_gameboard[co[0] - 1][co[1]] == 'X' and ai_gameboard[co[0] + 1][co[1]] == ' ' and ai_gameboard[co[0]][co[1]] == 'X') or (ai_gameboard[co[0] - 1][co[1]] == ' ' and ai_gameboard[co[0] + 1][co[1]] == 'X' and ai_gameboard[co[0]][co[1]] == 'X') or (ai_gameboard[co[0]][co[1] - 1] == 'X' and ai_gameboard[co[0]][co[1] + 1] == ' ' and ai_gameboard[co[0]][co[1]] == 'X') or (ai_gameboard[co[0]][co[1] - 1] == ' ' and ai_gameboard[co[0]][co[1] + 1] == 'X' and ai_gameboard[co[0]][co[1]] == 'X')):
            if(ct == 0):
                if(co[0] + 1 == pc[0]):
                    flag = 1
                    while ai_gameboard[co[0] + flag][co[1]] != '░':
                        prev_coords = [co[0], co[1]]
                        co = [co[0] + flag, co[1]]
                        coords = [co[0], co[1]]
                elif(co[0] - 1 == pc[0]):
                    flag = 1
                    while ai_gameboard[co[0] - flag][co[1]] != '░':
                        prev_coords = [co[0], co[1]]
                        co = [co[0] - flag, co[1]]
                        coords = [co[0], co[1]]
                elif(co[1] - 1 == pc[1]):
                    flag = 1
                    while ai_gameboard[co[0]][co[1] - flag] != '░':
                        prev_coords = [co[0], co[1]]
                        co = [co[0], co[1] - flag]
                        coords = [co[0], co[1]]
                elif(co[1] + 1 == pc[1]):
                    flag = 1
                    while ai_gameboard[co[0]][co[1] + flag] != '░':
                        prev_coords = [co[0], co[1]]
                        co = [co[0], co[1] + flag]
                        coords = [co[0], co[1]]
                
                probability_board_hunting(prev_coords, co, prob, ct + 1)              
    except IndexError:
        pass
            
    if(np.max(prob) == 0):
        pb = sum(playerboard, [])
        index = [i for i in range(len(pb)) if(pb[i]) == 'X']
        choose = rd.randint(0, len(index) - 1)
        nco = [index[choose] // 10, index[choose] % 10]
        
        probability_board_hunting(co, nco, prob, ct) 
    
    return np.max(prob)

def ai_shooting(): #finds squares with highest probability and chooses randomly between them
    
    global mode, prev_coords, first_coords, coords
    probability = [[0] * 10 for i in range(10)]
    if(mode == 'targeting'):
        
        maxprobability = probability_board_targeting(player_ships_remaining, probability, 0)
        props = sum(probability, [])
        index = [i for i in range(len(props)) if(props[i]) == maxprobability]
        choose = rd.randint(0, len(index) - 1)
        
        if(check_hit(index[choose] // 10, index[choose] % 10, playerboard)):
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = 'X'
            playerboard[index[choose] // 10][index[choose] % 10] = 'X'
            
            if(check_sink(playerboard, ai_gameboard, player_ships_remaining, player_placement)):
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nI sunk a boat!')
                time.sleep(.8)
                print('\n=======================================')
                
                pbs = sum(ai_gameboard, [])
                if('X' in pbs):
                    mode = 'hunting'
                    idx = [i for i in range(len(pbs)) if(pbs[i]) == 'X']
                    ch = rd.randint(0, len(index) - 1)
                    coords = [idx[ch] // 10, idx[ch] % 10]
                else:
                    mode = 'targeting'
            
            else:
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nIt\'s a hit!')
                time.sleep(.8)
                print('\n=======================================')
                
                mode = 'hunting'
                coords = [index[choose] // 10, index[choose] % 10]
            
            prev_coords = [index[choose] // 10, index[choose] % 10]
        else:
            for i in range(3):
                time.sleep(.8)
                print("...")
            print('\nI missed.')
            time.sleep(.8)
            print('\n=======================================')
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = ' '
            playerboard[index[choose] // 10][index[choose] % 10] = ' '
        
        print('\nYour board')
        print_board(playerboard)
        
    elif(mode == 'hunting'):
        
        maxprobability = probability_board_hunting(prev_coords, coords, probability, 0)
        props = sum(probability, [])
        index = [i for i in range(len(props)) if(props[i]) == maxprobability]
        choose = rd.randint(0, len(index) - 1)
        if(check_hit(index[choose] // 10, index[choose] % 10, playerboard)):
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = 'X'
            playerboard[index[choose] // 10][index[choose] % 10] = 'X'
            
            if(check_sink(playerboard, ai_gameboard, player_ships_remaining, player_placement)):
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nI sunk a boat!')
                time.sleep(.8)
                print('\n=======================================')
                pbs = sum(ai_gameboard, [])
                if('X' in pbs):
                    mode = 'hunting'
                    idx = [i for i in range(len(pbs)) if(pbs[i]) == 'X']
                    ch = rd.randint(0, len(idx) - 1)
                    print(idx, ch)
                    coords = [idx[ch] // 10, idx[ch] % 10]
                else:
                    mode = 'targeting'
            
            else:
                for i in range(3):
                    time.sleep(.8)
                    print("...")
                print('\nIt\'s a hit!')
                time.sleep(.8)
                print('\n=======================================')
                
                mode = 'hunting'
                prev_coords = [coords[0], coords[1]]
                coords = [index[choose] // 10, index[choose] % 10]
        
        else:
            for i in range(3):
                time.sleep(.8)
                print("...")
            print('\nI missed.')
            time.sleep(.8)
            print('\n=======================================')
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = ' '
            playerboard[index[choose] // 10][index[choose] % 10] = ' '
            
        print('\nYour board')
        print_board(playerboard)

def pregame(): #pregame set up(choosing mode, how many ships, ship placement)
    print('\n=======================================')
    print('\nLet\'s play BattleShips')
    print('\n=======================================')
    
    Flag = True
    while Flag:
        nship = input('Enter how many ships you would like to place [1-9]: ')
        print('\n=======================================')
        if(nship not in [str(i) for i in range(1,10)]):
            print('\nEnter a number from 1 to 9.')
            print('\n=======================================')
        else:
            Flag = False            
    
    global numship
    numship = [int(i) for i in range(1, int(nship) + 1)]
    global numship2
    numship2 = c.deepcopy(numship)

    global setting
    setting = input("Would you like to play against an AI or another player?\n"
                    " 1) Player vs player\n"
                    " 2) Player vs Ai\n\n")
    print('\n=======================================')
    while setting not in ['1', '2']:
        setting = input('Invalid input. Would you like to play against an AI or another person?\n'
                        ' 1) for player vs player\n'
                        ' 2) for player vs Ai\n\n')
        print('\n=======================================')
    num_player(int(setting))
    instructions()
    
    global name 
    name = []
    if(setting == '2'):
        name.append(input("Enter your name: "))
        print('\n=======================================')
        print("\nIt's time to set up your ship, " + name[0] + ". Please keep in mind:\n\n"
              " - Ships will be places based on their orientation\n"
              " - Horizontal ships will be placed relative to the left-most square\n"
              " - Vertical ships will be placed relative to the right-most square\n"
              " - Ships can not extend beyond the border and can not cross-over other ships")
        input("Press enter to continue")
        print('\n=======================================')
        
        ai_ship_placement(len(numship), 0)
        while len(numship) != 0:
            placement_info(numship, playerboard)
    else:
        for i in range(2):
            for j in range(35):
                print('\n')
            name.append(input('Enter player ' + str(i + 1) + '\'s name: '))
            print('\n=======================================')
            print("\nIt's time to set up your ship, " + name[i] + ". Please keep in mind:\n\n"
                  " - Ships will be places based on their orientation\n"
                  " - Horizontal ships will be placed relative to the left-most square\n"
                  " - Vertical ships will be placed relative to the right-most square\n"
                  " - Ships can not extend beyond the border and can not cross-over other ships")
            input("Press enter to continue")
            print('\n=======================================')
    
            if(i == 0):
                while len(numship) != 0:
                    placement_info(numship, playerboard1)
            else:
                while len(numship2) != 0:
                    placement_info(numship2, playerboard2)

pregame()

if(setting == '1'):
    for j in range(35):
        print('\n')
    print('\nBefore starting, I will flip a coin to see who will go first:')
    for i in range(3):
        time.sleep(.8)
        print("...")
    
    if(rd.randint(0, 1) == 0): #player 1 goes first
        print('\n' + name[0] + ' gets to go first.')
        time.sleep(2)
        print('\n=======================================')
        while len(player1_ships_remaining) != 0 and len(player2_ships_remaining) != 0:
            print('\n' + name[0] + ' turn.')
            player_shooting(main_gameboard1, playerboard2, player2_ships_remaining, player2_placements)
            if(len(player1_ships_remaining) == 0 or len(player2_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
            print('\n' + name[1] + '\'s turn.')
            player_shooting(main_gameboard2, playerboard1, player1_ships_remaining, player1_placement)
            if(len(player2_ships_remaining) == 0 or len(player1_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
        if(len(player1_ships_remaining) == 0):
            print('\n\nCongratulations, ' + name[0] + ', you have sunk all of ' + name[1] + '\'s ships!')
        elif(len(player2_ships_remaining) == 0):
            print('\n\nCongratulations, ' + name[1] + ', you have sunk all of ' + name[0] + '\'s ships!')
    else:
        print('\n' + name[1] + ' gets to go first.')
        time.sleep(2)
        print('\n=======================================')
        while len(player2_ships_remaining) != 0 and len(player1_ships_remaining) != 0:
            print('\n' + name[1] + '\'s turn.')
            player_shooting(main_gameboard2, playerboard1, player1_ships_remaining, player1_placement)
            if(len(player2_ships_remaining) == 0 or len(player1_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
            print('\n' + name[0] + ' turn.')
            player_shooting(main_gameboard1, playerboard2, player2_ships_remaining, player2_placements)
            if(len(player1_ships_remaining) == 0 or len(player2_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
        if(len(player2_ships_remaining) == 0):
            print('\n\nCongratulations, ' + name[0] + ', you have sunk all of ' + name[1] + '\'s ships!')
        elif(len(player1_ships_remaining) == 0):
            print('\n\nCongratulations, ' + name[1] + ', you have sunk all of ' + name[0] + '\'s ships!')
elif(setting == '2'):
    print('\nBefore starting, I will flip a coin to see who will go first:')
    for i in range(3):
        time.sleep(.8)
        print("...")
    
    if(rd.randint(0, 1) == 0): #player goes first
        print('\nYou get to go first.')
        time.sleep(2)
        print('\n=======================================')
        while len(player_ships_remaining) != 0 and len(ai_ships_remaining) != 0:
            print('\nYour turn.')
            player_shooting(player_gameboard, ai_board, ai_ships_remaining, ai_placement)
            if(len(player_ships_remaining) == 0 or len(ai_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
            print('\nMy turn.\n')
            ai_shooting()
            input("Press enter to continue")
            print('\n=======================================')
        
        if(len(player_ships_remaining) == 0):
            print('\nYou lose, ' + name[0] + '. I have sunk all of your ships.')
        elif(len(ai_ships_remaining) == 0):
            print('\nYou won! \n\nCongratulations, ' + name[0] + ', you have sunk all of my ships!')
    else:
        print('\nI get to go first.')
        time.sleep(2)
        print('\n=======================================')
        while len(player_ships_remaining) != 0 and len(ai_ships_remaining) != 0:
            print('\nMy turn.')
            ai_shooting()
            if(len(player_ships_remaining) == 0 or len(ai_ships_remaining) == 0):
                break
            input("Press enter to continue")
            print('\n=======================================')
            print('\nYour turn.')
            player_shooting(player_gameboard, ai_board, ai_ships_remaining, ai_placement)
            input("Press enter to continue")
            print('\n=======================================')
        
        if(len(player_ships_remaining) == 0):
            print('\nYou lose, ' + name[0] + '. I have sunk all of your ships.')
        elif(len(ai_ships_remaining) == 0):
            print('\nYou won! \n\nCongratulations, ' + name[0] + ', you have sunk all of my ships!')