import pygame
from pygame.locals import KEYDOWN, K_ESCAPE

pygame.font.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

word_size = 28    # 汉字像素
grid_size = 400
spot_size = grid_size // word_size


class Spot:
    def __init__(self, r, c, spot_size):
        self.r = r
        self.c = c
        self.x = c * spot_size
        self.y = r * spot_size
        self.spot_size = spot_size
        self.color = WHITE

    def render(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.spot_size, self.spot_size))

    def write_spot(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = BLACK
        self.background = WHITE

    def render(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), width=2, border_radius=5)

        font = pygame.font.SysFont('SimHei', 20)
        surface = font.render(self.text, False, BLACK, self.background)
        window.blit(surface, (self.x+20, self.y+5))

    def clicked(self):
        if self.text == 'save':
            self.background = GREEN
        elif self.text == 'clear':
            self.background = RED

    def reset(self):
        self.background = WHITE


class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.word_grid = []
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.window.fill(WHITE)
        self.save_button = Button(450, 100, 80, 30, 'save')
        self.clear_button = Button(450, 150, 80, 30, 'clear')

        # make word grid
        for i in range(word_size):
            self.word_grid.append([])
            for j in range(word_size):
                self.word_grid[i].append(Spot(i, j, spot_size))

    def update(self):
        self.save_button.render(self.window)
        self.clear_button.render(self.window)

        # render spots
        for i in range(word_size):
            for j in range(word_size):
                spot = self.word_grid[i][j]
                spot.render(self.window)

        self.act()

        # draw lines
        for i in range(word_size + 1):
            pygame.draw.line(self.window, BLACK, (0, i * spot_size), (word_size * spot_size, i * spot_size))
            pygame.draw.line(self.window, BLACK, (i * spot_size, 0), (i * spot_size, word_size * spot_size))

        pygame.display.update()
        return self.quit()

    def act(self):
        for event in pygame.event.get():
            left, center, right = pygame.mouse.get_pressed()
            if left:
                position = pygame.mouse.get_pos()
                x, y = position
                if 0 < x < grid_size and 0 < y < grid_size:
                    r, c = self.pos_to_spot(position)
                    # print(r, c, 'clicked')
                    clicked_spot = self.word_grid[r][c]
                    clicked_spot.write_spot()
                    self.save_button.reset()
                    self.clear_button.reset()
                elif 450 < x < 530 and 100 < y < 130:
                    self.save_button.clicked()
                    self.reset_grid()
                elif 450 < x < 530 and 150 < y < 180:
                    self.clear_button.clicked()
                    self.reset_grid()

    def reset_grid(self):
        for i in range(word_size):
            for j in range(word_size):
                self.word_grid[i][j].reset()

    def pos_to_spot(self, position):
        x, y = position
        r, c = y // spot_size, x // spot_size
        return r, c

    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True




