import pygame, sys, subprocess, time, random, string, chess
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode([600, 600])
pygame.display.set_caption('BitBot2')
pygame.display.set_icon(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\red_king.png'))
flip = True
outcome = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\bitbot2_title.png')
shift = 20

piece_images = {'P':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_pawn.png'),[75,75]),
                'N':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_knight.png'),[75,75]),
                'B':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_bishop.png'),[75,75]),
                'R':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_rook.png'),[75,75]),
                'Q':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_queen.png'),[75,75]),
                'K':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_king.png'),[75,75]),
                'p':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_pawn.png'),[75,75]),
                'n':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_knight.png'),[75,75]),
                'b':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_bishop.png'),[75,75]),
                'r':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_rook.png'),[75,75]),
                'q':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_queen.png'),[75,75]),
                'k':pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_king.png'),[75,75])}

playwhite = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playwhite.png')
playblack = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playblack.png')
watchbot = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\watchbot.png')
playboth = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playboth.png')

screen.fill([245,219,195])
screen.blit(outcome, [79+shift,95])
screen.blit(playwhite, [190,290])
screen.blit(playblack, [190,370])
screen.blit(watchbot, [190,450])
screen.blit(playboth, [190,530])
pygame.display.flip()

def update(offset=0,mouse_position=64,selected=64,promotion=False):
    for i in range(64):
        if ((i+(i//8))%2) == 1:
            pygame.draw.rect(screen,[245,219,195],[(i%8)*75,((i//8)*75)-offset,75,75],0)
        else:
            pygame.draw.rect(screen,[187,87,70],[(i%8)*75,((i//8)*75)-offset,75,75],0)
    image = None
    for i, square in enumerate(chess.SQUARES):
        if board.piece_at(square):
            if i == selected:
                image = pygame.transform.scale(piece_images[str(board.piece_at(square))],[80,80])
            else:
                if flip:
                    if i == mouse_position:
                        screen.blit(pygame.transform.scale(piece_images[str(board.piece_at(square))],[80,80]), [((i%8)*75)-3,(525-((i//8)*75))-offset-3])
                    else:
                        screen.blit(piece_images[str(board.piece_at(square))], [(i%8)*75,(525-((i//8)*75))-offset])
                else:
                    if i == mouse_position:
                        screen.blit(pygame.transform.scale(piece_images[str(board.piece_at(square))],[80,80]), [522-((i%8)*75),((i//8)*75)-offset-3])
                    else:
                        screen.blit(piece_images[str(board.piece_at(square))], [525-((i%8)*75),((i//8)*75)-offset])
    if image and not promotion:
        screen.blit(image, [pygame.mouse.get_pos()[0]-37,pygame.mouse.get_pos()[1]-37])
    pygame.display.flip()

def start():
    global board, mode, shift, flip
    board = chess.Board()
    mode = [None,None]
    while mode[0] is None:
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pos()[0] > 190 and pygame.mouse.get_pos()[0] < 410:
                    if pygame.mouse.get_pos()[1] > 290 and pygame.mouse.get_pos()[1] < 350:
                        flip = True
                        mode = [False,True]
                    elif pygame.mouse.get_pos()[1] > 370 and pygame.mouse.get_pos()[1] < 430:
                        flip = False
                        mode = [True,False]
                    elif pygame.mouse.get_pos()[1] > 450 and pygame.mouse.get_pos()[1] < 510:
                        flip = True
                        mode = [False,False]
                    '''
                    elif pygame.mouse.get_pos()[1] > 530 and pygame.mouse.get_pos()[1] < 590:
                        flip = True
                        mode = [True,True]
                    '''
                        
        screen.fill([245,219,195])
        screen.blit(outcome, [79+shift,95])
        screen.blit(playwhite, [190,290])
        screen.blit(playblack, [190,370])
        screen.blit(watchbot, [190,450])
        #screen.blit(playboth, [190,530])
        if pygame.mouse.get_pos()[0] > 190 and pygame.mouse.get_pos()[0] < 410:
            if pygame.mouse.get_pos()[1] > 290 and pygame.mouse.get_pos()[1] < 350:
                screen.blit(pygame.transform.scale(playwhite,[224,63]), [187,289])
            elif pygame.mouse.get_pos()[1] > 370 and pygame.mouse.get_pos()[1] < 430:
                screen.blit(pygame.transform.scale(playblack,[224,63]), [187,369])
            elif pygame.mouse.get_pos()[1] > 450 and pygame.mouse.get_pos()[1] < 510:
                screen.blit(pygame.transform.scale(watchbot,[224,63]), [187,449])
            '''
            elif pygame.mouse.get_pos()[1] > 530 and pygame.mouse.get_pos()[1] < 590:
                screen.blit(pygame.transform.scale(playboth,[224,63]), [187,529])
            '''
        pygame.display.flip()
    for i in range(24):
        update(((23-i)*25))
        time.sleep(0.008)
    main()

def bitconvert():
    global board
    whitetype = {chess.PAWN:0,chess.KNIGHT:1,chess.BISHOP:2,chess.ROOK:3,chess.QUEEN:4,chess.KING:5}
    blacktype = {chess.PAWN:6,chess.KNIGHT:7,chess.BISHOP:8,chess.ROOK:9,chess.QUEEN:10,chess.KING:11}
    bitboard = ['0' for i in range(64*12)]
    for i, square in enumerate(chess.SQUARES):
        if board.piece_at(square):
            if board.piece_at(square).color == chess.WHITE:
                bitboard[i+(whitetype[board.piece_at(square).piece_type]*64)] = '1'
            if board.piece_at(square).color == chess.BLACK:
                bitboard[i+(blacktype[board.piece_at(square).piece_type]*64)] = '1'
    return ''.join(bitboard) + str(int(board.turn))

def promotion(start_position,end_position):
    global board, flip
    squares = []
    if board.turn:
        keys = ['Q','N','R','B']
    else:
        keys = ['q','n','r','b']
    while True:
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    flip = not flip
                    update(0,64,start_position[0]+(start_position[1]*8),True)
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_square in squares:
                    if squares.index(mouse_square) == 0:
                        return chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]),promotion=chess.QUEEN)
                    elif squares.index(mouse_square) == 1:
                        return chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]),promotion=chess.KNIGHT)
                    elif squares.index(mouse_square) == 2:
                        return chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]),promotion=chess.ROOK)
                    elif squares.index(mouse_square) == 3:
                        return chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]),promotion=chess.BISHOP)
        if flip:
            mouse_square = (((pygame.mouse.get_pos()[0]*8)//600)+(((pygame.mouse.get_pos()[1]*8)//600)*8))
        else:
            mouse_square = (((pygame.mouse.get_pos()[0]*8)//600)+(((pygame.mouse.get_pos()[1]*8)//600)*8))

        if board.turn:
            if flip:
                pygame.draw.rect(screen,[248,248,248],[end_position[0]*75,0,75,300],0)
                pygame.draw.rect(screen,[0,0,0],[end_position[0]*75,0,75,300],3)
                squares = [end_position[0]+(i*8) for i in range(4)]
            else:
                pygame.draw.rect(screen,[248,248,248],[(7-end_position[0])*75,300,75,300],0)
                pygame.draw.rect(screen,[0,0,0],[(7-end_position[0])*75,300,75,300],3)
                squares = [63-end_position[0]-(8*i) for i in range(4)]
        else:
            if flip:
                pygame.draw.rect(screen,[248,248,248],[end_position[0]*75,300,75,300],0)
                pygame.draw.rect(screen,[0,0,0],[end_position[0]*75,300,75,300],3)
                squares = [63-(7-end_position[0])-(8*i) for i in range(4)]
            else:
                pygame.draw.rect(screen,[248,248,248],[(7-end_position[0])*75,0,75,300],0)
                pygame.draw.rect(screen,[0,0,0],[(7-end_position[0])*75,0,75,300],3)
                squares = [(7-end_position[0])+(i*8) for i in range(4)]
        for i, square in enumerate(squares):
            if mouse_square == square:
                screen.blit(pygame.transform.scale(piece_images[keys[i]],[80,80]),[((square%8)*75)-2,((square//8)*75)-2])
            else:
                screen.blit(piece_images[keys[i]],[(square%8)*75,(square//8)*75])
        pygame.display.flip()

def main():
    global board, mode, flip, shift, outcome
    while not board.is_game_over():
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    flip = not flip
                    update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flip:
                    start_square = (((pygame.mouse.get_pos()[0]*8)//600)+((7-((pygame.mouse.get_pos()[1]*8)//600))*8))
                    start_position = [((pygame.mouse.get_pos()[0]*8)//600),(7-((pygame.mouse.get_pos()[1]*8)//600))]
                else:
                    start_square = ((7-((pygame.mouse.get_pos()[0]*8)//600))+(((pygame.mouse.get_pos()[1]*8)//600)*8))
                    start_position = [(7-((pygame.mouse.get_pos()[0]*8)//600)),((pygame.mouse.get_pos()[1]*8)//600)]
            if event.type == pygame.MOUSEBUTTONUP:
                if flip:
                    end_position = [((pygame.mouse.get_pos()[0]*8)//600),(7-((pygame.mouse.get_pos()[1]*8)//600))]
                else:
                    end_position = [(7-((pygame.mouse.get_pos()[0]*8)//600)),((pygame.mouse.get_pos()[1]*8)//600)]
                move = chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]))
                if move in board.legal_moves:
                    board.push(move)
                    if mode[0] and mode[1]:
                        flip = not flip
                        time.sleep(0.1)
                elif chess.Move(chess.square(start_position[0],start_position[1]),chess.square(end_position[0],end_position[1]),promotion=chess.QUEEN) in board.legal_moves:
                    board.push(promotion(start_position,end_position))
                    if mode[0] and mode[1]:
                        flip = not flip
                        time.sleep(0.1)
                update()
        if mode[int(board.turn)]:
            if flip:
                mouse_square = (((pygame.mouse.get_pos()[0]*8)//600)+((7-((pygame.mouse.get_pos()[1]*8)//600))*8))
            else:
                mouse_square = ((7-((pygame.mouse.get_pos()[0]*8)//600))+(((pygame.mouse.get_pos()[1]*8)//600)*8))
            if pygame.mouse.get_pressed()[0]:
                update(0,64,start_square)
            else:
                if mouse_square in set(move.from_square for move in board.legal_moves):
                    update(0,mouse_square)
                else:
                    update()          
        else:
            time.sleep(0.5)
            if not board.is_game_over():
                process = subprocess.Popen([r"C:\Users\chase\OneDrive\Desktop\chess engine\C\chess2.exe", bitconvert()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = str(process.communicate()[0].decode())
                move = ''
                for i, bit in enumerate(bitconvert()[:-1]):
                    if bit != output[i]:
                        move += (string.ascii_lowercase[(i%64)%8] + str(((i%64)//8)+1))
                board.push_san(move)
                update()

    time.sleep(0.5)
    shift = 0
    if board.outcome().winner == chess.WHITE:
        outcome = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_wins.png')
    elif board.outcome().winner == chess.BLACK:
        outcome = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_wins.png')
    else:
        outcome = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\draw.png')
    for i in range(24):
        pygame.draw.rect(screen,[245,219,195],[0,0,600,25*i],0)
        screen.blit(outcome, [79+shift,95-(600-(25*i))])
        screen.blit(playwhite, [190,290-(600-(25*i))])
        screen.blit(playblack, [190,370-(600-(25*i))])
        screen.blit(watchbot, [190,450-(600-(25*i))])
        screen.blit(playboth, [190,530-(600-(25*i))])
        pygame.display.flip()
        time.sleep(0.008)
    start()
start()
