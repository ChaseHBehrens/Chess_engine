import random, copy
board = [[0 for x in range(3)] for y in range(3)]
turn = True

def possible_moves(b):
    l = []
    for y in range(3):
        for x in range(3):
            if b[y][x] == 0:
                l.append([x,y])
    return l

def win(b):
    for i in range(3):
        if (b[i][0] == 1 and b[i][1] == 1 and b[i][2] == 1) or (b[0][i] == 1 and b[1][i] == 1 and b[2][i] == 1):
            return 1
        if (b[i][0] == -1 and b[i][1] == -1 and b[i][2] == -1) or (b[0][i] == -1 and b[1][i] == -1 and b[2][i] == -1):
            return -1
    if (b[0][0] == 1 and b[1][1] == 1 and b[2][2] == 1) or (b[2][0] == 1 and b[1][1] == 1 and b[0][2] == 1):
        return 1
    if (b[0][0] == -1 and b[1][1] == -1 and b[2][2] == -1) or (b[2][0] == -1 and b[1][1] == -1 and b[0][2] == -1):
        return -1
    if len(possible_moves(b)) == 0:
        return 0
    return ''

def move(b,t,index):
    if t:
        b[possible_moves(b)[index][1]][possible_moves(b)[index][0]] = 1
    else:
        b[possible_moves(b)[index][1]][possible_moves(b)[index][0]] = -1
    return b

def display():
    for y in range(3):
        string = ''
        for x in range(3):
            if board[y][x] == 1:
                string += 'X'
            elif board[y][x] == -1:
                string += 'O'
            else:
                string += ' '
            if x < 2:
                string += '|'
        print(string)
        if y < 2:
            print('-----')
    print(win(board))
display()


def brain(b, t, depth, alpha=-100000, beta=100000):
    if depth < 100:
        if win(b) != '':
            return win(b) - (depth / 10)
        else:
            if t:  
                for i in range(len(possible_moves(b))):
                    alpha = max(alpha, brain(move(copy.deepcopy(b), t, i), (not t), (depth + 1), alpha, beta))
                    if alpha >= beta:
                        break
                return alpha
            else: 
                for i in range(len(possible_moves(b))):
                    beta = min(beta, brain(move(copy.deepcopy(b), t, i), (not t), (depth + 1), alpha, beta))
                    if beta <= alpha:
                        break
                return beta
    else:
        return 0

        


running = True
while running:

    if turn:
        '''
        n = int(input())
        board = move(copy.deepcopy(board),turn,n)
        display()
        '''
        evaluations = []
        for i in range(len(possible_moves(board))):
            evaluations.append(brain(move(copy.deepcopy(board),turn,i),(not turn),0))
        board = move(copy.deepcopy(board),turn,evaluations.index(max(evaluations)))
        display()
        
    else:
        evaluations = []
        for i in range(len(possible_moves(board))):
            evaluations.append(brain(move(copy.deepcopy(board),turn,i),(not turn),0))
        board = move(copy.deepcopy(board),turn,evaluations.index(min(evaluations)))
        display()
    
    if win(board) != '':
        
        board = [[0 for x in range(3)] for y in range(3)]
        display()
        turn = False
        
        #running = False
    turn = not turn
