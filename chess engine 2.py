import chess, pygame, threading, sys, random, time, os
from pygame.locals import *
pygame.init()
side = False
display = True
game_inputs = []
scores = []

screen=pygame.display.set_mode([600, 600])
screen.fill([255, 255, 255])

pieces = {'K':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_king.png'),[75,75]),
          'k':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_king.png'),[75,75]),
          'Q':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_queen.png'),[75,75]),
          'q':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_queen.png'),[75,75]),
          'R':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_rook.png'),[75,75]),
          'r':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_rook.png'),[75,75]),
          'B':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_bishop.png'),[75,75]),
          'b':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_bishop.png'),[75,75]),
          'N':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_knight.png'),[75,75]),
          'n':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_knight.png'),[75,75]),
          'P':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_pawn.png'),[75,75]),
          'p':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_pawn.png'),[75,75])}
input_key = {'K':1,
             'Q':0.83,
             'R':0.67,
             'B':0.5,
             'N':0.33,
             'P':0.17,
             '.':0,
             'p':-0.17,
             'n':-0.33,
             'b':-0.5,
             'r':-0.67,
             'q':-0.83,
             'k':-1}
input_key2 = {'K':0,
             'Q':9,
             'R':5,
             'B':3,
             'N':3,
             'P':1,
             '.':0,
             'p':-1,
             'n':-3,
             'b':-3,
             'r':-5,
             'q':-9,
             'k':0}
import tensorflow as tf
try:
    model = tf.keras.models.load_model(r'C:\Users\chase\OneDrive\Desktop\chess engine\Network Files')
except:
    print('could not load data')
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(65, input_shape=(65,), activation='relu'))
    model.add(tf.keras.layers.Dense(10000, activation='relu'))
    model.add(tf.keras.layers.Dense(10000, activation='relu'))
    model.add(tf.keras.layers.Dense(10000, activation='relu'))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
 

def draw():
    #time.sleep(0.3)
    global board, side
    screen.fill([0,0,0])
    x = 7*int(side)
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen,[238,238,210],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            else:
                pygame.draw.rect(screen,[118,150,86],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            
            if str(board)[(i*2)+(j*16)] != '.':
                screen.blit(pieces[str(board)[(i*2)+(j*16)]], [abs(x-i)*75,abs(x-j)*75])
    pygame.display.flip()

def new_game():
    global board, evaluations, display, game_inputs, scores
    board = chess.Board()
    game_inputs = []
    scores = []
    evaluations = []
    if display:
        draw()
new_game()

def generate_inputs():
    global board
    inputs = []
    for j in range(8):
        for i in range(8):
            inputs.append(input_key[str(board)[(i*2)+(j*16)]])
    if board.turn:
        inputs.append(1)
    else:
        inputs.append(-1)
    return inputs
def generate_scores():
    global board
    inputs = []
    for j in range(8):
        for i in range(8):
            inputs.append(input_key2[str(board)[(i*2)+(j*16)]])
    return sum(inputs)

def score():
    global board
    if str(board.outcome()).split(',')[1][8] == 'T':
        return 100
    if str(board.outcome()).split(',')[1][8] == 'F':
        return -100
    if str(board.outcome()).split(',')[1][8] == 'N':
        return sum(generate_inputs())*5
   
while True:
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RSHIFT or event.key == K_LSHIFT:
                if side:
                    side = False
                else:
                    side = True
            if event.key == K_SPACE:
                if display:
                    display = False
                else:
                    display = True
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    evals = [0 for i in range(len(list(board.legal_moves)))]
    for i in range(len(evals)):
        board.push(chess.Move.from_uci(str(list(board.legal_moves)[i])))
        evals[i] = model.predict([generate_inputs()],verbose = 0)[0][0]
        board.pop()
    if board.turn:
        evaluations.append(max(evals))
    else:
        evaluations.append(min(evals))
    if display:
        print(evaluations[-1])
        
    game_inputs.append(generate_inputs())
    scores.append(generate_scores())
    board.push(chess.Move.from_uci(str(list(board.legal_moves)[evals.index(evaluations[-1])])))
    if display:
        draw()
    else:
        '''
        pass
        '''
        screen.fill([0,0,0])
        pygame.display.flip()
        
    if board.outcome() or len(evaluations) == 75:
        x_train = [game_inputs[i] for i in range(len(evaluations)-1)]
        y_train = [[scores[i+1]] for i in range(len(evaluations)-1)]
        model.fit(x_train, y_train, epochs=5)
        time.sleep(1)
        tf.keras.models.save_model(model, r'C:\Users\chase\OneDrive\Desktop\chess engine\Network Files')
        time.sleep(1)
        new_game()
