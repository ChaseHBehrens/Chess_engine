import pygame, os, chess


game_type = int(input(f'1:Play Both{os.linesep}2:Play White{os.linesep}3:Play Black{os.linesep}4:Bot vs Bot{os.linesep}'))
if game_type == 1:
    turn_key = [True,False]
elif game_type == 2:
    turn_key = [True]
elif game_type == 3:
    turn_key = [False]
elif game_type == 4:
    turn_key = []

running = True
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

def agrobot(color):
    key = {'None':0,'P':10,'N':30,'B':30,'R':50,'Q':90,'K':0,'p':-10,'n':-30,'b':-30,'r':-50,'q':-90,'k':0}

    if color:
        location = [chess.square_file(board.king(chess.BLACK)),chess.square_rank(board.king(chess.BLACK))]
    else:
        location = [chess.square_file(board.king(chess.WHITE)),chess.square_rank(board.king(chess.WHITE))]

    evaluation = 0
    for x in range(8):
        for y in range(8):
            if x != location[0] and y != location[1]:
                evaluation += key[str(board.piece_at(chess.square(x,y)))]/((((location[0]-x)**2)+((location[1]-y)**2))**0.5)

    return evaluation

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
            evaluations.append(agrobot(turn))
            board.pop()
        if turn:
            board.push(chess.Move.from_uci(str(list(board.legal_moves)[evaluations.index(max(evaluations))])))
        else:
            board.push(chess.Move.from_uci(str(list(board.legal_moves)[evaluations.index(min(evaluations))])))
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
