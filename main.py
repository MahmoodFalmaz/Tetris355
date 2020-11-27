import random, time, pygame, sys
from pygame.locals import *
from pygame import mixer
import os.path
from os import path

#Initailize the pygame with fonts
pygame.font.init()

#Background music
pygame.init()


#The Game Window Dimensions
WindowdowWidth = 800
WindowdowHeight = 800

#The Tetris Board Dimensions
tetrisWindow_Width = 300  # meaning 300 // 10 = 30 width per block
tetrisWindow_Height = 600  # meaning 600 // 20 = 30 height per block
tetrisBoard_Size = 30

X_Margin = (WindowdowWidth - tetrisWindow_Width) // 2
Y_Margin = WindowdowHeight - tetrisWindow_Height


# Referenced from https://inventwithpython.com/pygame/chapter7.html
# https://www.pygame.org/docs/
# https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
# https://www.byteacademy.co/blog/tetris-pygame-python
# https://www.pygame.org/project/3783
#https://stackoverflow.com/questions/62106273/tetris-pygame-falling-issues
# Tetris SHAPE FORMATS and the different oritentation it can display
S_SHAPE_TEMPLATE = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z_SHAPE_TEMPLATE = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I_SHAPE_TEMPLATE = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O_SHAPE_TEMPLATE = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J_SHAPE_TEMPLATE = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L_SHAPE_TEMPLATE = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T_SHAPE_TEMPLATE = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#Different Tetris Shapes 
tetrisShapes = [S_SHAPE_TEMPLATE, Z_SHAPE_TEMPLATE, I_SHAPE_TEMPLATE, O_SHAPE_TEMPLATE, J_SHAPE_TEMPLATE, L_SHAPE_TEMPLATE, T_SHAPE_TEMPLATE]
#Different Tetris Colors 
tetrisShapes_Colors = [(255, 0, 0), (255, 20, 147), (255, 69, 0), (0, 255, 127), (255, 255, 0),(255, 255, 255), (224, 255, 255)]


#Shape Object that contains descriptions of the current tetris shape
class Shape(object):  
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = tetrisShapes_Colors[tetrisShapes.index(shape)]
        self.rotation = 0


#Main Function to run the game and validation checks if the game should run
def main(Window):
    if path.exists("background.wav"):
        mixer.music.load("background.wav")
        pygame.mixer.music.set_volume(0.3)
        mixer.music.play(-1) #continuously play the music
    clock = pygame.time.Clock()
    normal_FPS = 0
    increased_FPS = 0.15
    difficulty = 10
    score = 0
    lockedPositions = {}
    updatePiece = False
    run = True
    tetrisPiece = randomTetris_Shape()
    nextTetrisPiece = randomTetris_Shape() 

    running, pause = 1, 0
    state = running

    while run: #GameLoop
        gameLayout = createGrid(lockedPositions)
        normal_FPS += clock.get_rawtime()
        difficulty += clock.get_rawtime()
        clock.tick()
        mouse = pygame.mouse.get_pos()

        if state == running:
            if difficulty/1000 > 5:
                difficulty = 0
                if difficulty > 0.12:
                    difficulty -= 0.005

            if normal_FPS/1000 > increased_FPS:
                normal_FPS = 0
                tetrisPiece.y += 1
                if not(spaceCheck(tetrisPiece, gameLayout)) and tetrisPiece.y > 0:
                    tetrisPiece.y -= 1
                    updatePiece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
            if state == running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetrisPiece.x -= 1
                        if not(spaceCheck(tetrisPiece, gameLayout)):
                            tetrisPiece.x += 1
                    if event.key == pygame.K_RIGHT:
                        tetrisPiece.x += 1
                        if not(spaceCheck(tetrisPiece, gameLayout)):
                            tetrisPiece.x -= 1
                    if event.key == pygame.K_DOWN:
                        tetrisPiece.y += 1
                        if not(spaceCheck(tetrisPiece, gameLayout)):
                            tetrisPiece.y -= 1
                    if event.key == pygame.K_UP:
                        tetrisPiece.rotation += 1
                        if not(spaceCheck(tetrisPiece, gameLayout)):
                            tetrisPiece.rotation -= 1
            if event.type == pygame.MOUSEBUTTONUP:
                    print(mouse) 
                    if WindowdowWidth-140 <= mouse[0] <= WindowdowWidth+140 and WindowdowHeight-40 <= mouse[1] <= WindowdowHeight+40: 
                        if (mixer.music.get_volume()!=0):
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(0.3)
                    if WindowdowWidth-140 <= mouse[0] <= WindowdowWidth and WindowdowHeight-80 <= mouse[1] <= WindowdowHeight-40:
                        if state == running: 
                            state = pause
                        elif state == pause: 
                            state = running
        if state == running:
            shape_pos = listShape(tetrisPiece)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    gameLayout[y][x] = tetrisPiece.color

            if updatePiece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    lockedPositions[p] = tetrisPiece.color
                tetrisPiece = nextTetrisPiece
                nextTetrisPiece = randomTetris_Shape()
                updatePiece = False
                score += scoredRows(gameLayout, lockedPositions) * 10

        drawWindow(Window, gameLayout,mouse, state, score)
        nextShape(nextTetrisPiece, Window)
        pygame.display.update()

        if checkState(lockedPositions):
            displayText(Window, "Game Over!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False


#Create the grid 10 wide and 20 high
def createGrid(lockedPositions={}): 
    gameLayout = [[(0,0,0) for i in range(10)] for j in range(20)]
    for i in range(len(gameLayout)):
        for j in range(len(gameLayout[i])):
            if (j, i) in lockedPositions:
                x = lockedPositions[(j,i)]
                gameLayout[i][j] = x
    return gameLayout

#Tetris Shapes
def listShape(shape):
    pass

#Checks if the tile dimensions are moved into a vlid space
def spaceCheck(shape, gameLayout):
    validSpace = [[(j, i) for j in range(10) if gameLayout[i][j] == (0,0,0)] for i in range(20)]
    validSpace = [j for x in validSpace for j in x]
    shapeMovement = listShape(shape)
    for i in shapeMovement:
        if i not in validSpace:
            if i[1] > -1:
                return False
    return True

#Checks the state of the game
def checkState(positions):
    for tile in positions:
        x, y = tile
        if y < 1:
            return True
    return False


def randomTetris_Shape():
    pass

#Displays text on the main screen
def displayText(Window, text, size, color):
    pass

#Displays the game layout
def drawLayout(Window, gameLayout):
    pass

#Rows that have be obtained by the player // Shifting row down one and adding to the top if once it's been cleared.
def scoredRows(gameLayout, locked):
    k = 0
    for i in range(len(gameLayout)-1, -1, -1):
        checkrow = gameLayout[i]
        if (0,0,0) not in checkrow:
            k += 1
            position = i
            for j in range(len(checkrow)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if k > 0:
        for key in sorted(list(locked),key=lambda x: x[1])[::-1]:
            x, y = key
            if y < position:
                newKey = (x, y + k)
                locked[newKey] = locked.pop(key)
    return k

#Determins the next shape to be used
def nextShape(shape, Window):
    pass

#Displays the layout, text, score and state of the game
def drawWindow(Window, gameLayout,mouse,state, score=0):
    Window.fill((0, 0, 0))
    Window.blit(image, (0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 40)
    Window.blit(logo, (WindowdowWidth/3,WindowdowHeight/12))
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Total Score: ' + str(score), 1, (255,255,255))
    score_xCord = X_Margin + tetrisWindow_Width + 50
    score_yCord = Y_Margin + tetrisWindow_Height/2 - 100
    score_xCord = X_Margin - 200
    score_yCord = Y_Margin + 200
    Window.blit(label, (score_xCord + 10, score_yCord - 30))
    for i in range(len(gameLayout)):
        for j in range(len(gameLayout[i])):
            pygame.draw.rect(Window, gameLayout[i][j], (X_Margin + j*tetrisBoard_Size, Y_Margin + i*tetrisBoard_Size, tetrisBoard_Size, tetrisBoard_Size), 6)
    pygame.draw.rect(Window, (255, 0, 0), (X_Margin, Y_Margin, tetrisWindow_Width, tetrisWindow_Height), 5)
    drawLayout(Window, gameLayout)
    handleMuteButton(Window,mouse)
    handlePauseButton(Window,state,mouse)

#Handles the Mute button
def handleMuteButton(Window,mouse):
    pass

#Handles the Pause Button
def handlePauseButton(Window,state,mouse):
    pass

#Main Menu
def mainMenu(Window):
    run = True
    while run:
        Window.fill((0,0,0))
        displayText(Window, 'Press Any Key To Play', 60, (255,255,255))
        displayText(Window, 'Press [Q] To Quit', 60, (255,255,255))
        displayText(Window, 'Move', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                else:
                    main(Window)

    pygame.display.quit()


Window = pygame.display.set_mode((WindowdowWidth, WindowdowHeight))
image  = pygame.image.load("tetris.jpg").convert_alpha()
size = width, height = 800 , 800
image = pygame.transform.scale(image,size)
mainMenu(Window) 