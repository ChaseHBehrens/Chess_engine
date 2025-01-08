import chess.pgn, pygame, time, os
import tensorflow as tf

game_type = int(input(f'1:Play Both{os.linesep}2:Play White{os.linesep}3:Play Black{os.linesep}4:Bot vs Bot{os.linesep}'))
if game_type == 1:
    turn_key = [True,False]
elif game_type == 2:
    turn_key = [True]
elif game_type == 3:
    turn_key = [False]
elif game_type == 4:
    turn_key = []

try:
    running = True
    model = tf.keras.models.load_model(r'C:\Users\chase\OneDrive\Desktop\chess engine\Network Files')
except:
    running = False

key = {0:'P',1:'N',2:'B',3:'R',4:'Q',5:'K',6:'p',7:'n',8:'b',9:'r',10:'q',11:'k'}
def generate_input(color):
    global board
    if color:
        inputs = [1 if str(board.piece_at(chess.square(i%64,0))) == key[i//64] else 0 for i in range(768)]     
    else:
        inputs = [1 if str(board.piece_at(chess.square(i%64,0))) == key[i//64] else 0 for i in range(767,-1,-1)]
    return inputs

board = chess.Board()
pygame.init()
screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
selection = False
if game_type == 3:
    flip = 1
else:
    flip = 0

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

def draw():
    global board,flip
    x = 7*flip
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen,[238,238,210],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            else:
                pygame.draw.rect(screen,[118,150,86],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            if str(board)[(i*2)+(j*16)] != '.':
                screen.blit(pieces[str(board)[(i*2)+(j*16)]], [abs(x-i)*75,abs(x-j)*75])
    if selection:
        pygame.draw.rect(screen,[0,200,200],[selection[0]*75,selection[1]*75,75,75],3)
    pygame.display.flip()

draw()
turn = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if flip == 1:
                    flip = 0
                else:
                    flip = 1
                selection = [7-selection[0],7-selection[1]]
                draw()
    if turn in turn_key:
        if pygame.mouse.get_pressed()[0]:
            try:
                board.push_san((chr(97+abs(selection[0]-(flip*7)))+str(abs(selection[1]+((flip*2)-1)+((flip-1)*7))))+(chr(97+abs((pygame.mouse.get_pos()[0]//75)-(flip*7)))+str(abs((pygame.mouse.get_pos()[1]//75)+((flip*2)-1)+((flip-1)*7)))))
                turn = not turn
            except:
                pass
            selection = [pygame.mouse.get_pos()[0]//75,pygame.mouse.get_pos()[1]//75]
            draw()
    else:
        evaluations = []
        for move in board.legal_moves:
            board.push(move)
            evaluations.append(model.predict([generate_input(turn)],verbose = 0)[0][0])
            board.pop()
        board.push(chess.Move.from_uci(str(list(board.legal_moves)[evaluations.index(max(evaluations))])))
        if flip == 1:
            selection = [7-(board.peek().to_square%8),board.peek().to_square//8]
        else:
            selection = [board.peek().to_square%8,7-(board.peek().to_square//8)]
        draw()
        turn = not turn
        
    if not board.legal_moves:
        running = False
    clock.tick(5)
    
pygame.quit()
