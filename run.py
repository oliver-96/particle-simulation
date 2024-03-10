import pygame as pg
import sys
import math
import time

from schema import static
from particle import Particle
from grid import InfiniteGrid, FiniteGrid
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
    radius = 10

    if static.SIM_SETTINGS['COLLISION_TYPE'] == 'grid_infinite':
        grid = InfiniteGrid()
    elif static.SIM_SETTINGS['COLLISION_TYPE'] == 'grid_finite':
        grid = FiniteGrid(radius * 2, width, height)
    else:
        grid = None
    i = 0

    # Other setup
    average_fps = AverageFps(1, target_fps)

    # Main loop
    while True:
        total_start = time.time()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        # Reset screen
        screen.fill((0, 0, 0))

        # Get average FPS
        average_fps.calculate_avg_fps(clock.get_fps())
        # average_fps.print_avg_fps_and_particle(Particle)

        # Generate particles
        if i % 10 == 0 and average_fps.current_average_fps > min_fps:
            T = 300
            xv = 150 * math.sin(2 * math.pi * i / T)
            Particle(width / 2 + 20, height * 0.05, xv, 300, radius=radius)
            Particle(width / 2 - 20, height * 0.05, -xv, 300, radius=radius)

        # Simulate particles
        simulation_loop(Particle, grid, gravity, dt)

        # Draw particles
        [particle.draw(screen) for particle in Particle.particle_list]
        
        # Update screen
        pg.display.flip()
        clock.tick(target_fps)
        i += 1

        total_end = time.time()

        total = total_end - total_start
        print(f'Particles = {len(Particle.particle_list)}')
        # print(f"Total: {total} seconds")

if __name__ == '__main__':
    run()










