import pygame
import random
import time
import keyboard
import math
import os
import threading

screen=pygame.display.set_mode([600, 600])
screen.fill([255, 255, 255])
white_king = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_king.png'),[75,75])
black_king = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_king.png'),[75,75])
white_queen = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_queen.png'),[75,75])
black_queen = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_queen.png'),[75,75])
white_rook = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_rook.png'),[75,75])
black_rook = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_rook.png'),[75,75])
white_bishop = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_bishop.png'),[75,75])
black_bishop = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_bishop.png'),[75,75])
white_knight = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_knight.png'),[75,75])
black_knight = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_knight.png'),[75,75])
white_pawn = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_pawn.png'),[75,75])
black_pawn = pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_pawn.png'),[75,75])

side = 1
display = 1
result = ''
en_passant = 9
castling = [0,0,0,0]
in_check = []
turn = 1
move_choice = []
moves = []
board = [[-4,-2,-3,-5,-6,-3,-2,-4],
        [-1,-1,-1,-1,-1,-1,-1,-1],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [4,2,3,5,6,3,2,4]]

game = [board]
evaluations = []
evaluate = []
non_sigmoid = []

def key_check():
    global side
    global display
    while True:
        pygame.event.get()
        if keyboard.is_pressed('esc'):
            os._exit(1)
        if keyboard.is_pressed('shift'):
            side *= -1
        if keyboard.is_pressed('space'):
            display *= -1
        while keyboard.is_pressed('space') or keyboard.is_pressed('shift'):
            time.sleep(0.01)
        time.sleep(0.1) 
thread = threading.Thread(target=key_check)
thread.start()


def draw():
    global board
    global side
    if side == -1:
        b = [[board[7-j][7-i] for i in range(8)] for j in range(8)]
    if side == 1:
        b = [[board[j][i] for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen,[238,238,210],[i*75,j*75,75,75],0)
            else:
                pygame.draw.rect(screen,[118,150,86],[i*75,j*75,75,75],0)
            if b[j][i] == 6:
                screen.blit(white_king, [i*75,j*75])
            if b[j][i] == -6:
                screen.blit(black_king, [i*75,j*75])
            if b[j][i] == 5:
                screen.blit(white_queen, [i*75,j*75])
            if b[j][i] == -5:
                screen.blit(black_queen, [i*75,j*75])
            if b[j][i] == 4:
                screen.blit(white_rook, [i*75,j*75])
            if b[j][i] == -4:
                screen.blit(black_rook, [i*75,j*75])
            if b[j][i] == 3:
                screen.blit(white_bishop, [i*75,j*75])
            if b[j][i] == -3:
                screen.blit(black_bishop, [i*75,j*75])
            if b[j][i] == 2:
                screen.blit(white_knight, [i*75,j*75])
            if b[j][i] == -2:
                screen.blit(black_knight, [i*75,j*75])
            if b[j][i] == 1:
                screen.blit(white_pawn, [i*75,j*75])
            if b[j][i] == -1:
                screen.blit(black_pawn, [i*75,j*75])
    pygame.display.flip()

def new_game():
    global result
    global en_passant
    global casling
    global in_check
    global turn
    global moves
    global board
    global game
    global weights
    global bias
    global evaluations
    global non_sigmoid
    result = ''
    en_passant = 9
    castling = [0,0,0,0]
    in_check = []
    turn = 1
    moves = []
    board = [[-4,-2,-3,-5,-6,-3,-2,-4],
             [-1,-1,-1,-1,-1,-1,-1,-1],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [1,1,1,1,1,1,1,1],
             [4,2,3,5,6,3,2,4]]
    game = [board]
    evaluations = []
    evaluate = []
    non_sigmoid = []
    draw()

    bias = [line.strip().split(',') for line in open(r'C:\Users\chase\OneDrive\Desktop\chess engine\bias.txt')]
    bias = [[float(bias[j][i]) for i in range(len(bias[j]))] for j in range(len(bias))]
    w1 = [line.strip().split(',') for line in open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights1.txt')]
    w2 = [line.strip().split(',') for line in open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights2.txt')]
    w3 = [line.strip().split(',') for line in open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights3.txt')]
    w4 = [line.strip().split(',') for line in open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights4.txt')]
    weights = []
    weights.append([[float(w1[j][i]) for i in range(len(w1[j]))] for j in range(len(w1))])
    weights.append([[float(w2[j][i]) for i in range(len(w2[j]))] for j in range(len(w2))])
    weights.append([[float(w3[j][i]) for i in range(len(w3[j]))] for j in range(len(w3))])
    weights.append([[float(w4[j][i]) for i in range(len(w4[j]))] for j in range(len(w4))])
    
    
def move(m):
    global board
    board2 = [[board[j][i] for i in range(8)] for j in range(8)]
    board2[m[1][0]][m[1][1]] = board[m[0][0]][m[0][1]]
    board2[m[0][0]][m[0][1]] = 0
    
    if len(m) == 3:
        if m[2]>0:
            if m[2] == 9:
                board2[3][en_passant] = 0
            else:
                board2[m[1][0]][m[1][1]] = m[2]
        if m[2]<0:
            if m[2] == -9:
                board2[4][en_passant] = 0
            else:
                board2[m[1][0]][m[1][1]] = m[2]
    if len(m) == 4:
        board2[m[3][0]][m[3][1]] = board[m[2][0]][m[2][1]]
        board2[m[2][0]][m[2][1]] = 0
        
    return board2

def check(t,a,b):
    global in_check
    if t == 1:
        for i in range(8):
            for j in range(8):
                if a[i][j] == 6:
                    if i<7 and j<6 and a[i+1][j+2] == -2: 
                        in_check.append(b)
                    if i<7 and j>2 and a[i+1][j-2] == -2: 
                        in_check.append(b)
                    if i>0 and j<6 and a[i-1][j+2] == -2: 
                        in_check.append(b)
                    if i>0 and j>2 and a[i-1][j-2] == -2: 
                        in_check.append(b)
                    if i<6 and j<7 and a[i+2][j+1] == -2: 
                        in_check.append(b)
                    if i<6 and j>0 and a[i+2][j-1] == -2:
                        in_check.append(b)
                    if i>2 and j<7 and a[i-2][j+1] == -2: 
                        in_check.append(b)
                    if i>2 and j>0 and a[i-2][j-1] == -2:
                        in_check.append(b)

                    if i!=7:
                        if a[i+1][j] == -6:
                            in_check.append(b)
                    if i!=0:
                        if a[i-1][j] == -6:
                            in_check.append(b)
                    if j!=7:
                        if a[i][j+1] == -6:
                            in_check.append(b)
                    if j!=0:
                        if a[i][j-1] == -6:
                            in_check.append(b)
                    if i!=7 and j!=7:
                        if a[i+1][j+1] == -6:
                            in_check.append(b)
                    if i!=0 and j!=0:
                        if a[i-1][j-1] == -6 or a[i-1][j-1] == -1:
                            in_check.append(b)
                    if i!=0 and j!=7:
                        if a[i-1][j+1] == -6 or a[i-1][j+1] == -1:
                            in_check.append(b)
                    if i!=7 and j!=0:
                        if a[i+1][j-1] == -6:
                            in_check.append(b)

                    for x in range(min(i,j)):
                        if a[(i-x)-1][(j-x)-1] != 0:
                            if a[(i-x)-1][(j-x)-1] == -5 or a[(i-x)-1][(j-x)-1] == -3:
                                in_check.append(b)
                            break
                    for x in range(min(7-i,7-j)):
                        if a[(i+x)+1][(j+x)+1] != 0:
                            if a[(i+x)+1][(j+x)+1] == -5 or a[(i+x)+1][(j+x)+1] == -3:
                                in_check.append(b)
                            break
                    for x in range(min(7-i,j)):
                        if a[(i+x)+1][(j-x)-1] != 0:
                            if a[(i+x)+1][(j-x)-1] == -5 or a[(i+x)+1][(j-x)-1] == -3:
                                in_check.append(b)
                            break
                    for x in range(min(i,7-j)):
                        if a[(i-x)-1][(j+x)+1] != 0:
                            if a[(i-x)-1][(j+x)+1] == -5 or a[(i-x)-1][(j+x)+1] == -3:
                                in_check.append(b)
                            break
                    for x in range(i):
                        if a[(i-x)-1][j] != 0:
                            if a[(i-x)-1][j] == -5 or a[(i-x)-1][j] == -4:
                                in_check.append(b)
                            break
                    for x in range(7-i):
                        if a[(i+x)+1][j] != 0:
                            if a[(i+x)+1][j] == -5 or a[(i+x)+1][j] == -4:
                                in_check.append(b)
                            break
                    for x in range(j):
                        if a[i][(j-x)-1] != 0:
                            if a[i][(j-x)-1] == -5 or a[i][(j-x)-1] == -4:
                                in_check.append(b)
                            break
                    for x in range(7-j):
                        if a[i][(j+x)+1] != 0:
                            if a[i][(j+x)+1] == -5 or a[i][(j+x)+1] == -4:
                                in_check.append(b)
                            break

    if t == -1:
        for i in range(8):
            for j in range(8):
                if a[i][j] == -6:
                    if i<7 and j<6 and a[i+1][j+2] == 2: 
                        in_check.append(b)
                    if i<7 and j>2 and a[i+1][j-2] == 2: 
                        in_check.append(b)
                    if i>0 and j<6 and a[i-1][j+2] == 2: 
                        in_check.append(b)
                    if i>0 and j>2 and a[i-1][j-2] == 2: 
                        in_check.append(b)
                    if i<6 and j<7 and a[i+2][j+1] == 2: 
                        in_check.append(b)
                    if i<6 and j>0 and a[i+2][j-1] == 2:
                        in_check.append(b)
                    if i>2 and j<7 and a[i-2][j+1] == 2: 
                        in_check.append(b)
                    if i>2 and j>0 and a[i-2][j-1] == 2:
                        in_check.append(b)

                    if i!=7:
                        if a[i+1][j] == 6:
                            in_check.append(b)
                    if i!=0:
                        if a[i-1][j] == 6:
                            in_check.append(b)
                    if j!=7:
                        if a[i][j+1] == 6:
                            in_check.append(b)
                    if j!=0:
                        if a[i][j-1] == 6:
                            in_check.append(b)
                    if i!=7 and j!=7:
                        if a[i+1][j+1] == 6 or a[i+1][j+1] == 1:
                            in_check.append(b)
                    if i!=0 and j!=0:
                        if a[i-1][j-1] == 6:
                            in_check.append(b)
                    if i!=0 and j!=7:
                        if a[i-1][j+1] == 6:
                            in_check.append(b)
                    if i!=7 and j!=0:
                        if a[i+1][j-1] == 6 or a[i+1][j-1] == 1:
                            in_check.append(b)

                    for x in range(min(i,j)):
                        if a[(i-x)-1][(j-x)-1] != 0:
                            if a[(i-x)-1][(j-x)-1] == 5 or a[(i-x)-1][(j-x)-1] == 3:
                                in_check.append(b)
                            break
                    for x in range(min(7-i,7-j)):
                        if a[(i+x)+1][(j+x)+1] != 0:
                            if a[(i+x)+1][(j+x)+1] == 5 or a[(i+x)+1][(j+x)+1] == 3:
                                in_check.append(b)
                            break
                    for x in range(min(7-i,j)):
                        if a[(i+x)+1][(j-x)-1] != 0:
                            if a[(i+x)+1][(j-x)-1] == 5 or a[(i+x)+1][(j-x)-1] == 3:
                                in_check.append(b)
                            break
                    for x in range(min(i,7-j)):
                        if a[(i-x)-1][(j+x)+1] != 0:
                            if a[(i-x)-1][(j+x)+1] == 5 or a[(i-x)-1][(j+x)+1] == 3:
                                in_check.append(b)
                            break
                    for x in range(i):
                        if a[(i-x)-1][j] != 0:
                            if a[(i-x)-1][j] == 5 or a[(i-x)-1][j] == 4:
                                in_check.append(b)
                            break
                    for x in range(7-i):
                        if a[(i+x)+1][j] != 0:
                            if a[(i+x)+1][j] == 5 or a[(i+x)+1][j] == 4:
                                in_check.append(b)
                            break
                    for x in range(j):
                        if a[i][(j-x)-1] != 0:
                            if a[i][(j-x)-1] == 5 or a[i][(j-x)-1] == 4:
                                in_check.append(b)
                            break
                    for x in range(7-j):
                        if a[i][(j+x)+1] != 0:
                            if a[i][(j+x)+1] == 5 or a[i][(j+x)+1] == 4:
                                in_check.append(b)
                            break

def move_calculator(t):
    global in_check
    global en_passant
    global castling
    global moves
    moves = []
    if t == 1:
        for i in range(8):
            for j in range(8):
                if board[i][j] == 2:
                    if i<7 and j<6 and board[i+1][j+2]<1: 
                        moves.append([[i,j],[i+1,j+2]])
                    if i<7 and j>2 and board[i+1][j-2]<1: 
                        moves.append([[i,j],[i+1,j-2]])
                    if i>0 and j<6 and board[i-1][j+2]<1: 
                        moves.append([[i,j],[i-1,j+2]])
                    if i>0 and j>2 and board[i-1][j-2]<1: 
                        moves.append([[i,j],[i-1,j-2]])
                    if i<6 and j<7 and board[i+2][j+1]<1: 
                        moves.append([[i,j],[i+2,j+1]])
                    if i<6 and j>0 and board[i+2][j-1]<1:
                        moves.append([[i,j],[i+2,j-1]])
                    if i>2 and j<7 and board[i-2][j+1]<1: 
                        moves.append([[i,j],[i-2,j+1]])
                    if i>2 and j>0 and board[i-2][j-1]<1:
                        moves.append([[i,j],[i-2,j-1]])
                if board[i][j] == 4:
                    for x in range(i):
                        if board[(i-x)-1][j] != 0:
                            if board[(i-x)-1][j]<0:
                                moves.append([[i,j],[(i-x)-1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,j]])
                    for x in range(7-i):
                        if board[(i+x)+1][j] != 0:
                            if board[(i+x)+1][j]<0:
                                moves.append([[i,j],[(i+x)+1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,j]])
                    for x in range(j):
                        if board[i][(j-x)-1] != 0:
                            if board[i][(j-x)-1]<0:
                                moves.append([[i,j],[i,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j-x)-1]])
                    for x in range(7-j):
                        if board[i][(j+x)+1] != 0:
                            if board[i][(j+x)+1]<0:
                                moves.append([[i,j],[i,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j+x)+1]])
                if board[i][j] == 3:
                    for x in range(min(i,j)):
                        if board[(i-x)-1][(j-x)-1] != 0:
                            if board[(i-x)-1][(j-x)-1]<0:
                                moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                    for x in range(min(7-i,7-j)):
                        if board[(i+x)+1][(j+x)+1] != 0:
                            if board[(i+x)+1][(j+x)+1]<0:
                                moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                    for x in range(min(7-i,j)):
                        if board[(i+x)+1][(j-x)-1] != 0:
                            if board[(i+x)+1][(j-x)-1]<0:
                                moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                    for x in range(min(i,7-j)):
                        if board[(i-x)-1][(j+x)+1] != 0:
                            if board[(i-x)-1][(j+x)+1]<0:
                                moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                if board[i][j] == 5:
                    for x in range(min(i,j)):
                        if board[(i-x)-1][(j-x)-1] != 0:
                            if board[(i-x)-1][(j-x)-1]<0:
                                moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                    for x in range(min(7-i,7-j)):
                        if board[(i+x)+1][(j+x)+1] != 0:
                            if board[(i+x)+1][(j+x)+1]<0:
                                moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                    for x in range(min(7-i,j)):
                        if board[(i+x)+1][(j-x)-1] != 0:
                            if board[(i+x)+1][(j-x)-1]<0:
                                moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                    for x in range(min(i,7-j)):
                        if board[(i-x)-1][(j+x)+1] != 0:
                            if board[(i-x)-1][(j+x)+1]<0:
                                moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                    for x in range(i):
                        if board[(i-x)-1][j] != 0:
                            if board[(i-x)-1][j]<0:
                                moves.append([[i,j],[(i-x)-1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,j]])
                    for x in range(7-i):
                        if board[(i+x)+1][j] != 0:
                            if board[(i+x)+1][j]<0:
                                moves.append([[i,j],[(i+x)+1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,j]])
                    for x in range(j):
                        if board[i][(j-x)-1] != 0:
                            if board[i][(j-x)-1]<0:
                                moves.append([[i,j],[i,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j-x)-1]])
                    for x in range(7-j):
                        if board[i][(j+x)+1] != 0:
                            if board[i][(j+x)+1]<0:
                                moves.append([[i,j],[i,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j+x)+1]])
                if board[i][j] == 1:
                    if board[i-1][j] == 0:
                        if i == 1:
                            moves.append([[i,j],[i-1,j],2])
                            moves.append([[i,j],[i-1,j],3])
                            moves.append([[i,j],[i-1,j],4])
                            moves.append([[i,j],[i-1,j],5])
                        else:
                            moves.append([[i,j],[i-1,j]])
                            if i == 6 and board[i-2][j] == 0:
                                moves.append([[i,j],[i-2,j]])
                    if j>0:
                        if board[i-1][j-1]<0:
                            if i>1:
                                moves.append([[i,j],[i-1,j-1]])
                            else:
                                moves.append([[i,j],[i-1,j-1],2])
                                moves.append([[i,j],[i-1,j-1],3])
                                moves.append([[i,j],[i-1,j-1],4])
                                moves.append([[i,j],[i-1,j-1],5])
                    if j<7:
                        if board[i-1][j+1]<0:
                            if i>1:
                                moves.append([[i,j],[i-1,j+1]])
                            else:
                                moves.append([[i,j],[i-1,j+1],2])
                                moves.append([[i,j],[i-1,j+1],3])
                                moves.append([[i,j],[i-1,j+1],4])
                                moves.append([[i,j],[i-1,j+1],5])
                    if i == 3:
                        if en_passant == j+1:
                            moves.append([[i,j],[i-1,j+1],9])
                        if en_passant == j-1:
                            moves.append([[i,j],[i-1,j-1],9])
                if board[i][j] == 6:
                    if i!=7:
                        if board[i+1][j]<1:
                            moves.append([[i,j],[i+1,j]])
                    if i!=0:
                        if board[i-1][j]<1:
                            moves.append([[i,j],[i-1,j]])
                    if j!=7:
                        if board[i][j+1]<1:
                            moves.append([[i,j],[i,j+1]])
                    if j!=0:
                        if board[i][j-1]<1:
                            moves.append([[i,j],[i,j-1]])
                    if i!=7 and j!=7:
                        if board[i+1][j+1]<1:
                            moves.append([[i,j],[i+1,j+1]])
                    if i!=0 and j!=0:
                        if board[i-1][j-1]<1:
                            moves.append([[i,j],[i-1,j-1]])
                    if i!=0 and j!=7:
                        if board[i-1][j+1]<1:
                            moves.append([[i,j],[i-1,j+1]])
                    if i!=7 and j!=0:
                        if board[i+1][j-1]<1:
                            moves.append([[i,j],[i+1,j-1]])

        in_check = []
        check(1,board,0)
        check(1,move([[7,4],[7,3]]),0)
        if in_check == []:
            if castling[0] == 0 and board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
                moves.append([[7,4],[7,2],[7,0],[7,3]])
        in_check = []
        check(1,board,0)
        check(1,move([[7,4],[7,5]]),0)
        if in_check == []:
            if castling[1] == 0 and board[7][5] == 0 and board[7][6] == 0:
                moves.append([[7,4],[7,6],[7,7],[7,5]])

        in_check = []
        for i in range(len(moves)):
            check(1,move(moves[i]),moves[i])
        for i in range(len(in_check)):
            try:
                moves.remove(in_check[i])
            except:
                pass
            
            
                    
    if t == -1:
        for i in range(8):
            for j in range(8):
                if board[i][j] == -2:
                    if i<7 and j<6 and board[i+1][j+2]>-1: 
                        moves.append([[i,j],[i+1,j+2]])
                    if i<7 and j>2 and board[i+1][j-2]>-1: 
                        moves.append([[i,j],[i+1,j-2]])
                    if i>0 and j<6 and board[i-1][j+2]>-1: 
                        moves.append([[i,j],[i-1,j+2]])
                    if i>0 and j>2 and board[i-1][j-2]>-1: 
                        moves.append([[i,j],[i-1,j-2]])
                    if i<6 and j<7 and board[i+2][j+1]>-1: 
                        moves.append([[i,j],[i+2,j+1]])
                    if i<6 and j>0 and board[i+2][j-1]>-1:
                        moves.append([[i,j],[i+2,j-1]])
                    if i>2 and j<7 and board[i-2][j+1]>-1: 
                        moves.append([[i,j],[i-2,j+1]])
                    if i>2 and j>0 and board[i-2][j-1]>-1:
                        moves.append([[i,j],[i-2,j-1]])
                if board[i][j] == -4:
                    for x in range(i):
                        if board[(i-x)-1][j] != 0:
                            if board[(i-x)-1][j]>0:
                                moves.append([[i,j],[(i-x)-1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,j]])
                    for x in range(7-i):
                        if board[(i+x)+1][j] != 0:
                            if board[(i+x)+1][j]>0:
                                moves.append([[i,j],[(i+x)+1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,j]])
                    for x in range(j):
                        if board[i][(j-x)-1] != 0:
                            if board[i][(j-x)-1]>0:
                                moves.append([[i,j],[i,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j-x)-1]])
                    for x in range(7-j):
                        if board[i][(j+x)+1] != 0:
                            if board[i][(j+x)+1]>0:
                                moves.append([[i,j],[i,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j+x)+1]])
                if board[i][j] == -3:
                    for x in range(min(i,j)):
                        if board[(i-x)-1][(j-x)-1] != 0:
                            if board[(i-x)-1][(j-x)-1]>0:
                                moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                    for x in range(min(7-i,7-j)):
                        if board[(i+x)+1][(j+x)+1] != 0:
                            if board[(i+x)+1][(j+x)+1]>0:
                                moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                    for x in range(min(7-i,j)):
                        if board[(i+x)+1][(j-x)-1] != 0:
                            if board[(i+x)+1][(j-x)-1]>0:
                                moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                    for x in range(min(i,7-j)):
                        if board[(i-x)-1][(j+x)+1] != 0:
                            if board[(i-x)-1][(j+x)+1]>0:
                                moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                if board[i][j] == -5:
                    for x in range(min(i,j)):
                        if board[(i-x)-1][(j-x)-1] != 0:
                            if board[(i-x)-1][(j-x)-1]>0:
                                moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j-x)-1]])
                    for x in range(min(7-i,7-j)):
                        if board[(i+x)+1][(j+x)+1] != 0:
                            if board[(i+x)+1][(j+x)+1]>0:
                                moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j+x)+1]])
                    for x in range(min(7-i,j)):
                        if board[(i+x)+1][(j-x)-1] != 0:
                            if board[(i+x)+1][(j-x)-1]>0:
                                moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,(j-x)-1]])
                    for x in range(min(i,7-j)):
                        if board[(i-x)-1][(j+x)+1] != 0:
                            if board[(i-x)-1][(j+x)+1]>0:
                                moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,(j+x)+1]])
                    for x in range(i):
                        if board[(i-x)-1][j] != 0:
                            if board[(i-x)-1][j]>0:
                                moves.append([[i,j],[(i-x)-1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i-x)-1,j]])
                    for x in range(7-i):
                        if board[(i+x)+1][j] != 0:
                            if board[(i+x)+1][j]>0:
                                moves.append([[i,j],[(i+x)+1,j]])
                            break
                        else:
                            moves.append([[i,j],[(i+x)+1,j]])
                    for x in range(j):
                        if board[i][(j-x)-1] != 0:
                            if board[i][(j-x)-1]>0:
                                moves.append([[i,j],[i,(j-x)-1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j-x)-1]])
                    for x in range(7-j):
                        if board[i][(j+x)+1] != 0:
                            if board[i][(j+x)+1]>0:
                                moves.append([[i,j],[i,(j+x)+1]])
                            break
                        else:
                            moves.append([[i,j],[i,(j+x)+1]])
                if board[i][j] == -1:
                    if board[i+1][j] == 0:
                        if i == 6:
                            moves.append([[i,j],[i+1,j],-2])
                            moves.append([[i,j],[i+1,j],-3])
                            moves.append([[i,j],[i+1,j],-4])
                            moves.append([[i,j],[i+1,j],-5])
                        else:
                            moves.append([[i,j],[i+1,j]])
                            if i == 1 and board[i+2][j] == 0:
                                moves.append([[i,j],[i+2,j]])
                    if j>0:
                        if board[i+1][j-1]>0:
                            if i<6:
                                moves.append([[i,j],[i+1,j-1]])
                            else:
                                moves.append([[i,j],[i+1,j-1],-2])
                                moves.append([[i,j],[i+1,j-1],-3])
                                moves.append([[i,j],[i+1,j-1],-4])
                                moves.append([[i,j],[i+1,j-1],-5])
                        
                    if j<7:
                        if board[i+1][j+1]>0:
                            if i<6:
                                moves.append([[i,j],[i+1,j+1]])
                            else:
                                moves.append([[i,j],[i+1,j+1],-2])
                                moves.append([[i,j],[i+1,j+1],-3])
                                moves.append([[i,j],[i+1,j+1],-4])
                                moves.append([[i,j],[i+1,j+1],-5])
                    if i == 4:
                        if en_passant == j+1:
                            moves.append([[i,j],[i+1,j+1],-9])
                        if en_passant == j-1:
                            moves.append([[i,j],[i+1,j-1],-9])
                    
                if board[i][j] == -6:
                    if i!=7:
                        if board[i+1][j]>-1:
                            moves.append([[i,j],[i+1,j]])
                    if i!=0:
                        if board[i-1][j]>-1:
                            moves.append([[i,j],[i-1,j]])
                    if j!=7:
                        if board[i][j+1]>-1:
                            moves.append([[i,j],[i,j+1]])
                    if j!=0:
                        if board[i][j-1]>-1:
                            moves.append([[i,j],[i,j-1]])
                    if i!=7 and j!=7:
                        if board[i+1][j+1]>-1:
                            moves.append([[i,j],[i+1,j+1]])
                    if i!=0 and j!=0:
                        if board[i-1][j-1]>-1:
                            moves.append([[i,j],[i-1,j-1]])
                    if i!=0 and j!=7:
                        if board[i-1][j+1]>-1:
                            moves.append([[i,j],[i-1,j+1]])
                    if i!=7 and j!=0:
                        if board[i+1][j-1]>-1:
                            moves.append([[i,j],[i+1,j-1]])

        in_check = []
        check(-1,board,0)
        check(-1,move([[0,4],[0,3]]),0)
        if in_check == []:
            if castling[2] == 0 and board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
                moves.append([[0,4],[0,2],[0,0],[0,3]])
        in_check = []
        check(-1,board,0)
        check(-1,move([[0,4],[0,5]]),0)
        if in_check == []:
            if castling[3] == 0 and board[0][5] == 0 and board[0][6] == 0:
                moves.append([[0,4],[0,6],[0,7],[0,5]])

        in_check = []
        for i in range(len(moves)):
            check(-1,move(moves[i]),moves[i])
        for i in range(len(in_check)):
            try:
                moves.remove(in_check[i])
            except:
                pass

def sigmoid(n):
    #n = (n*10)-5
    return 1/(1+math.exp(-n))
def d_sigmoid(n):
    n = (n*10)-5
    return (1/(1+math.exp(-n)))*(1-(1/(1+math.exp(-n))))
    
    
def engine(m,t):
    global weights
    global bias
    global evaluate
    global non_sigmoid

    x = [[(t/2)+0.5],[],[],[],[]]
    y = [[(t/2)+0.5],[],[],[],[]]
    for i in range(8):
        for j in range(8):
            x[0].append((m[i][j]+6)*0.0833)
            y[0].append((m[i][j]+6)*0.0833)

    for i in range(4):
        for j in range(len(weights[i])):
            y[i+1].append(((sum([weights[i][j][l] * x[i][l] for l in range(len(weights[i][j]))])+bias[i][j])/(sum(x[i])+1)))
            x[i+1].append(sigmoid(y[i+1][j]))
            
    
    non_sigmoid.append(y)
    evaluate.append(x)
    
    return x[4][0]

def set_base():
    b = [[random.randint(0,10000)/10000 for i in range(100)] for j in range(3)]
    b.append([random.randint(0,10000)/10000])
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\bias.txt','w').writelines([str(b[i])[1:len(str(b[i]))-1]+'\n' for i in range(len(b))])
    w1 = [[random.randint(0,10000)/10000 for i in range(65)] for j in range(100)]
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights1.txt','w').writelines([str(w1[i])[1:len(str(w1[i]))-1]+'\n' for i in range(len(w1))])
    w2 = [[random.randint(0,10000)/10000 for i in range(100)] for j in range(100)]
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights2.txt','w').writelines([str(w2[i])[1:len(str(w2[i]))-1]+'\n' for i in range(len(w2))])
    w3 = [[random.randint(0,10000)/10000 for i in range(100)] for j in range(100)]
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights3.txt','w').writelines([str(w3[i])[1:len(str(w3[i]))-1]+'\n' for i in range(len(w3))])
    w4 = [[random.randint(0,10000)/10000 for i in range(100)] for j in range(1)]
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights4.txt','w').writelines([str(w4[i])[1:len(str(w4[i]))-1]+'\n' for i in range(len(w4))])
set_base()
def update_weights():
    global bias
    global weights
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\bias.txt','w').writelines([str(bias[i])[1:len(str(bias[i]))-1]+'\n' for i in range(len(bias))])
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights1.txt','w').writelines([str(weights[0][i])[1:len(str(weights[0][i]))-1]+'\n' for i in range(len(weights[0]))])
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights2.txt','w').writelines([str(weights[1][i])[1:len(str(weights[1][i]))-1]+'\n' for i in range(len(weights[1]))])
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights3.txt','w').writelines([str(weights[2][i])[1:len(str(weights[2][i]))-1]+'\n' for i in range(len(weights[2]))])
    open(r'C:\Users\chase\OneDrive\Desktop\chess engine\weights4.txt','w').writelines([str(weights[3][i])[1:len(str(weights[3][i]))-1]+'\n' for i in range(len(weights[3]))])

#############################################################################################################################################################################################

def backpropagate(s,s2):
    global weights
    global bias
    global turn
    global game
    global evaluations
    global non_sigmoid
    
    
    evals = []
    nonsigmoid = []
    
    for l in range(len(evaluations)):
        if l%2 == 0:
            evals.append([[evaluations[l][i][j] for j in range(len(evaluations[l][i]))] for i in range(len(evaluations[l]))])
            nonsigmoid.append([[non_sigmoid[l][i][j] for j in range(len(evaluations[l][i]))] for i in range(len(evaluations[l]))])


    change_to_weight = [[[0 for l in range(len(weights[i][j]))] for j in range(len(weights[i]))] for i in range(len(weights))]
    change_to_bias = [[0 for j in range(len(bias[i]))] for i in range(len(bias))]
    
    for l in range(len(evals)):
        gradiant = ([[0 for o in range(len(evals[l][k]))] for k in range(4)])
        gradiant.append([2*(evals[l][4][0]-s)])
        #print(evals[l][4][0])
        bias_gradiant = ([[0 for o in range(len(evals[l][k]))] for k in range(4)])
        bias_gradiant.append([2*(evals[l][4][0]-s)])
        
        for k in range(4):
            for i in range(len(evals[l][4-k])): 
                for j in range(len(evals[l][3-k])):
                    gradiant[3-k][j] += gradiant[4-k][i]*weights[3-k][i][j]*d_sigmoid(nonsigmoid[l][4-k][i])
                    bias_gradiant[3-k][j] += bias_gradiant[4-k][i]*d_sigmoid(nonsigmoid[l][4-k][i])
                    change_to_weight[3-k][i][j] += gradiant[4-k][i]*evals[l][3-k][j]*d_sigmoid(nonsigmoid[l][4-k][i])
                change_to_bias[3-k][i] += bias_gradiant[4-k][i]*d_sigmoid(nonsigmoid[l][4-k][i])


    evals = []
    nonsigmoid = []

    for l in range(len(evaluations)):
        if l%2 != 0:
            evals.append([[evaluations[l][i][j] for j in range(len(evaluations[l][i]))] for i in range(len(evaluations[l]))])
            nonsigmoid.append([[non_sigmoid[l][i][j] for j in range(len(evaluations[l][i]))] for i in range(len(evaluations[l]))])

    for l in range(len(evals)):
        gradiant = ([[0 for o in range(len(evals[l][k]))] for k in range(4)])
        gradiant.append([2*(evals[l][4][0]-s2)])
        bias_gradiant = ([[0 for o in range(len(evals[l][k]))] for k in range(4)])
        bias_gradiant.append([2*(evals[l][4][0]-s2)])
        
        for k in range(4):
            for i in range(len(evals[l][4-k])): 
                for j in range(len(evals[l][3-k])):
                    gradiant[3-k][j] += gradiant[4-k][i]*weights[3-k][i][j]*d_sigmoid(nonsigmoid[l][4-k][i])
                    bias_gradiant[3-k][j] += bias_gradiant[4-k][i]*d_sigmoid(nonsigmoid[l][4-k][i])
                    change_to_weight[3-k][i][j] += gradiant[4-k][i]*evals[l][3-k][j]*d_sigmoid(nonsigmoid[l][4-k][i])
                change_to_bias[3-k][i] += bias_gradiant[4-k][i]*d_sigmoid(nonsigmoid[l][4-k][i])


    
    for i in range(len(change_to_weight)):
        for j in range(len(change_to_weight[i])):
            for l in range(len(change_to_weight[i][j])):
                change_to_weight[i][j][l] /= len(game)
                change_to_weight[i][j][l] *= 1.5
    for i in range(len(change_to_bias)):
        for j in range(len(change_to_bias[i])):
            change_to_bias[i][j] /= len(game)
            change_to_bias[i][j] *= 1.5


    for i in range(len(weights)):
        for j in range(len(weights[i])):
            for l in range(len(weights[i][j])):
                weights[i][j][l] += change_to_weight[i][j][l]
    for i in range(len(bias)):
        for j in range(len(bias[i])):
            bias[i][j] += change_to_bias[i][j]

    for i in range(len(weights)):
        for j in range(len(weights[i])):
            for l in range(len(weights[i][j])):
                weights[i][j][l] = round(weights[i][j][l],5)
                if weights[i][j][l]<0:
                    weights[i][j][l] = 0
                if weights[i][j][l]>1:
                    weights[i][j][l] = 1
    for i in range(len(bias)):
        for j in range(len(bias[i])):
            bias[i][j] = round(bias[i][j],5)
            if bias[i][j]<0:
                bias[i][j] = 0
            if bias[i][j]>1:
                bias[i][j] = 1
              
    update_weights()     
    

#############################################################################################################################################################################################

def score(m,r):
    peices = 0
    v = {1:1,-1:1,2:3,-2:3,3:3,-3:3,4:5,-4:5,5:9,-5:9,6:10,-6:10}
    for i in range(8):
        for j in range(8):
            if r == 1:
                if board[i][j]<0:
                    peices += v[board[i][j]]
            if r == -1:
                if board[i][j]>0:
                    peices += v[board[i][j]]

    peices = (peices/49)*0.4
    p = ((5-(m[move_choice[1][0]][move_choice[1][1]]))/4)*0.1

    if r == 1:
        return 0.5+(peices+p)
    if r == -1:
        return 0.5-(peices+p)
    
                    

def play_turn(t):
    global board
    global turn
    global en_passant
    global castling
    global result
    global moves
    global in_check
    global game
    global move_choice
    global evaluations
    move_calculator(t)
    if len(moves) == 0:
        in_check = []
        check(t,board,0)
        if len(in_check)>0:
            if t == 1:
                result = -1
            if t == -1:
                result = 1
        else:
            result = 0
        return

    e = []
    for i in range(len(moves)):
        e.append(engine(move(moves[i]),turn))
    if t == 1:
        evaluations.append(evaluate[e.index(max(e))])
        move_choice = moves[e.index(max(e))]
    if t == -1:
        evaluations.append(evaluate[e.index(min(e))])
        move_choice = moves[e.index(min(e))]
    board = move(move_choice)
    if display == 1:
        draw()
    
    if t == 1:
        if move_choice[0][0] == 6 and move_choice[1][0] == 4 and board[move_choice[0][0]][move_choice[0][1]] == 1:
            en_passant = a[0][1]
        else:
            en_passant = 9
        if board[7][4] == 0:
            castling[0] = 1
            castling[1] = 1
        if board[7][0] == 0:
            castling[0] = 1
        if board[7][7] == 0:
            castling[1] = 1
    if t == -1:
        if move_choice[0][0] == 1 and move_choice[1][0] == 3 and board[move_choice[0][0]][move_choice[0][1]] == -1:
            en_passant = a[0][1]
        else:
            en_passant = 9
        if board[0][4] == 0:
            castling[2] = 1
            castling[3] = 1
        if board[0][0] == 0:
            castling[2] = 1
        if board[0][7] == 0:
            castling[3] = 1
    
    game.append(board)
    if game.count(board) == 3:
        result = 0
        return
    
    w = []
    b = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != 6 and board[i][j] != -6:
                if board[i][j] > 0:
                    w.append(board[i][j])
                if board[i][j] < 0:
                    b.append(abs(board[i][j]))
    if 1 not in w and 1 not in b:
        if sum(w)<4 and sum(b)<4:
            result = 0
            return        

    turn *= -1


while True:
    new_game()
    while result == '':
        play_turn(turn)
        if display == 1:
            time.sleep(0.5)
    
    if result == 0:
        backpropagate(0.25,0.75)
    if result == 1:
        backpropagate(score(game[len(game)-1],1),1)
    if result == -1:
        backpropagate(0,score(game[len(game)-1],-1))
    
