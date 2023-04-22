import random  # For generating random numbers
import sys # For exiting game when cancel is clicked
import pygame
from pygame.locals import * # Basic requirements

#Global Variables

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode(size=(SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'flappyBird.png'
BACKGROUND = 'background.png'
PIPE = 'pipe.png'

def welcomeScreen():
    """
    Shows welcome images on screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_width())/2)
    messagey = int(SCREENHEIGHT*0.01)
    basex = 0

    while True:
        for events in pygame.event.get():
            # If user clicks on cross button, close the game
            if((events.type == QUIT) or (events.type == KEYDOWN and events.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()
            
            # If the user presses space key or up key, start the game
            elif(events.type == KEYDOWN and events.key == K_SPACE):
                return
            else:
                SCREEN.blit(GAME_SPRITES["background"] , (0,0))
                SCREEN.blit(GAME_SPRITES["player"] , (playerx-10,playery))
                SCREEN.blit(GAME_SPRITES["message"],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES["base"] , (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    newPipe1 = getrandomPipe()
    newPipe2 = getrandomPipe()

    upperPipes = [
        {"x":SCREENWIDTH+200, "y":newPipe1[0]["y"]},
        {"x":SCREENWIDTH+(SCREENWIDTH/2)+200, "y":newPipe2[0]["y"]}
    ]

    lowerPipes = [
        {"x":SCREENWIDTH+200, "y":newPipe1[1]["y"]},
        {"x":SCREENWIDTH+(SCREENWIDTH/2)+200, "y":newPipe2[1]["y"]}
    ]

    pipeVelX = -4
    playerVely = -9
    playerMaxVel = 10
    playerMinVel = -8
    playerAccY = 1

    playerFlapAccv = -8 # Bird velocity while flapping
    playerFlapped = False
    while True:
        for events in pygame.event.get():
            if ((events.type == QUIT) or (events.type == KEYDOWN and events.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()
            if(events.type == KEYDOWN and (events.key == K_SPACE or events.key==K_UP)):
                playerVely = playerFlapAccv
                playerFlapped = True
                GAME_SOUNDS["wing"].play()
    
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        
        playerMidPos = playerx + (GAME_SPRITES["player"].get_width()/2) 
        for pipe in upperPipes:
            pipeMidpos = pipe['x'] + (GAME_SPRITES["pipe"][0].get_width()/2)
            if pipeMidpos <= playerMidPos < pipeMidpos+4:
                score+=1
                GAME_SOUNDS["point"].play()
        if playerVely < playerMaxVel and not playerFlapped:
            playerVely+=playerAccY
        if playerFlapped:
            playerFlapped = False
        
        playerheight = GAME_SPRITES["player"].get_height()
        playery = playery + min(playerVely,GROUNDY-playery-playerheight)

        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe['x']+=pipeVelX
            lowerpipe['x']+=pipeVelX
        
        if 0 < upperPipes[0]["x"] < 5:
            newpipe = getrandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES["background"],(0,0))
        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0],(upperpipe["x"],upperpipe["y"]))    
            SCREEN.blit(GAME_SPRITES["pipe"][1],(lowerpipe["x"],lowerpipe["y"]))    
        SCREEN.blit(GAME_SPRITES["base"],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"],(playerx,playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width+=GAME_SPRITES["numbers"][digit].get_width()
        xoffset = (SCREENWIDTH-width)/2

        for digits in myDigits:
            SCREEN.blit(GAME_SPRITES["numbers"][digits],(xoffset,SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES["numbers"][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def getrandomPipe():
    """
    Generate Position of two pipes
    """
    pipeheight = GAME_SPRITES["pipe"][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES["base"].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH+10
    y1 = pipeheight - y2 + offset
    pipe = [
        {"x":pipeX, "y":-y1}, # upperpipe
        {"x":pipeX,"y":y2}
    ]
    return pipe;

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

if __name__ == '__main__':
    # This will be the main point from where the game will start
    pygame.init() # Initializes all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Prathamesh")
    GAME_SPRITES["numbers"] = (
        pygame.image.load("numbers/zero.png").convert_alpha(),
        pygame.image.load("numbers/one.png").convert_alpha(),
        pygame.image.load("numbers/two.png").convert_alpha(),
        pygame.image.load("numbers/three.png").convert_alpha(),
        pygame.image.load("numbers/four.png").convert_alpha(),
        pygame.image.load("numbers/five.png").convert_alpha(),
        pygame.image.load("numbers/six.png").convert_alpha(),
        pygame.image.load("numbers/seven.png").convert_alpha(),
        pygame.image.load("numbers/eight.png").convert_alpha(),
        pygame.image.load("numbers/nine.png").convert_alpha()
    )
    GAME_SPRITES["message"] = pygame.image.load("message.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("base.png").convert_alpha()
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS["die"] = pygame.mixer.Sound("sounds/die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("sounds/hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("sounds/point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("sounds/swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("sounds/wing.wav")

    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        maingame()