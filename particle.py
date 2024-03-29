import numpy as np
import pygame as pg

BOUNDARY_DAMPING = 0.6
COLLISION_DAMPING = 0.8

class Particle:
    particle_list = []
    def __init__ (self, x, y, vx, vy, mass=1, radius=10, colour=(255,255,255)):
        self.position = np.array((x, y), dtype=float)
        self.velocity = np.array((vx, vy), dtype=float)
        self.acceleration = np.array((0, 0), dtype=float)
        self.mass = mass
        self.radius = radius
        self.colour = colour

        Particle.particle_list.append(self)

        self.index = len(Particle.particle_list) - 1
    
    def apply_force(self, force=np.array((0, 0))):
        self.acceleration += force / self.mass
    
    def boundary(self, width, height):
        if self.position[0] - self.radius < 0:
            self.position[0] = 0 + self.radius
            self.velocity[0] *= -1 * BOUNDARY_DAMPING
        
        if self.position[0] + self.radius > width:
            self.position[0] = width - self.radius
            self.velocity[0] *= -1 * BOUNDARY_DAMPING
        
        if self.position[1] - self.radius < 0:
            self.position[1] = 0 + self.radius
            self.velocity[1] *= -1 * BOUNDARY_DAMPING
        
        if self.position[1] + self.radius > height:
            self.position[1] = height - self.radius
            self.velocity[1] *= -1 * BOUNDARY_DAMPING  

    @classmethod
    def reset_checked_pairs(cls):
        cls.checked_pairs = set()

    def check_collision(self):
        for other_particle in Particle.particle_list:
            if other_particle != self:
                particle_pair = frozenset([self, other_particle])

                if particle_pair not in Particle.checked_pairs:
                    distance = np.linalg.norm(self.position - other_particle.position)

                    if distance < self.radius + other_particle.radius:
                        overlap = distance - self.radius - other_particle.radius
                        self.handle_collisions_static(self, other_particle, distance, overlap)
                        self.handle_collisions(self, other_particle)

                    Particle.checked_pairs.add(particle_pair)
    
    @staticmethod
    def check_collisions_grid(particle_pair_list):

        i = 0
        distance_list = [np.linalg.norm(particle_pair[0].position - particle_pair[1].position) for particle_pair in particle_pair_list]
        rad = particle_pair_list[0][0].radius * 2
        distance_array = np.array(distance_list)
        overlap_list = distance_array - rad

        for particle_pair in particle_pair_list:
            if overlap_list[i] < 0:

                particle_1 = particle_pair[0]
                particle_2 = particle_pair[1]   

                overlap = overlap_list[i]
                
                Particle.handle_collisions_static(particle_1, particle_2, distance_list[i], overlap)
                Particle.handle_collisions(particle_1, particle_2)
            i += 1
    
    @staticmethod
    def handle_collisions_static(particle_1, particle_2, distance, overlap):
        distance_vector = (particle_1.position - particle_2.position)
        distance_vector_normalise = distance_vector / distance
        particle_1.position -= 0.5 * overlap * distance_vector_normalise
        particle_2.position += 0.5 * overlap * distance_vector_normalise

    @staticmethod
    def handle_collisions(particle_1, particle_2):
        combined_mass = particle_1.mass + particle_2.mass
        mass_term_1 = (2 * particle_2.mass) / combined_mass
        mass_term_2 = (2 * particle_1.mass) / combined_mass

        velocity_difference = (particle_1.velocity - particle_2.velocity)
        position_difference = (particle_1.position - particle_2.position)
        position_magnitde = particle_1.radius + particle_2.radius        
        position_magnitde_squared = position_magnitde**2
        dot_product_normalised = np.dot(velocity_difference, position_difference) / position_magnitde_squared

        particle_velocity_new = particle_1.velocity - (mass_term_1 * dot_product_normalised) * position_difference
        other_particle_velocity_new = particle_2.velocity - (mass_term_2 * dot_product_normalised) * -position_difference

        particle_1.velocity = particle_velocity_new * COLLISION_DAMPING
        particle_2.velocity = other_particle_velocity_new * COLLISION_DAMPING

    def update(self, dt):
        self.velocity += self.acceleration * dt

        self.position += self.velocity * dt
        self.acceleration = np.array((0,0), dtype=float)
    
    def draw(self, screen):
        x = self.position[0]
        y = self.position[1]
        
        pg.draw.circle(screen, self.colour, (int(x), int(y)), self.radius)
