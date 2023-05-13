import pygame
import torch
from pygame.locals import KEYDOWN, K_ESCAPE
import numpy as np
from PIL import Image
from torchvision import transforms
from model import CNN
from dataset import idx_to_class

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

word_size = 28  # 汉字像素
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


class Text:
    def __init__(self, x, y, message, font_size, font_color, background):
        self.x = x
        self.y = y
        self.message = message
        self.font_size = font_size
        self.font_color = font_color
        self.background = background

    def render(self, window, message=None):
        if message:
            self.message = message
        font = pygame.font.SysFont('SimHei', self.font_size)
        text = font.render(self.message, True, self.font_color, self.background)
        window.blit(text, (self.x+10, self.y+5))


class Button:
    def __init__(self, x, y, width, height, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = Text(self.x, self.y, text, 15, BLACK, WHITE)
        self.color = BLACK
        self.background = WHITE

    def render(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), width=2, border_radius=5)
        self.text.render(window)

    def clicked(self):
        if self.text.message == 'save':
            self.text.background = GREEN
        elif self.text.message == 'clear':
            self.text.background = RED
        elif self.text.message == 'predict':
            self.text.background = ORANGE

    def reset(self):
        self.text.background = WHITE


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
        self.pre_button = Button(450, 300, 80, 30, 'predict')
        self.text = Text(470, 220, '', 30, TURQUOISE, GREY)
        self.model = None

        # 保存图像时用
        self.index = 0

        # make word grid
        for i in range(word_size):
            self.word_grid.append([])
            for j in range(word_size):
                self.word_grid[i].append(Spot(i, j, spot_size))

    def update(self):
        self.save_button.render(self.window)
        self.clear_button.render(self.window)
        self.pre_button.render(self.window)

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
                # click grid
                if 0 < x < grid_size and 0 < y < grid_size:
                    r, c = self.pos_to_spot(position)
                    # print(r, c, 'clicked')
                    clicked_spot = self.word_grid[r][c]
                    clicked_spot.write_spot()
                    self.save_button.reset()
                    self.clear_button.reset()
                    self.pre_button.reset()
                # click save button
                elif 450 < x < 530 and 100 < y < 130:
                    self.save_button.clicked()
                    # self.save_word_image()
                    self.reset_grid()
                    self.clear_button.reset()
                    self.pre_button.reset()
                # click clear button
                elif 450 < x < 530 and 150 < y < 180:
                    self.clear_button.clicked()
                    self.reset_grid()
                    self.save_button.reset()
                    self.pre_button.reset()
                # click predict button
                elif 450 < x < 530 and 300 < y < 330:
                    self.pre_button.clicked()
                    pred = self.predict()
                    self.text.render(self.window, pred)
                    self.save_button.reset()
                    self.clear_button.reset()
                else:
                    self.save_button.reset()
                    self.clear_button.reset()
                    self.pre_button.reset()

    def predict(self):
        if self.model is None:
            print('load model...')
            self.model = CNN(28, 1, 8)
            self.model.load_state_dict(torch.load('./model/model_acc_1.0.pth'))
        word_image = self.grid2image()
        transform = transforms.ToTensor()
        image = transform(word_image).unsqueeze(0).float()
        output = self.model(image)
        pred = torch.argmax(output).item()
        return idx_to_class[pred]

    def grid2image(self):
        grid_image = []
        for i in range(word_size):
            grid_image.append([])
            for j in range(word_size):
                grid_image[i].append(int(self.word_grid[i][j].color == BLACK) * 255)
        return Image.fromarray(np.asarray(grid_image))

    def save_word_image(self):
        word_image = self.grid2image()
        word_name = '王'
        word_image.convert('L').save(f'./dataset/{word_name}/{self.index}.jpg')
        print(f'save {word_name}/{self.index}.jpg')
        self.index += 1

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
