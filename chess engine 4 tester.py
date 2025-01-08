import chess.pgn, pygame, time
import tensorflow as tf

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
rep = [0,0,0]

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
    global board
    x = 7*0
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen,[238,238,210],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            else:
                pygame.draw.rect(screen,[118,150,86],[abs(x-i)*75,abs(x-j)*75,75,75],0)
            if str(board)[(i*2)+(j*16)] != '.':
                screen.blit(pieces[str(board)[(i*2)+(j*16)]], [abs(x-i)*75,abs(x-j)*75])
    pygame.display.flip()

draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    evaluations = []
    for move in board.legal_moves:
        board.push(move)
        evaluations.append(model.predict([generate_input(True)],verbose = 0)[0][0])
        board.pop()
    rep.pop(0)
    rep.append(max(evaluations))
    if (rep[0] == rep[2]):
        evaluations[evaluations.index(max(evaluations))] = 0
    board.push(chess.Move.from_uci(str(list(board.legal_moves)[evaluations.index(max(evaluations))])))
    print('Max Evaluation:')
    print(max(evaluations))
    draw()
    evaluations = []
    for move in board.legal_moves:
        board.push(move)
        evaluations.append(model.predict([generate_input(False)],verbose = 0)[0][0])
        board.pop()
    board.push(chess.Move.from_uci(str(list(board.legal_moves)[evaluations.index(max(evaluations))])))
    print('Max Evaluation:')
    print(max(evaluations))
    draw()
    
    if not board.legal_moves:
        running = False


pygame.quit()
    
    
