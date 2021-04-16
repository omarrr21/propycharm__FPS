import pygame
import sys
from math import *

pygame.init()
width = 400
height = 400
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# colors
backgrounf = (21, 67, 96)
border = (208, 211, 212)
red = (231, 76, 60)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
green = (88, 214, 141)

playerColor = [red, green, violet, yellow]
blocks = 40
noPlayers = 4

players = []
for i in range(noPlayers):
    players.append(playerColor[i])

d = blocks//2 - 2
cols = int(width//blocks)
rows = int(height//blocks)

grid = []


class Spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

    def addNeighbors(self, i, j):
        if i > 0:
            self.neighbors.append(grid[i-1][j])
        if i < rows - 1:
            self.neighbors.append(grid[i + 1][j])
        if j < cols -1:
            self.neighbors.append(grid[i][j+1])
        if j > 0:
            self.neighbors.append(grid[i][j-1])


def intializeGrid():
    global grid, players
    players = []

    for i in range(noPlayers):
        players.append(playerColor[i])

    grid = [[] for _ in range(cols)]
    for i in range(cols):
        for j in range(rows):
            newObj = Spot()
            grid[i].append(newObj)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(i,j)


def drawGrid(currentIndex):
    r = 0
    c = 0

    for i in range(width//blocks):
        r += blocks
        c += blocks

        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))

def showPresentGrid(vibrate = 1):
    r = -blocks
    c = -blocks
    padding = 2
    for i in range(cols):
        r += blocks
        c = -blocks
        for j in range(rows):
            c += blocks

            if grid[i][j].noAtoms == 0:
                grid[i][j].color = border

            elif grid[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, grid[i][j].color, (r + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))

            elif grid[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid[i][j].color, (r + 5, c + blocks/2 - d/2 -vibrate, d, d))
                pygame.draw.ellipse(display, grid[i][j].color, (r + d/2 + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))

            elif grid[i][j].noAtoms == 3:
                angle = 90
                x = r + blocks/2 - d/2 + (d/2)*cos(radians(angle))
                y = c + blocks/2 - d/2 + (d/2)*sin(radians(angle))
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))

                x = r + blocks/2 - d/2 + (d/2) * cos(radians(angle+90))
                y = c + 5 + (d/2) * sin(radians(angle+90))
                pygame.draw.ellipse(display, grid[i][j].color, (x+ vibrate, y, d, d))

                x = r + blocks/2 - d/2 + (d/2)*cos(radians(angle - 90))
                y = c + 5 + (d/2)*sin(radians(angle - 90))
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))


    pygame.display.update()



def addAtom(i, j, color):
    grid[i][j].noAtoms += 1
    grid[i][j].color = color
    if grid[i][j].noAtoms >= len(grid[i][j].neighbors):
        overflow(grid[i][j], color)

def overflow(cell, color):
    showPresentGrid()
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color

        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            overflow(cell.neighbors[m], color)



def gameLoop():
    intializeGrid()
    turns = 0
    vibrate = 0.5
    currentPlayer = 0
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = int(x/blocks)
                j = int(y/blocks)
                if grid[i][j].color == players[currentPlayer] or grid[i][j].color == border:
                    turns += 1
                    addAtom(i, j, players[currentPlayer])
                    currentPlayer += 1
                    if currentPlayer >= noPlayers:
                        currentPlayer = 0


        display.fill(backgrounf)
        # vibrate atoms
        vibrate *= -1

        drawGrid(currentPlayer)
        showPresentGrid(vibrate)

        pygame.display.update()
    clock.tick(20)

gameLoop()



