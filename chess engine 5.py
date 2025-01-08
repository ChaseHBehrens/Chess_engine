import pygame, os, chess, chess.engine

stockfish = chess.engine.SimpleEngine.popen_uci(r'C:\Users\chase\OneDrive\Desktop\chess engine\stockfish\stockfish-windows-x86-64-avx2.exe')

running = True
board = chess.Board()
pygame.init()
screen = pygame.display.set_mode([620, 600])
clock = pygame.time.Clock()
selection = False
flip = 0
score = stockfish.analyse(board, chess.engine.Limit(time=2.0))['score']
turn = True

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

def extract_score():
    global board, score, turn
    if score.is_mate():
        if (turn and str(score)[14] == '+') or ((not turn) and str(score)[14] == '-'):
            score_value = 10000
        else:
            score_value = -10000
    else:
        if turn:
            score_value = int(score.relative.score())
        else:
            score_value = -1 * int(score.relative.score())
    return score_value

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

    offset = extract_score()
    pygame.draw.rect(screen, [0,0,0], [600,0,20,600], 0)
    pygame.draw.rect(screen, [250,250,250], [600,300-(offset//4),20,300+(offset//4)], 0)
    pygame.display.flip()

draw()
print(extract_score())
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

    if pygame.mouse.get_pressed()[0]:
        try:
            board.push_san((chr(97+abs(selection[0]-(flip*7)))+str(abs(selection[1]+((flip*2)-1)+((flip-1)*7))))+(chr(97+abs((pygame.mouse.get_pos()[0]//75)-(flip*7)))+str(abs((pygame.mouse.get_pos()[1]//75)+((flip*2)-1)+((flip-1)*7)))))
            turn = not turn
            score = stockfish.analyse(board, chess.engine.Limit(time=2.0))['score']
            print(extract_score())
        except:
            pass
        if pygame.mouse.get_pos()[0] < 600:
            selection = [pygame.mouse.get_pos()[0]//75,pygame.mouse.get_pos()[1]//75]
        draw()
    if not board.legal_moves:
        running = False
    clock.tick(5)

stockfish.quit()
pygame.quit()
