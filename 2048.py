#!/usr/bin/env python3

import pygame, sys, random, math, time

pygame.init()
pygame.font.init()

RESOLUTION = WIDTH, HEIGHT = 570, 740
TITLE = "2048"
GRID_SIZE = 4
STARTING_TILES = 2

tileSize  = 500 // GRID_SIZE
backgroundColor = (250, 248, 239)
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
center = [WIDTH // 2, max(HEIGHT - WIDTH // 2, HEIGHT // 2 + 100)]
scale = 4 / GRID_SIZE
score = 0
# Add window title icon
# icon = pygame.image.load('2048icon.png')
# pygame.display.set_icon(icon)

class Tiles(object):
    def __init__(self, value):
        self.value = value
        # Tile color
        if self.value == 0:
            self.color = (205, 192, 180)
        elif self.value == 2:
            self.color = (238, 228, 218)
        elif self.value == 4:
            self.color = (237, 224, 200)
        elif self.value == 8:
            self.color = (242, 177, 121)
        elif self.value == 16:
            self.color = (245, 149, 99)
        elif self.value == 32:
            self.color = (246, 124, 95)
        elif self.value == 64:
            self.color = (246, 94, 59)
        elif self.value == 128:
            self.color = (237, 207, 114)
        elif self.value == 256:
            self.color = (237, 204, 97)
        elif self.value == 512:
            self.color = (237, 200, 80)
        elif self.value == 1024:
            self.color = (237, 197, 63)
        elif self.value == 2048:
            self.color = (237, 194, 46)
        else:
            self.color = (60, 58, 50)
        # Make block value font smaller for higher values
        if self.value < 10 ** 2:
            self.fontSize = 85
        elif self.value < 10 ** 3:
            self.fontSize = 75
        elif self.value < 10 ** 4:
            self.fontSize = 65
        elif self.value < 10 ** 5:
            self.fontSize = 55
        elif self.value < 10 ** 6:
            self.fontSize = 45
        elif self.value < 10 ** 7:
            self.fontSize = 35
        elif self.value < 10 ** 9:
            self.fontSize = 30
        else:
            self.fontSize = 25
        # Set font color
        if self.value < 8:
            self.fontColor = (119, 110, 101)
        else:
            self.fontColor = (249, 246, 242)
        

class Grid(object):

    def __init__(self):
        self.tiles = [[Tiles(0) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    def newTile(self):
        pos = []
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.tiles[y][x].value == 0:
                    pos.append([x, y])
        value = 4 if random.randint(0, 9) == 0 else 2
        if len(pos) == 0:
            return
        pos = random.choice(pos)
        x = pos[0]
        y = pos[1]
        self.tiles[y][x] = Tiles(value)

# Rotate counter clock-wise
def ccw(tiles):
    output = []
    for x in range(len(tiles[0])-1, -1, -1):
        output.append([])
        for y in range(len(tiles)):
            output[-1].append(tiles[y][x])
    return output

# Rotate clock-wise
def cw(tiles):
    output = []
    for x in range(len(tiles[0])):
        output.append([])
        for y in range(len(tiles)-1, -1, -1):
            output[-1].append(tiles[y][x])
    return output



def _left(tiles):
    merged = []
    newGrid = []
    for y in range(GRID_SIZE):
        line = tiles[y]
        lineMerged = []
        newLine = []
        for x in range(GRID_SIZE):
            if line[x].value != 0:
                if len(newLine) == 0:
                    newLine.append(line[x])
                    lineMerged.append(False)
                elif newLine[-1].value == line[x].value:
                    if lineMerged[-1] == False:
                        newLine[-1] = Tiles(line[x].value * 2)
                        lineMerged[-1] = True
                    else:
                        newLine.append(line[x])
                        lineMerged.append(False)
                else:
                    newLine.append(line[x])
                    lineMerged.append(False)
        newLine += [Tiles(0)] * (GRID_SIZE - len(newLine))
        lineMerged += [False] * (GRID_SIZE - len(lineMerged))
        merged.append(lineMerged)
        newGrid.append(newLine)

    addScore = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if merged[y][x] == True:
                addScore += newGrid[y][x].value
    
    return [newGrid, addScore]


# Helper functions
def _right(tiles):
    merged = []
    newGrid = []
    for y in range(GRID_SIZE):
        line = tiles[y]
        lineMerged = []
        newLine = []
        for x in range(GRID_SIZE-1, -1, -1):
            if line[x].value != 0:
                if len(newLine) == 0:
                    newLine = [line[x]]
                    lineMerged.append(False)
                elif newLine[0].value == line[x].value:
                    if lineMerged[0] == False:
                        newLine[0] = Tiles(line[x].value*2)
                        lineMerged[0] = True
                    else:
                        newLine = [line[x]] + newLine
                        lineMerged = [False] + lineMerged
                else:
                    newLine = [line[x]] + newLine
                    lineMerged = [False] + lineMerged
        newLine = [Tiles(0)] * (GRID_SIZE - len(newLine)) + newLine
        lineMerged = [False] * (GRID_SIZE - len(lineMerged)) + lineMerged
        merged.append(lineMerged)
        newGrid.append(newLine)

    addScore = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if merged[y][x] == True:
                addScore += newGrid[y][x].value
    
    return [newGrid, addScore]


def _up(tiles):
    tiles = _left(ccw(tiles))
    return [cw(tiles[0]), tiles[1]]


def _down(tiles):
    tiles = _right(ccw(tiles))
    return [cw(tiles[0]), tiles[1]]


def left(grid, score):
    tiles = grid.tiles
    temp = _left(tiles)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if tiles[y][x].value != temp[0][y][x].value:
                grid.tiles = temp[0]
                score += temp[1]
                grid.newTile()
                return [grid, score]
    return [grid, score]


def right(grid, score):
    tiles = grid.tiles
    temp = _right(grid.tiles)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if tiles[y][x].value != temp[0][y][x].value:
                grid.tiles = temp[0]
                score += temp[1]
                grid.newTile()
                return [grid, score]
    return [grid, score]

def up(grid, score):
    tiles = grid.tiles
    temp = _up(tiles)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if tiles[y][x].value != temp[0][y][x].value:
                grid.tiles = temp[0]
                score += temp[1]
                grid.newTile()
                return [grid, score]
    return [grid, score]

def down(grid, score):
    tiles = grid.tiles
    temp = _down(tiles)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if tiles[y][x].value != temp[0][y][x].value:
                grid.tiles = temp[0]
                score += temp[1]
                grid.newTile()
                return [grid, score]
    return [grid, score]




def draw(grid):
    # Fill Background
    screen.fill(backgroundColor)
    
    text = pygame.font.SysFont("Clear Sans", 100)
    title = text.render("2048", True, (119, 110, 101))
    screen.blit(title, (50, 50))
    
    # Starting Position of grid
    startX = center[0] - tileSize * GRID_SIZE/2
    startY = center[1] - tileSize * GRID_SIZE/2
    
    # Ending Position of grid
    endX = center[0] + tileSize * GRID_SIZE/2
    endY = center[1] + tileSize * GRID_SIZE/2

    # Draw tiles
    grid = grid.tiles
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            fontColor = grid[y][x].fontColor
            value = grid[y][x].value
            color = grid[y][x].color
            pygame.draw.rect(screen, color, [startX + x * tileSize, startY + \
                y * tileSize, tileSize, tileSize])
            font = pygame.font.SysFont("Clear Sans", int(grid[y][x].fontSize*scale))
            text = font.render((str(value) if value != 0 else ""), True, fontColor)
            textWidth = text.get_width()
            textHeight = text.get_height()
            screen.blit(text, (startX + x*tileSize + tileSize/2 - textWidth/2, \
                startY + y*tileSize + tileSize/1.9 - textHeight/2))
            
    
    # line thickness
    thickness = math.ceil(10 * scale)
    
    # draw lines
    for pos in range(GRID_SIZE+1):
        e = math.ceil(1 * scale)
        pygame.draw.line(screen, (187, 173, 160), (startX - thickness // 2 + \
            e, startY + pos * tileSize), (endX + thickness//2, startY + pos * \
            tileSize), thickness)
        pygame.draw.line(screen, (187, 173, 160), (startX + pos * tileSize, \
            startY - thickness // 2 + e), (startX + pos * tileSize, endY + \
            thickness // 2), thickness)

    # display score
    font = pygame.font.SysFont("Clear Sans", 40)
    text = font.render("Score", True, (238, 228, 218))
    textWidth = text.get_width()
    textHeight = text.get_height()
    
    pygame.draw.rect(screen, (187, 173, 160), (WIDTH - 235 - textWidth // 2, \
        105 - textHeight // 2, textWidth * 1.7, textHeight // 2 * 7))
                     
    screen.blit(text, (WIDTH -  210 - textWidth//2, 110 - textHeight//2))

    if score < 10:
        size = 80
    elif score < 10 ** 2:
        size = 75
    elif score < 10 ** 3:
        size = 70
    elif score < 10 ** 4:
        size = 65
    elif score < 10 ** 5:
        size = 60
    elif score < 10 ** 6:
        size = 50
    elif score < 10 ** 7:
        size = 40
    else:
        size = 30
    
    font = pygame.font.SysFont("Clear Sans", size)
    text = font.render(str(score), True, (255, 255, 255))
    textWidth = text.get_width()
    textHeight = text.get_height()
    screen.blit(text, (WIDTH - ((210 + textWidth // 2) if score < 10 ** 12 \
        else 270), 155 - textHeight // 2))
    
    font = pygame.font.SysFont("Clear Sans", 24)
    text = font.render("New Game", True, (238, 228, 218))
    textWidth = text.get_width()
    textHeight = text.get_height()
    pygame.draw.rect(screen, (143, 122, 102), (WIDTH - 387, 145, 103, 25))
    screen.blit(text, (WIDTH - 335 - textWidth // 2, 157 - textHeight // 2))
    
    pygame.display.update()

def isGameOver(grid):
    grid = grid.tiles
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x].value == 0:
                return False
            value = grid[y][x].value
            if y != 0 and grid[y-1][x].value == value:
                return False
            if y != GRID_SIZE-1 and grid[y+1][x].value == value:
                return False
            if x != 0 and grid[y][x-1].value == value:
                return False
            if x != GRID_SIZE-1 and grid[y][x+1].value == value:
                return False
    return True


def gameOver():
    messageTime = 5 # seconds
    font = pygame.font.SysFont('Clear Sans', 50)
    score_label = font.render("Game Over; Score: " + str(score), True, (119, 110, 101))
    surface = pygame.Surface((WIDTH, HEIGHT))  # the size of your rect
    surface.set_alpha(192) # alpha level
    for _ in range(messageTime): # For loop is needed so that user can close the window
        surface.fill((255, 255, 255)) # this fills the entire surface
        screen.blit(surface, (0, 0)) # (0, 0) are the top-left coordinates
        screen.blit(score_label,(WIDTH // 2 - score_label.get_width() // 2, \
            HEIGHT // 2 - score_label.get_height()))
        pygame.display.update()
        time.sleep(1)


grid = Grid()
GAME_OVER = False
for _ in range(STARTING_TILES):
    grid.newTile()
keys = ""
button = 0
draw(grid)

while True:
    prevButton = button
    prev = keys
    for event in pygame.event.get():
        keys = ""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            button = event.button
            break
        else:
            button = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys = "up"
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys = "down"
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys = "left"
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys = "right"
            break
    GAME_OVER = isGameOver(grid)
    if GAME_OVER:
        draw(grid)
        GAME_OVER = False
        gameOver()
        score = 0
        grid = Grid()
        for _ in range(STARTING_TILES):
            grid.newTile()
        draw(grid)

    # new game
    if button != prev and button != 0:
        x, y = pygame.mouse.get_pos()
        button = 0
        if x in range(WIDTH - 387, WIDTH - 284) and y in range(145, 170):
            score = 0
            grid = Grid()
            for _ in range(STARTING_TILES):
                grid.newTile()
            draw(grid)

    if keys != prev and keys != "":
        if keys == "up":
            [grid, score] = up(grid, score)
        if keys == "down":
            [grid, score] = down(grid, score)
        if keys == "left":
            [grid, score] = left(grid, score)
        if keys == "right":
            [grid, score] = right(grid, score)
        draw(grid)


