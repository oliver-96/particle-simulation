import pygame as pg
import sys
import math

from schema import static
from particle import Particle
from grid import Grid
from forces import gravity_force
from utils import start_up_title, AverageFps
from simulation import simulation_loop

settings_dict = static.SIM_SETTINGS
width = settings_dict['WIDTH']
height = settings_dict['HEIGHT']
target_fps = settings_dict['TARGET_FPS']
min_fps = settings_dict['MIN_FPS']
sub_step = settings_dict['SUB_STEP']
collision_type = settings_dict['COLLISION_TYPE']


def run():
    # Generate title
    start_up_title(collision_type, target_fps, sub_step)

    # Pygame Setup
    pg.init()
    screen = pg.display.set_mode((width, height))

    clock = pg.time.Clock()

    # World Setup
    dt = 1 / target_fps
    gravity = gravity_force(3)
    grid = Grid()
    i = 0

    # Other setup
    average_fps = AverageFps(1, target_fps)

    # Main loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        # Reset screen
        screen.fill((0, 0, 0))

        # Get average FPS
        average_fps.calculate_avg_fps(clock.get_fps())
        average_fps.print_avg_fps_and_particle(Particle)

        # Generate particles
        if i % 3 == 0 and average_fps.current_average_fps > min_fps:
            T = 300
            xv = 150 * math.sin(2 * math.pi * i / T)
            Particle(width / 2 + 20, height * 0.05, xv, 300, radius=5)
            Particle(width / 2 - 20, height * 0.05, -xv, 300, radius=5)

        # Simulate particles
        simulation_loop(Particle, grid, gravity, dt)

        # Draw particles
        [particle.draw(screen) for particle in Particle.particle_list]
        
        # Update screen
        pg.display.flip()
        clock.tick(target_fps)
        i += 1

if __name__ == '__main__':
    run()










