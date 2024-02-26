
from schema import static

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

        if collision_type == 'grid_finite':
            if len(Particle.particle_list) > 1:
                grid.reset()
                [grid.particle_location(particle) for particle in Particle.particle_list]
                grid.check_particles()