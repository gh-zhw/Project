from interface import Window


WIDTH = 600
HEIGHT = 400
title = '汉字识别'

window = Window(WIDTH, HEIGHT, title)

quit = False
while not quit:
    quit = window.update()
