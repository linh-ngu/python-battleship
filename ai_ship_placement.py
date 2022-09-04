import random as rd

nums = ['0','1','2','3','4','5','6','7','8','9']

def generate():
    global board
    global possible
    board = [['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░'], ['░', '░', '░', '░', '░', '░', '░', '░', '░', '░']]
    possible = [[] for i in range(9)]

def ppossible(shipl, counter):
 
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
    possible[counter] = [x for x in possible[counter] if valid(x[2], x[0], x[1], shipl, board)]
    
    #randomly chooses the position of the ship
    choose = rd.randint(0, len(possible[counter]) - 1)        
    
    #placing down ship on the board
    for j in range(len(possible[counter])):
        if(possible[counter][choose][2] == 'h'):
            for k in range(shipl):
                board[possible[counter][choose][0]][possible[counter][choose][1] + k] = shipl
        elif(possible[counter][choose][2] == 'v'):
            for k in range(shipl):
                board[possible[counter][choose][0] + k][possible[counter][choose][1]] = shipl
    
    #continues onto the next ship
    ppossible(shipl - 1, counter + 1)

def valid(ori, r, c, s, pb):
    temp = []
    if ori == 'h':
        for i in range(c, c + s):
            if(pb[r][i] == '░'):
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

def aiboard():
    print('\n=======================================')
    print('')
    for i in range(len(board)):
        print(nums[i], end = '   ')
        for j in range(len(board[i])):
            print(board[i][j], end = '  ')
        print('')
    print('\n    A  B  C  D  E  F  G  H  I  J')
    print('\n=======================================')


generate()
ppossible(9, 0)
aiboard()