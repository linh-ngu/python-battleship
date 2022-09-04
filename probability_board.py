import random as rd
import numpy as np

possible = [[] for i in range(9)]
playerboard = [['9','9','9','9','9','9','9','9','9','░'], ['8','░','░','7','7','7','7','7','7','7'], ['8','░','░','░','░','░','░','░','6','░'], ['8','░','░','░','░','░','░','░','6','░'], ['8','░','░','░','1','2','░','░','6','░'], ['8','░','3','3','3','2','░','░','6','░'], ['8','░','5','5','5','5','5','░','6','4'], ['8','░','░','░','░','░','░','░','6','4'], ['8','░','░','░','░','░','░','░','░','4'], ['░','░','░','░','░','░','░','░','░','4']]
player_placement = {1:[4,4,'h'], 2:[4,5,'v'], 3:[5,2,'h'], 4:[6,9,'v'], 5:[6,2,'h'], 6:[2,8,'v'], 7:[1,3,'h'], 8:[1,0,'v'], 9:[0,0,'h']}
ai_board = [(['░'] * 10) for i in range(10)]
ai_gameboard = [(['░'] * 10) for i in range(10)]
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
player_ships_remaining = [9,8,7,6,5,4,3,2,1]
mode = 'targeting'
coords = [0, 1]
first_coords = [0, 1]
prev_coords = [0,1]

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

def check_hit(r,c, mg2): #checks if shot hit ship
    if(mg2[r][c] != '░'):
        return True
    else:
        return False
    
def print_board(pb): #prints inputed board
    print('')
    for i in range(len(pb)):
        print(nums[i], end = '   ')
        for j in range(len(pb[i])):
            print(pb[i][j], end = '  ')
        print('')
    print('\n    A  B  C  D  E  F  G  H  I  J')
    print('\n=======================================')

def probability_board_targeting(ships, prob, counter):
    if(counter == len(player_ships_remaining)):
        return np.max(prob)
    for i in range(10):
        for j in range(10):
            if(j + ships[counter] <= 10 and check_placement('h', i, j, ships[counter], ai_gameboard)): #horizontal
                for k in range(ships[counter]):
                    prob[i][j + k] += 1
            
            if(i + ships[counter] <= 10 and check_placement('v', i, j, ships[counter], ai_gameboard)): #vertical 
                for k in range(ships[counter]):
                    prob[i + k][j] += 1
                           
    return probability_board_targeting(ships, prob, counter + 1)

def probability_board_hunting(coords, prob, player_ships_remaining, fc, ct, pc):
    try:
        if(ai_gameboard[coords[0] - 1][coords[1]] != 'X' and ai_gameboard[coords[0] - 1][coords[1]] != ' ' and ai_gameboard[coords[0] - 1][coords[1]] != 'S'):
            prob[coords[0] - 1][coords[1]] += 1
            if(coords[0] - 1 == pc[0]):
                prob[coords[0] - 1][coords[1]] += 1
    except IndexError:
        pass
    try:
        if(ai_gameboard[coords[0] + 1][coords[1]] != 'X' and ai_gameboard[coords[0] + 1][coords[1]] != ' ' and ai_gameboard[coords[0] + 1][coords[1]] != 'S'):
            prob[coords[0] + 1][coords[1]] += 1
            if(coords[0] + 1 == pc[0]):
                prob[coords[0] + 1][coords[1]] += 1
    except IndexError:
        pass
    try:
        if(ai_gameboard[coords[0]][coords[1] - 1] != 'X' and ai_gameboard[coords[0]][coords[1] - 1] != ' ' and ai_gameboard[coords[0]][coords[1] - 1] != 'S'):
            prob[coords[0]][coords[1] - 1] += 1
            if(coords[1] - 1 == pc[1]):
                prob[coords[0]][coords[1] - 1] += 1
    except IndexError: 
        pass
    try:
        if(ai_gameboard[coords[0]][coords[1] + 1] != 'X' and ai_gameboard[coords[0]][coords[1] + 1] != ' ' and ai_gameboard[coords[0]][coords[1] + 1] != 'S'):
            prob[coords[0]][coords[1] + 1] += 1
            if(coords[1] + 1 == pc[1]):
                prob[coords[0]][coords[1] + 1] += 1
    except IndexError:
        pass
    
    pc[0] = coords[0]
    pc[1] = coords[1]
    
    print_board(prob)
    
    if(check_sink(playerboard, ai_gameboard) or len(player_ships_remaining) == 0):
        return np.max(prob)
    
    if(np.max(prob) == 0):
        if(ct == 0):
            probability_board_hunting(fc, prob, player_ships_remaining, fc, ct + 1, pc)
        else:
            pb = sum(playerboard, [])
            index = [i for i in range(len(pb)) if(pb[i]) == 'X']
            choose = rd.randint(0, len(index) - 1)
            nfc = [index[choose] // 10, index[choose] % 10, playerboard]
            probability_board_hunting(nfc, prob, player_ships_remaining, fc, ct, pc)
            print_board(prob)
    
    return np.max(prob)

def ai_shooting(fc): #finds squares with highest probability and chooses randomly between them
    global mode
    probability = [[0] * 10 for i in range(10)]
    
    if(mode == 'targeting'):
        
        maxprobability = probability_board_targeting(player_ships_remaining, probability, 0)
        props = sum(probability, [])
        index = [i for i in range(len(props)) if(props[i]) == maxprobability]
        choose = rd.randint(0, len(index) - 1)
        if(check_hit(index[choose] // 10, index[choose] % 10, playerboard)):
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = 'X'
            playerboard[index[choose] // 10][index[choose] % 10] = 'X'
            
            if(check_sink(playerboard, ai_gameboard)):
                pbs = sum(ai_gameboard, [])
                if('X' in pbs):
                    mode = 'hunting'
                    idx = [i for i in range(len(pbs)) if(pbs[i]) == 'X']
                    ch = rd.randint(0, len(index) - 1)
                    coords = [idx[ch] // 10, idx[ch] % 10, playerboard]
                else:
                    mode = 'targeting'
                print('\nYou sunk a boat!')
                print('\n=======================================')
            else:
                mode = 'hunting'
                coords = [index[choose] // 10, index[choose] % 10]
                print('\nIt\'s a hit!')
                print('\n=======================================')
            
            global prev_coords
            first_coords[0] = index[choose] // 10
            first_coords[1] = index[choose] % 10
            prev_coords[0] = index[choose] // 10
            prev_coords[1] = index[choose] % 10

            print_board(ai_gameboard)
        else:
            
            print('\nI missed.')
            print('\n=======================================')
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = ' '
            playerboard[index[choose] // 10][index[choose] % 10] = ' '
            
            print_board(ai_gameboard)
            
    elif(mode == 'hunting'):
        print(prev_coords)
        maxprobability = probability_board_hunting(coords, probability, player_ships_remaining, fc, 0, prev_coords)
        props = sum(probability, [])
        index = [i for i in range(len(props)) if(props[i]) == maxprobability]
        choose = rd.randint(0, len(index) - 1)
        
        if(check_hit(index[choose] // 10, index[choose] % 10, playerboard)):
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = 'X'
            playerboard[index[choose] // 10][index[choose] % 10] = 'X'
            
            if(check_sink(playerboard, ai_gameboard)):
                pbs = sum(ai_gameboard, [])
                if('X' in pbs):
                    mode = 'hunting'
                    idx = [i for i in range(len(pbs)) if(pbs[i]) == 'X']
                    ch = rd.randint(0, len(index) - 1)
                    coords = [idx[ch] // 10, idx[ch] % 10, playerboard]
                else:
                    mode = 'targeting'
                print('\nYou sunk a boat!')
                print('\n=======================================')
            else:
                mode = 'hunting'
                coords = [index[choose] // 10, index[choose] % 10]
                print('\nIt\'s a hit!')
                print('\n=======================================')
          
            print_board(ai_gameboard)
        else:
            print('\nI missed.')
            print('\n=======================================')
            
            ai_gameboard[index[choose] // 10][index[choose] % 10] = ' '
            playerboard[index[choose] // 10][index[choose] % 10] = ' '
            
            print_board(ai_gameboard)

def check_sink(pb, opb):
    global mode
    pbs = sum(pb, [])
    for i in player_ships_remaining:
        if str(i) not in pbs:
            if(player_placement[i][2] == 'h'):
                for j in range(i):
                    pb[player_placement[i][0]][player_placement[i][1] + j] = 'S'
                    opb[player_placement[i][0]][player_placement[i][1] + j] = 'S'
            elif(player_placement[i][2] == 'v'):
                for j in range(i):
                    pb[player_placement[i][0] + j][player_placement[i][1]] = 'S'
                    opb[player_placement[i][0] + j][player_placement[i][1]] = 'S'
            player_placement.pop(i)
            player_ships_remaining.remove(i)
            return True


for i in range(55):
    print(i)
    print(mode)
    ai_shooting(first_coords)
    if(len(player_ships_remaining) == 0):
        print(i)
        break