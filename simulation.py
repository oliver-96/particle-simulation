from schema import static
from multiprocessing import Process, Queue
import time


settings_dict = static.SIM_SETTINGS

width = settings_dict['WIDTH']
height = settings_dict['HEIGHT']
sub_step = settings_dict['SUB_STEP']
collision_type = settings_dict['COLLISION_TYPE']

def simulation_loop(Particle, grid, gravity, dt):
    Particle.reset_checked_pairs()   
    if collision_type == 'grid_infinite':
        if Particle.particle_list:
            grid.initalise_tables(Particle.particle_list[0].radius * 2, len(Particle.particle_list))
        
    for _ in range(sub_step):
        for particle in Particle.particle_list:
            particle.apply_force(gravity)
            particle.update(dt / sub_step)
            particle.boundary(width, height)
            if collision_type == 'loop':
                particle.check_collision()
        
        if collision_type == 'grid_infinite':
            if len(Particle.particle_list) > 1:
                [grid.position_to_cell_coordinates(particle) for particle in Particle.particle_list]
                grid.hash_coord_particle_index_sort()
                grid.create_start_index_table()
                grid.check_particles(Particle)

        start_time = time.time()
        if collision_type == 'grid_finite':
            if len(Particle.particle_list) > 1:
                grid.reset()
                start_location = time.time()
                [grid.particle_location(particle) for particle in Particle.particle_list]
                end_location = time.time()
                total_location = end_location - start_location
                # print(f"Location: {total_location} seconds")

                start_pairs = time.time()
                particles_to_check = grid.check_particles()
                end_pairs = time.time()

                total_pairs = end_pairs - start_pairs
                # print(f"Pairs: {total_pairs} seconds")

                start_dist = time.time()
                Particle.check_collisions_grid(particles_to_check)
                end_dist = time.time()
                total_dist = end_dist - start_dist
                print(f"Distance: {total_dist} seconds")

        end_time = time.time()
        total = end_time - start_time
        print(f"Total Collision: {total} seconds")