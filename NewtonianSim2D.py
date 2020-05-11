# Basic Newtonian body simulation
# Units are in meters and kilograms

import time
import os
import numpy as np
from numpy import linalg as LA
import pygame
import pygame_gui

# parameters
scale = 1
fps = 60
worldsize = 3 * 10 ** 11  # side length
resolution = 300  # Screen starts as square of this size
ticklength = 500
G = 6.67408 * 10 ** -11
black = (0, 0, 0)

# bodies (radius, velocity, position, mass, color)
'''bodies = np.array([[[696340], [0, 0], [0, 0], [1.989 * 10 ** 30], [255, 255, 0]],
                   [[6371], [0, 29.78 * 10 ** 3], [1.496 * 10 ** 11, 0], [5.972 * 10 ** 24], [0, 0, 255]]])'''

init_row = np.array([[[-1], [0, 0], [0, 0], [0], [0, 0, 0]]])
bodies = np.array([[[-1], [0, 0], [0, 0], [0], [0, 0, 0]]])

# setup

timer = time.time()
frametimer = time.time()
timeelapsed = 0
done = False
paused = True

# initialize the screen + ui elements

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (366, 30)
pygame.init()

screen = pygame.display.set_mode((resolution, resolution))
pygame.display.set_caption("Newton")
objects = pygame.Surface((resolution, resolution))
paths = pygame.Surface((resolution, resolution))

paths.set_colorkey(black)
paths.fill(black)
objects.set_colorkey(black)

start_manager = pygame_gui.UIManager((resolution, resolution))
start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((int(resolution / 2 - 50), int(resolution / 2 - 25)), (100, 50)),
    text='start',
    manager=start_manager)

menu_manager = pygame_gui.UIManager((resolution, resolution))
settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-98, -38), (100, 40)),
                                        text='settings',
                                        manager=menu_manager,
                                        anchors={'left': 'right',
                                                 'right': 'right',
                                                 'top': 'bottom',
                                                 'bottom': 'bottom'})
add = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-98, -38), (100, 40)),
                                        text='add',
                                        manager=menu_manager,
                                        anchors={'left': 'right',
                                                 'right': 'right',
                                                 'top': 'bottom',
                                                 'bottom': 'bottom'})
pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-290, -38), (100, 40)),
                                                       text='start',
                                                       manager=menu_manager,
                                                       anchors={'left': 'right',
                                                                'right': 'right',
                                                                'top': 'bottom',
                                                                'bottom': 'bottom'})

text_manager = pygame_gui.UIManager((resolution, resolution))
textinput = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (resolution, 0)),
                                                                   manager=text_manager)
textinput.set_allowed_characters('numbers')
prompt = pygame_gui.elements.ui_text_box.UITextBox(html_text='Screen resolution',
                                                   relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                                                   manager=text_manager)

# functions

def draw():
    screen.fill(black)
    objects.fill(black)

    if ui > 10 and bodies[0][0][0] != -1:
        for i in range(bodies.shape[0]):
            x = int(resolution * (bodies[i][2][0] / worldsize) + resolution / 2)
            y = int(-resolution * (bodies[i][2][1] / worldsize) + resolution / 2)
            paths.set_at((x, y), (255, 0, 0))
            pygame.draw.circle(objects, (int(bodies[i][4][0]), int(bodies[i][4][1]), int(bodies[i][4][2])), (x, y),
                               int(scale * resolution * (bodies[i][0][0] / worldsize)))

        screen.blit(paths, (0, 0))
        screen.blit(objects, (0, 0))

    if ui == 0:
        start_manager.draw_ui(screen)
    if 0 < ui < 9:
        text_manager.draw_ui(screen)
    if ui == 11:
        menu_manager.draw_ui(screen)

    pygame.display.flip()


# main loop

ui = 0 # current ui screen
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start:
                    ui += 1

                if event.ui_element == settings:
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(html_text='Screen resolution',
                                                                       relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                                                                       manager=text_manager)
                    ui = 1

                if event.ui_element == add:
                    if bodies[0][0][0] != -1:
                        bodies = np.append(bodies, init_row, axis = 0)
                    print(bodies)
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(html_text='Enter object position (m) in format x, y',
                                                                       relative_rect=pygame.Rect((-3, 24),(resolution + 6, 35)),
                                                                       manager=text_manager)
                    ui = 3

                if event.ui_element == pause:
                    if paused == True:
                        text = 'pause'
                    else:
                        text = 'start'
                    menu_manager = pygame_gui.UIManager((resolution, resolution))
                    pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-290, -38), (100, 40)),
                                                         text=text,
                                                         manager=menu_manager,
                                                         anchors={'left': 'right',
                                                                  'right': 'right',
                                                                  'top': 'bottom',
                                                                  'bottom': 'bottom'})
                    settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-98, -38), (100, 40)),
                                                            text='settings',
                                                            manager=menu_manager,
                                                            anchors={'left': 'right',
                                                                     'right': 'right',
                                                                     'top': 'bottom',
                                                                     'bottom': 'bottom'})
                    add = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-194, -38), (100, 40)),
                                                       text='add',
                                                       manager=menu_manager,
                                                       anchors={'left': 'right',
                                                                'right': 'right',
                                                                'top': 'bottom',
                                                                'bottom': 'bottom'})
                    paused = not(paused)

            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                text = textinput.get_text()
                if ui == 3:
                    bodies[bodies.shape[0] - 1][2][0] = float(text.split(',')[0])
                    bodies[bodies.shape[0] - 1][2][1] = float(text.split(',')[1])
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(
                        html_text='Enter object velocity (m/s) vector in format x, y',
                        relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                        manager=text_manager)
                    textinput.set_text('')
                    ui = 4

                elif ui == 4:
                    bodies[bodies.shape[0] - 1][1][0] = float(text.split(',')[0])
                    bodies[bodies.shape[0] - 1][1][1] = float(text.split(',')[1])
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(
                        html_text='Enter object mass (kg)',
                        relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                        manager=text_manager)
                    textinput.set_text('')
                    ui = 5

                elif ui == 5:
                    bodies[bodies.shape[0] - 1][3][0] = float(text)
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(
                        html_text='Enter displayed object color in format r, g, b',
                        relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                        manager=text_manager)
                    textinput.set_text('')
                    ui = 6

                elif ui == 6:
                    bodies[bodies.shape[0] - 1][4][0] = float(text.split(',')[0])
                    bodies[bodies.shape[0] - 1][4][1] = float(text.split(',')[1])
                    bodies[bodies.shape[0] - 1][4][2] = float(text.split(',')[2])
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(
                        html_text='Enter displayed object radius (m)',
                        relative_rect=pygame.Rect((-3, 24), (resolution + 6, 35)),
                        manager=text_manager)
                    textinput.set_text('')
                    ui = 7

                elif ui == 7:
                    bodies[bodies.shape[0] - 1][0][0] = float(text)
                    textinput.set_text('')
                    ui = 11
                    print(bodies)

                elif ui == 8:
                    worldsize = int(text)
                    textinput.set_text('')
                    ui = 11

                elif ui == 1:
                    resolution = int(text)
                    screen = pygame.display.set_mode((resolution, resolution))
                    objects = pygame.Surface((resolution, resolution))
                    paths = pygame.Surface((resolution, resolution))
                    start_manager = pygame_gui.UIManager((resolution, resolution))
                    text_manager = pygame_gui.UIManager((resolution, resolution))
                    textinput = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                        relative_rect=pygame.Rect((0, 0), (resolution, 0)),
                        manager=text_manager)
                    prompt = pygame_gui.elements.ui_text_box.UITextBox(html_text='Enter world size (m)',
                                                                       relative_rect=pygame.Rect((-3, 24),(resolution + 6, 35)),
                                                                       manager=text_manager)
                    menu_manager = pygame_gui.UIManager((resolution, resolution))
                    settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-98, -38), (100, 40)),
                                                            text='settings',
                                                            manager=menu_manager,
                                                            anchors={'left': 'right',
                                                                     'right': 'right',
                                                                     'top': 'bottom',
                                                                     'bottom': 'bottom'})
                    add = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-194, -38), (100, 40)),
                                                       text='add',
                                                       manager=menu_manager,
                                                       anchors={'left': 'right',
                                                                'right': 'right',
                                                                'top': 'bottom',
                                                                'bottom': 'bottom'})
                    pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-290, -38), (100, 40)),
                                                       text='start',
                                                       manager=menu_manager,
                                                       anchors={'left': 'right',
                                                                'right': 'right',
                                                                'top': 'bottom',
                                                                'bottom': 'bottom'})
                    paths.set_colorkey(black)
                    paths.fill(black)
                    objects.set_colorkey(black)
                    ui = 8

        start_manager.process_events(event)
        text_manager.process_events(event)
        menu_manager.process_events(event)


    start_manager.update(time.time() - timer) # pass time elapsed to managers
    text_manager.update(time.time() - timer)
    menu_manager.update(time.time() - timer)
    timer = time.time()

    if ui > 10 and bodies[0][0] != -1 and not paused:
        for i in range(bodies.shape[0]):
            velocity = bodies[i][1]
            position = bodies[i][2]
            acceleration = np.array([0., 0.])

            for j in range(bodies.shape[0]):
                if j != i:
                    acceleration += (np.subtract(bodies[j][2], bodies[i][2]) * G * bodies[j][3]) / (
                        LA.norm(np.subtract(bodies[j][2], bodies[i][2]))) ** 3

            velocity += acceleration * ticklength
            position += velocity * ticklength
            bodies[i][1] = velocity
            bodies[i][2] = position

        timeelapsed += ticklength

    if time.time() - frametimer > 1 / fps:
        draw()
        # print('%s days' % (int(timeelapsed/86400)))
        frametimer = time.time()
