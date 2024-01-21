OFFSET = [-1, 0, 1]
HASH_TABLE_MULTIPLE = 5

class Grid:
    def __init__(self, cell_size=0, num_particles=0):
        self.cell_size = cell_size
        self.table_size = num_particles

        self.hash_coordinate_table = []
        self.particle_index_table = []
        self.cell_coordinate_table = []
        self.start_index_hash_table = []

    @staticmethod
    def cell_to_hash_coordinates(cell_x, cell_y, table_size):
        hash = (cell_x * 92837111) + (cell_y * 689287499)
        hash_coordinates = abs(hash) % (table_size * HASH_TABLE_MULTIPLE)

        return hash_coordinates
    
    def initalise_tables(self, cell_size, num_particles):
        self.cell_size = cell_size
        self.table_size = num_particles
        self.hash_coordinate_table = [0] * self.table_size
        self.particle_index_table = [0] * self.table_size
        self.cell_coordinate_table = [0] * self.table_size
        self.start_index_hash_table = [-1] * self.table_size * HASH_TABLE_MULTIPLE

    def position_to_cell_coordinates(self, particle):
        cell_coordinate_table_index = particle.index
        cell_x = (int(particle.position[0]) // self.cell_size)
        cell_y = (int(particle.position[1]) // self.cell_size)

        self.cell_coordinate_table[cell_coordinate_table_index] = [cell_x, cell_y]

        hash_coordinates = Grid.cell_to_hash_coordinates(cell_x, cell_y, self.table_size)

        self.hash_coordinate_table[cell_coordinate_table_index] = hash_coordinates
        self.particle_index_table[cell_coordinate_table_index] = cell_coordinate_table_index

    def hash_coord_particle_index_sort(self):
        combined_tables = list(zip(self.hash_coordinate_table, self.particle_index_table))
        combined_tables.sort()
        self.hash_coordinate_table, self.particle_index_table = map(list, zip(*combined_tables))
    
    def create_start_index_table(self):
        i = 0
        checked_hash_coordinates = set()

        for hash_coordinate in self.hash_coordinate_table:
            if hash_coordinate not in checked_hash_coordinates:
                self.start_index_hash_table[hash_coordinate] = i
            checked_hash_coordinates.add(hash_coordinate)
            i += 1
    
    def check_particles(self, particles):
        for particle in particles.particle_list:
            cell_coordinate = self.cell_coordinate_table[particle.index]

            for x_offset in OFFSET:
                for y_offset in OFFSET:
                    
                    cell_coordinate_check_x = cell_coordinate[0] + x_offset
                    cell_coordinate_check_y = cell_coordinate[1] + y_offset

                    current_hash_coordinate = Grid.cell_to_hash_coordinates(cell_coordinate_check_x, cell_coordinate_check_y, self.table_size) 

                    start_index = self.start_index_hash_table[current_hash_coordinate]

                    if start_index == -1:
                        continue
                    
                    for i in range(start_index, self.table_size):
                        if self.hash_coordinate_table[i] != current_hash_coordinate:
                            break
                        
                        other_particle_index = self.particle_index_table[i]

                        if other_particle_index == particle.index:
                            continue

                        other_particle = particles.particle_list[other_particle_index]
                        particles.check_collisions_grid(particle, other_particle)