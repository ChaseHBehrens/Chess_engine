import pygame, sys, time
import subprocess
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode([600, 600])
pygame.display.set_caption('BitBot1')
pygame.display.set_icon(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\red_king.png'))

piece_images = [pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_pawn.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_knight.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_bishop.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_rook.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_queen.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\white_king.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_pawn.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_knight.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_bishop.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_rook.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_queen.png'),[75,75]),
                pygame.transform.scale(pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\black_king.png'),[75,75])]

pieces = [0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000,
          0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
          0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
          0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
          0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
          0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
          0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000,
          0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010,
          0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100,
          0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001,
          0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000,
          0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000]

playwhite = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playwhite.png')
playblack = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playblack.png')
watchbot = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\watchbot.png')
playboth = pygame.image.load(r'C:\Users\chase\OneDrive\Desktop\chess engine\playboth.png')


screen.fill([245,219,195])
screen.blit(playwhite, [190,150])
screen.blit(playblack, [190,230])
screen.blit(watchbot, [190,310])
screen.blit(playboth, [190,390])
pygame.display.flip()
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
                if pygame.mouse.get_pos()[1] > 150 and pygame.mouse.get_pos()[1] < 210:
                    flip = True
                    mode = [True,False]
                elif pygame.mouse.get_pos()[1] > 230 and pygame.mouse.get_pos()[1] < 290:
                    flip = False
                    mode = [False,True]
                elif pygame.mouse.get_pos()[1] > 310 and pygame.mouse.get_pos()[1] < 370:
                    flip = True
                    mode = [False,False]
                elif pygame.mouse.get_pos()[1] > 390 and pygame.mouse.get_pos()[1] < 450:
                    flip = True
                    mode = [True,True]
                    
    screen.fill([245,219,195])
    screen.blit(playwhite, [190,150])
    screen.blit(playblack, [190,230])
    screen.blit(watchbot, [190,310])
    screen.blit(playboth, [190,390])
    if pygame.mouse.get_pos()[0] > 190 and pygame.mouse.get_pos()[0] < 410:
        if pygame.mouse.get_pos()[1] > 150 and pygame.mouse.get_pos()[1] < 210:
            screen.blit(pygame.transform.scale(playwhite,[240,66]), [180,147])
        elif pygame.mouse.get_pos()[1] > 230 and pygame.mouse.get_pos()[1] < 290:
            screen.blit(pygame.transform.scale(playblack,[240,66]), [180,227])
        elif pygame.mouse.get_pos()[1] > 310 and pygame.mouse.get_pos()[1] < 370:
            screen.blit(pygame.transform.scale(watchbot,[240,66]), [180,307])
        elif pygame.mouse.get_pos()[1] > 390 and pygame.mouse.get_pos()[1] < 450:
            screen.blit(pygame.transform.scale(playboth,[240,66]), [180,387])
    pygame.display.flip()

def update(offset=0,mouse_position=64):
    for i in range(64):
        if ((i%8)+(i//8))%2 == 0:
            pygame.draw.rect(screen,[245,219,195],[(i%8)*75,((i//8)*75)-offset,75,75],0)
        else:
            pygame.draw.rect(screen,[187,87,70],[(i%8)*75,((i//8)*75)-offset,75,75],0)

        for j, piese in enumerate(pieces):
            if flip:
                if (piese >> i) & 1:
                    if mouse_position == i:
                        screen.blit(piece_images[j], [(i%8)*75,((i//8)*75)-offset])
                    else:
                        screen.blit(piece_images[j], [(i%8)*75,((i//8)*75)-offset])
            else:
                if (piese >> (63-i)) & 1:
                    screen.blit(piece_images[j], [(i%8)*75,((i//8)*75)-offset])
    pygame.display.flip()

for i in range(24):
    update(((23-i)*25))
    time.sleep(0.008)

update()
turn = 0
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
                update()
    if mode[turn]:
        #print(((pygame.mouse.get_pos()[0]*8)//600)+(((pygame.mouse.get_pos()[1]*8)//600)*8))
        update(0,((pygame.mouse.get_pos()[0]*8)//600)+(((pygame.mouse.get_pos()[1]*8)//600)*8))
    else:
        pass

