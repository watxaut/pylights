import sys

import pygame

import pylights.model as model
from pylights.config import WINDOW_SIZE, NUM_LIGHTS, LIGHT_SIZE, BACKGROUND


def start():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.FULLSCREEN)

    lights = model.Lights()
    lights.create_lights(NUM_LIGHTS)

    reverse = False

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                reverse = True
            elif event.type == pygame.MOUSEBUTTONUP:
                reverse = False
        screen.fill(BACKGROUND)

        mouse_pos = pygame.mouse.get_pos()
        lights.refresh_lights_position(mouse_pos, reverse)

        [pygame.draw.circle(screen, light.color, light.pos, LIGHT_SIZE) for light in lights]

        pygame.display.flip()
