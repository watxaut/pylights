import sys
import time
import logging

import pygame

import pylights.model as model
from pylights.config import WINDOW_SIZE, NUM_LIGHTS, LIGHT_SIZE, BACKGROUND, DELTA_TIME, M_FPS

logger = logging.getLogger(__name__)


def start():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.FULLSCREEN)

    lights = model.Lights()
    lights.create_lights(NUM_LIGHTS)
    lights.set_delta_time(DELTA_TIME)

    reverse = False

    while 1:
        t_start = time.time() * 1000
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
        t_diff = time.time() * 1000 - t_start
        if t_diff < M_FPS:  # 16.67:  # 60 FPS
            pygame.time.wait(M_FPS - int(t_diff))
