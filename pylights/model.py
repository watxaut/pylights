import logging
import random

from pylights.config import MAX_VEL, MAX_ACC, MASS_PRODUCT, WINDOW_SIZE

logger = logging.getLogger(__name__)


def sum_tuples(a, b):
    return a[0] + b[0], a[1] + b[1]


def subtract_tuples(a, b):
    return a[0] - b[0], a[1] - b[1]


def print_debug(func):
    def decorator(*args, **kwargs):
        self = args[0]
        logger.info(f"Acc before: {self.acc}")
        logger.info(f"Vel before: {self.vel}")
        logger.info(f"Pos before: {self.pos}")
        out = func(*args, **kwargs)
        logger.info(f"Acc after: {self.acc}")
        logger.info(f"Vel after: {self.vel}")
        logger.info(f"Pos after: {self.pos}")
        return out

    return decorator


class Light:
    def __init__(self, window_size):
        self.acc: tuple = (0, 0)
        self.window_size: tuple = window_size
        x_init_dir = random.random() * 2 - 1
        y_init_dir = random.random() * 2 - 1
        mod_init_dir = (x_init_dir ** 2 + y_init_dir ** 2) ** 0.5
        init_vel = random.randint(1, 20)
        self.vel: tuple = (x_init_dir * init_vel / mod_init_dir, y_init_dir * init_vel / mod_init_dir)
        # self.vel: tuple = (random.randint(-20, 20), random.randint(-20, 20))
        self.pos: tuple = (window_size[0] // 2, window_size[1] // 2)
        self.color: tuple = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    @print_debug
    def move(self, mouse_position, reverse):
        self.update_acceleration(mouse_position, reverse)
        self.update_velocity()
        self.try_move_wall()
        self.pos = [int(i) for i in sum_tuples(self.pos, self.vel)]

    def try_move_wall(self):
        try_pos = [int(i) for i in sum_tuples(self.pos, self.vel)]
        if try_pos[0] < 0 or try_pos[0] > self.window_size[0]:
            self.vel = (-self.vel[0], self.vel[1])

        if try_pos[1] < 0 or try_pos[1] > self.window_size[1]:
            self.vel = (self.vel[0], -self.vel[1])

    def update_velocity(self):
        x_vel, y_vel = sum_tuples(self.vel, self.acc)

        mod_new_vel = (x_vel ** 2 + y_vel ** 2) ** 0.5
        if mod_new_vel > MAX_VEL:
            x_vel = x_vel / mod_new_vel * MAX_VEL
            y_vel = y_vel / mod_new_vel * MAX_VEL
        self.vel = (x_vel, y_vel)

    def update_acceleration(self, mouse_position, reverse):
        director_vec = subtract_tuples(mouse_position, self.pos)  # points to the mouse
        if reverse:
            director_vec = (-director_vec[0], -director_vec[1])
        module_vec = (director_vec[0] ** 2 + director_vec[1] ** 2) ** 0.5
        if module_vec == 0:
            module_vec = 0.01
        gravitation_force = MASS_PRODUCT / module_vec
        x_acc = gravitation_force * director_vec[0] / module_vec
        y_acc = gravitation_force * director_vec[1] / module_vec

        mod_new_acc = (x_acc ** 2 + y_acc ** 2) ** 0.5
        if mod_new_acc > MAX_ACC:
            x_acc = x_acc / mod_new_acc * MAX_ACC
            y_acc = y_acc / mod_new_acc * MAX_ACC

        self.acc = (x_acc, y_acc)


class Lights:
    lights = None

    def create_lights(self, number_of_lights):
        self.lights = [Light(WINDOW_SIZE) for _ in range(number_of_lights)]

    def refresh_lights_position(self, mouse_position, reverse):
        for light in self.lights:
            light.move(mouse_position, reverse)

    def __iter__(self):
        for light in self.lights:
            yield light
