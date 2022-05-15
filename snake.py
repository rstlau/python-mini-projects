import pygame
import sys
import random

class snake: # rep the moving snake
    def __init__(self):
        self.length = 1 
        self.blocks = [((window_x/2), (window_y/2))]
        self.direction = random.choice([up, left, right, down])
        self.colour = (0,0,0) # colour of the snake
        self.score = 0 # snake score

    def draw(self, surface):
        # draw the snake onto the surfac
        for block in self.blocks: # draw everyblock
            # for the position in the list, grab the x element and the y element

            # start at block_x, block_y, stretch by width gridsize and height gridsize
            body = pygame.Rect((block[0], block[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.colour, body)  # draw the snake body
            pygame.draw.rect(surface, (255,255,255), body, 1) # overlap boxes with the thickness divisor of 1 pixel space    
        pass

    def get_head_position(self):
        # returns the position of the head of the snake
        return self.blocks[0]

    def turn(self, direction): # what to do when you have a turn
        if self.length > 1 and ((direction[0]*-1,direction[1]*-1) == self.direction):
            return
        else:
            self.direction = direction # change direction

    def move(self, paused):
        if paused == True:
            return
        # calculate new position of the head of the snake
        curr_pos = self.get_head_position()
        new_x = self.direction[0]
        new_y = self.direction[1] 
        future_x = curr_pos[0] + new_x*gridsize
        future_y = curr_pos[1] + new_y*gridsize
        future_pos = (future_x%window_x,future_y%window_y)
        if future_pos in self.blocks[3:]: 
            self.reset()
        else: # append the new head to the start of the block list
            self.blocks.insert(0, future_pos)
            if len(self.blocks) > self.length:
                self.blocks.pop() # pop the last element if the length is longer

    def reset(self): #reset snake position when you eat your own tail
        self.length = 1
        self.blocks = [((window_x/2), (window_y/2))]
        self.direction = random.choice([up, left, right, down])
        self.score = 0

class food: # rep moving food blck
    def __init__(self):
        self.spawn = (0,40)
        self.color = (255,0,0)
        self.respawn() # need this to call random initial spawns

    def respawn(self):
        new_x = random.randint(0, grid_x-1)*gridsize # make sure the block rests inside a grid square, its a unit of the square
        new_y = random.randint(2, grid_y-1)*gridsize # a multiple of the gridsize, but not outside
        self.spawn = (new_x, new_y)

    def draw(self, surface): # draw the food object
        fblock = pygame.Rect((self.spawn[0], self.spawn[1]),(gridsize, gridsize))
        pygame.draw.rect(surface, self.color, fblock)
        pygame.draw.rect(surface, (255,255,255), fblock, 1) # thickness behind block so border around box

# draw the checkered bg
def draw_bg(surface):
    for y in range (2, int(grid_y)):
        for x in range (0, int(grid_x)):
            if (x+y)% 2 == 0: # draw light square if even
                # Rect((left, top), (width, height))
                # basically (left, top) = (0,0) fromm source then it stretches to (20,20)
                # and then you fill that stretch/selection with the colour
                lightr = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (255, 255, 255), lightr)
            else:  
                darkr = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (240, 240, 240), darkr)


# game window
# window is 480 x 480
window_x = 480
window_y = 480

# grid of 240 boxes to fill 480x480
# by x there will be 20 boxes
# by y there will be 20 boxes
gridsize = 20
grid_x = window_x/gridsize
grid_y = window_y/gridsize

up = (0,-1) # the new head position has to be higher than the tail 
down = (0, 1)
left = (-1,0)
right = (1,0)

fps = 10

# game loop
def main():
    pygame.init()

    clock = pygame.time.Clock()
    game_window = pygame.display.set_mode((window_x, window_y), 0, 32)
    pygame.display.set_caption("Snake Game") # this is the title of the window

    surface = pygame.Surface(game_window.get_size())
    surface = surface.convert() # surface that gets updated whenever action performed
    fonttext = pygame.font.SysFont("Calibri", 20)

    # initialize
    s = snake()
    f = food()    

    paused = False
    while True:
        clock.tick(fps) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    paused = not paused # switch to true or false with single key
                elif paused == False:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        s.turn(up)
                    elif event.key ==pygame.K_LEFT or event.key == pygame.K_a:
                        s.turn(left)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        s.turn(right)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        s.turn(down)
        draw_bg(surface)
        s.move(paused) # keeps snake in motion
        if s.get_head_position() == f.spawn: # overlap the position then you start counting
            s.score += 1
            s.length += 1
            f.respawn()
        s.draw(surface)
        f.draw(surface)
        game_window.blit(surface, (0,0))     

        banner = pygame.Surface((window_x, 40))
        banner.fill((50,50,50))
        game_window.blit(banner, (0,0))
        
        score_text = fonttext.render("Score: {0}".format(s.score),1, (255,255,255))
        game_window.blit(score_text, ((window_x/2)-gridsize*2, 10))
        pygame.display.update()

if __name__ == "__main__":
    main()

