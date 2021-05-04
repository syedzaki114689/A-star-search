import pygame
from pygame.locals import *
import math
import random

# globals
running = True
display_width = 800
display_height = 800
col = 100
row = 100
button_row_height = 50
fps = 60
fpsclk = pygame.time.Clock()

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

        '''if(random.random() < 0.3):
            self.wall = True
'''

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


def drawbuttons(active, game_display):

    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if(active == True):
        if (mouse[0] > 10 and mouse[0] < (display_width-20) and mouse[1] > (display_height+4) and mouse[1] < (display_height+4)+button_row_height):
            pygame.draw.rect(game_display, green, (50,
                                                   (display_height+4), (display_width-10), button_row_height))
            if(clicked[0] == 1):
                return "again"

        else:
            pygame.draw.rect(game_display, bright_green, (50, (display_height+4),
                                                          (display_width-10), button_row_height))

    else:
        pygame.draw.rect(game_display, green, (50, (display_height+4),
                                               (display_width-10), button_row_height))

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


def drawbox(game_display):
    pygame.draw.lines(game_display, black, False, [
        (50, 0), (50, display_height)], 5)
    pygame.draw.lines(game_display, black, False, [
        (50, display_height), (display_width+50, display_height)], 5)
    pygame.draw.lines(game_display, black, False, [
        (display_width+50, display_height), (display_width+50, 0)], 5)
    pygame.draw.lines(game_display, black, False, [
        (display_width+50, 0), (50, 0)], 5)


def add_walls(grid, t):
    maze = []

    if t == 1:
        f = open("mazedata.txt", "r")
    else:
        f = open("mazedata1.txt", "r")

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
                    grid[j][i].wall = True
                else:
                    grid[j][i].wall = False
    else:
        print("file error")


def astar(type):

    grid = []

    if type == 1:
        for i in range(col):
            lis = []
            for j in range(row):
                lis.append(point(i, j, width, height))
            grid.append(lis)

        add_walls(grid, 1)

    else:
        grid = draw_walls()

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
    winner = 00
    # previous_coordinates = (start.x*width, start.y*height)
    game_display = pygame.display.set_mode(
        (actual_display_width, actual_display_height))

    pygame.display.set_caption('A* search aligorithm')
    pygame.init()
    while (len(openset) > 0):
        drawbox(game_display)
        drawbuttons(False, game_display)
        event_handler()

        if(winner > len(openset)):
            print("no solution")
            break

        for s in openset:
            if(openset.__len__() <= winner):
                print("no path found")
                break

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
                    pygame.draw.circle(game_display, black, (grid[i][j].x*width+(width/2)+50,
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
            current_cordinates = (ele.x*width+(width/2)+50,
                                  ele.y*height+(width/2))
            if(ele.camefrom == None):
                previous_coordinates = (
                    start.x*width+(width/2)+50, start.y*height+(width/2))
            else:
                previous_coordinates = (
                    ele.camefrom.x*width+(width/2)+50, ele.camefrom.y*width+(width/2))

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
        fpsclk.tick(fps)
        game_display.fill(white)


def draw_walls():
    game_display1 = pygame.display.set_mode(
        (actual_display_width, actual_display_height))
    pygame.display.set_caption('A* search aligorithm')
    pygame.init()
    grid = []
    for i in range(col):
        lis = []
        for j in range(row):
            lis.append(point(i, j, width, height))
        grid.append(lis)

    t = 1
    while(t == 1):
        drawbox(game_display1)
        event_handler()
        for i in range(col):
            for j in range(row):
                if(grid[i][j].wall == True):
                    pygame.draw.circle(game_display1, black, (grid[i][j].x*width+(width/2)+50,
                                                              grid[i][j].y*height+(width/2)), height/2)

        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        if clicked[0] == 1:
            mouse_x, mouse_y = mouse[0], mouse[1]
            i = int(((2*mouse_x) - width - 100)/(2*width))
            j = int(((2*mouse_y) - width)/(2*height))

            if i < 0:
                i = 0
            if j < 0:
                j = 0
            if i >= col:
                i = col-1
            if j >= row:
                j = row-1

            grid[i][j].wall = True

        if (mouse[0] > 10 and mouse[0] < (display_width-20) and mouse[1] > (display_height+4) and mouse[1] < (display_height+4)+button_row_height):
            pygame.draw.rect(game_display1, green, (50,
                                                    (display_height+4), (display_width-10), button_row_height))
            if(clicked[0] == 1):
                t = 0

        else:
            pygame.draw.rect(game_display1, bright_green, (50, (display_height+4),
                                                           (display_width-10), button_row_height))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Run!', True, black)
        textRect = text.get_rect()
        textRect.center = (10+((display_width-20)/2),
                           (display_height+4)+(button_row_height/2))

        game_display1.blit(text, textRect)

        pygame.display.update()
        game_display1.fill(white)
        fpsclk.tick(fps)

    pygame.quit()
    return grid


def initial():
    game_display1 = pygame.display.set_mode(
        (700, 600))
    pygame.display.set_caption('A* search aligorithm')
    pygame.init()

    t = 0
    while t == 0:
        event_handler()
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        loc1 = [(10, 320), (300, 60)]
        loc2 = [(420, 320), (250, 60)]

        if (mouse[0] > loc1[0][0] and mouse[0] < loc1[1][0]+loc1[0][0] and mouse[1] > loc1[0][1] and mouse[1] < loc1[1][1]+loc1[0][1]):

            pygame.draw.rect(game_display1, green, (loc1[0], loc1[1]))

            if(clicked[0] == 1):
                t = 1

        else:
            pygame.draw.rect(game_display1, red, (loc1[0], loc1[1]))

        if (mouse[0] > loc2[0][0] and mouse[0] < loc2[1][0]+loc2[0][0] and mouse[1] > loc2[0][1] and mouse[1] < loc2[1][1]+loc2[0][1]):

            pygame.draw.rect(game_display1, green, (loc2[0], loc2[1]))

            if(clicked[0] == 1):
                t = 2

        else:
            pygame.draw.rect(game_display1, red, (loc2[0], loc2[1]))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Pathfinding algorithms', True, black)
        text1 = font.render('import wall data?', True, black)
        text2 = font.render('draw walls?', True, black)
        textRect = text.get_rect()
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect.center = (340, 100)
        textRect1.center = (170, 350)
        textRect2.center = (550, 350)
        game_display1.blit(text, textRect)
        game_display1.blit(text1, textRect1)
        game_display1.blit(text2, textRect2)

        pygame.display.update()
        game_display1.fill(white)
        fpsclk.tick(fps)
    pygame.quit()
    return t


t = initial()
astar(t)


while running:
    game_display = pygame.display.set_mode(
        (actual_display_width, actual_display_height))
    text = drawbuttons(True, game_display)
    if(text == "again"):
        t = initial()
        astar(t)
