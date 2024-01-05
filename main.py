import pygame, sys
from pygame.locals import * 
import random 
import time 

# constant 
WINDOW_WIDTH = 600 
WINDOW_HEIGHT = 600 
FPS = 60 
ROWS = 4
COLS = 5
GAP = 20 
BOX_SIZE = 80 
XMARGIN = (WINDOW_WIDTH - (COLS*BOX_SIZE + GAP*(COLS-1)))//2
YMARGIN = 150
GAME_WIDTH = XMARGIN + (COLS*BOX_SIZE + GAP*(COLS-1))
GAME_HEIGHT = YMARGIN + (ROWS*BOX_SIZE + GAP*(ROWS-1))
choice = [i for i in range((ROWS*COLS)//2)]*2
random.shuffle(choice)


# (117, 106, 182)
BG_COLOR = (178,132,199) #(251,46,1) #(187,187,187) 
FG_COLOR = (250,238,209)
PRIMARY_COLOR = (224, 174, 208)
SECONDARY_COLOR = (255, 229, 229)
SCORE = 0
MOVES = 0 

dct = {}
dct_set = set()
BOXES = []

class Box:
    def __init__(self, x, y, size, color, font, game_surface, number):
        self.revealed = False
        self.color = color
        self.x = x 
        self.y = y
        self.size = size 
        self.font = font
        self.game_surface = game_surface
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.number = number
        self.done = False 
    
    def print_box(self):
        if self.revealed or self.done:
            pygame.draw.rect(self.game_surface, self.color, self.rect)
            text = self.font.render(f'{self.number} {self.done}', False, (0, 0, 0))
            self.game_surface.blit(text, (self.x +(self.size//2), self.y + (self.size //2)))
        else:
            pygame.draw.rect(self.game_surface, FG_COLOR, self.rect)
    
    def isClicked(self, x, y):
        if (self.x <= x <= self.x + self.size) and (self.y <= y <= self.y+self.size):
            return True 
        return False 


def make_boxes(game_surface, rows, cols, font):
    y = YMARGIN
    x = XMARGIN
    width = 80 
    gap = 20 
    for i in range(rows):
        temp = []
        for j in range(cols):
            number = choice.pop()
            box = Box((x+j*(width+gap)), (y+i*(width+gap)), width, PRIMARY_COLOR, font, game_surface, number)
            temp.append(box)
        BOXES.append(temp[:])

def print_grid(game_surface, boxes,  ):
    for row in boxes:
        for box in row:
            box.print_box()

# def reset_boxes(boxes, show):
#     for row in boxes:
#         for box in row:
#             box.revealed = show 

def handle_click(game_surface, boxes, pos):
    global SCORE
    global MOVES
    x = pos[0]
    y = pos[1]
    if XMARGIN <= x <= GAME_WIDTH and YMARGIN <= y <= GAME_HEIGHT:
        for i in range(ROWS):
            for j in range(COLS):
                if boxes[i][j].isClicked(x, y):
                    boxes[i][j].revealed = not boxes[i][j].revealed
                    boxes[i][j].print_box()
                    num = boxes[i][j].number
                    if num not in dct:
                        dct[num] = (i, j)
                        if len(dct.keys()) > 3:
                            remove_dct(BOXES)
                        MOVES += 1
                    else:
                        n, m = dct[num]
                        boxes[i][j].done = True 
                        boxes[n][m].done = True 
                        del dct[num]
                        SCORE += 1

def remove_dct(boxes):
    k = next(iter(dct))
    n, m = dct[k]
    boxes[n][m].revealed = False 
    dct.pop(k)


def main():
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)


    # clock
    GAME_CLOCK = pygame.time.Clock()

    GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("MEMORY GAME")

    make_boxes(GAME_WINDOW, ROWS, COLS, myfont)

    while True:
        GAME_WINDOW.fill(BG_COLOR)

        print_grid(GAME_WINDOW, BOXES)

        SCORE_text = myfont.render(f'SCORE: {SCORE}', False, (0, 0, 0))
        MOVES_text = myfont.render(f'MOVES: {MOVES}', False, (0, 0, 0))
        GAME_WINDOW.blit(SCORE_text, (20, 20))
        GAME_WINDOW.blit(MOVES_text, (500, 20))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                btn = pygame.mouse.get_pressed()
                handle_click(GAME_WINDOW, BOXES, pos)

        

            
        
        pygame.display.update()

        GAME_CLOCK.tick(FPS)


if __name__=="__main__":
    main()