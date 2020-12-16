import pygame
from pygame.locals import *
import math
import random

# globals
running = True
display_width = 750
display_height = 750
col = 50
row = 50
button_row_height = 50
width = display_width/col
height = display_height/row
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
bright_green = (0, 255, 0)
actual_display_height = display_height+button_row_height
actual_display_width = display_width+100

game_display = pygame.display.set_mode(
    (actual_display_width, actual_display_height))


pygame.display.set_caption('A* search aligorithm')

pygame.init()


class point():

    def __init__(self, x, y, w, h):
        self.f = 0
        self.g = 0
        self.h = 0
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.neighbors = []
        self.camefrom = None
        self.wall = False

        if(random.random() < 0.2):
            self.wall = True

    def addneighbors(self, grid, rows, cols):
        i = self.x
        j = self.y

        if (i > 0):
            self.neighbors.append(grid[i-1][j])
        if(j > 0):
            self.neighbors.append(grid[i][j-1])
        if(i < rows-1):
            self.neighbors.append(grid[i+1][j])
        if(j < cols-1):
            self.neighbors.append(grid[i][j+1])

        if(i > 0 and j > 0):
            self.neighbors.append(grid[i-1][j-1])
        if(i < cols-1 and j > 0):
            self.neighbors.append(grid[i+1][j-1])
        if(i > 0 and j < rows-1):
            self.neighbors.append(grid[i-1][j+1])
        if(i < cols-1 and j < rows-1):
            self.neighbors.append(grid[i+1][j+1])


def heuristic(neighbor, end):
    distt = math.sqrt((neighbor.x-end.x)**2+(neighbor.y - end.y)**2)
    # distt = abs(neighbor.x-end.x) + abs(neighbor.y - end.y)
    return distt


def drawbuttons(active):

    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if(active == True):
        if (mouse[0] > 10 and mouse[0] < (display_width-20) and mouse[1] > (display_height+4) and mouse[1] < (display_height+4)+button_row_height):
            pygame.draw.rect(game_display, green, (10,
                                                   (display_height+4), (display_width-20), button_row_height))
            if(clicked[0] == 1):
                print("again")
                return "again"

        else:
            pygame.draw.rect(game_display, bright_green, (10, (display_height+4),
                                                          (display_width-20), button_row_height))

    else:
        pygame.draw.rect(game_display, green, (10, (display_height+4),
                                               (display_width-20), button_row_height))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Run again!', True, white)
    textRect = text.get_rect()
    textRect.center = (10+((display_width-20)/2),
                       (display_height+4)+(button_row_height/2))

    game_display.blit(text, textRect)


def event_handler():

    for event in pygame.event.get():
        if (event.type == QUIT):
            running = False
            pygame.quit()
            quit()


def drawbox():
    pygame.draw.lines(game_display, black, False, [
        (0, 0), (0, display_height)], 5)
    pygame.draw.lines(game_display, black, False, [
        (0, display_height), (display_width, display_height)], 5)
    pygame.draw.lines(game_display, black, False, [
        (display_height, display_height), (display_width, 0)], 5)
    pygame.draw.lines(game_display, black, False, [
        (display_height, 0), (0, 0)], 5)


def add_walls(grid):
    maze = []
    f = open("mazedata.txt", "r")
    lines = f.readlines()
    for line in lines:
        length = len(line)
        lis = []
        for i in range(length):
            if(not line[i] == '\n'):
                lis.append(line[i])
        maze.append(lis)
    # print(maze)
    if(len(maze) == len(grid)):
        for i in range(col):
            for j in range(row):
                if(maze[i][j] == '#'):
                    grid[i][j].wall = True
                else:
                    grid[i][j].wall = False
    else:
        print("file error")


def astar():
    grid = []

    for i in range(col):
        lis = []
        for j in range(row):
            lis.append(point(i, j, width, height))
        grid.append(lis)
    for i in range(col):
        for j in range(row):
            grid[i][j].addneighbors(grid, row, col)
    openset = []
    closedset = []
    start = grid[0][0]
    start.wall = False
    end = grid[col-1][row-1]
    end.wall = False
    openset.append(start)

    # add_walls(grid)

    winner = 00
    #previous_coordinates = (start.x*width, start.y*height)
    while (len(openset) > 0):
        drawbox()
        drawbuttons(False)
        event_handler()

        if(winner > len(openset)):
            print("no solution")
            break

        for s in openset:
            if(s.f < openset[winner].f):
                winner = openset.index(s)

        current = openset[winner]
    #    for s in openset:
    #        pygame.draw.rect(game_display, green, (s.x*width,
    #                                               s.y*height, width, height))

    #    for i in closedset:
    #        pygame.draw.rect(game_display, red, (i.x*width,
    #                                             i.y*height, width, height))

        for i in range(col):
            for j in range(row):
                if(grid[i][j].wall == True):
                    pygame.draw.circle(game_display, black, (grid[i][j].x*width+(width/2),
                                                             grid[i][j].y*height+(width/2)), height/2)

        path = []
        temp = current
        path.append(temp)
        while(not temp.camefrom == None):
            path.append(temp.camefrom)
            temp = temp.camefrom

        current_cordinates = ()
        previous_coordinates = ()

        for ele in path:
            # pygame.draw.rect(game_display, blue, (ele.x*width,
            #                                     ele.y*height, width, height))
            current_cordinates = (ele.x*width+(width/2),
                                  ele.y*height+(width/2))
            if(ele.camefrom == None):
                previous_coordinates = (
                    start.x*width+(width/2), start.y*height+(width/2))
            else:
                previous_coordinates = (
                    ele.camefrom.x*width+(width/2), ele.camefrom.y*width+(width/2))

            pygame.draw.lines(game_display, (100, 255, 150), False, [
                current_cordinates, previous_coordinates], 9)

        if(current == end):
            print("done")
            break

        openset.remove(current)
        closedset.append(current)

        for neighbor in current.neighbors:

            if neighbor not in closedset and neighbor.wall == False:
                tempg = current.g + 1

                newpath = False

                if neighbor in openset:

                    if(tempg < neighbor.g):
                        neighbor.g = tempg
                        newpath = True

                else:

                    neighbor.g = tempg
                    openset.append(neighbor)
                    newpath = True

                if(newpath == True):
                    neighbor.h = heuristic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.camefrom = current

        pygame.display.update()
        game_display.fill(white)
        pygame.time.wait(50)
    pygame.display.update()


# add_walls()
astar()

while running:
    text = drawbuttons(True)
    if(text == "again"):
        print("dasdsafcfsa")
        astar()
    event_handler()
    pygame.display.update()
