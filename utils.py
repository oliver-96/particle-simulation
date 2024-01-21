import art

def start_up_title(collision_type, target_fps, sub_step):
    heading_banner = '=' * 45
    settings_banner = '-' * 22
    heading_text = 'Particle  Sim'
    heading_font = 'big'

    print(heading_banner)
    heading = art.text2art(heading_text, font = heading_font, chr_ignore=True)
    print(heading.rstrip())
    print(heading_banner)

    print('Settings')
    print(settings_banner)
    print(f'Collision Type = {collision_type}')
    print(f'Target FPS = {target_fps}')
    print(f'Sub Steps = {sub_step}')
    print(settings_banner)

class AverageFps:
    def __init__(self, moving_average_length, target_fps):
        self.moving_average_length = moving_average_length
        self.target_fps = target_fps
        self.fps_list = [target_fps] * moving_average_length
        self.current_average_fps = sum(self.fps_list) / self.moving_average_length
        self.i = 0
    
    def calculate_avg_fps(self, current_fps):
        self.fps_list[self.i] = current_fps
        self.i += 1
        if self.i % self.moving_average_length == 0:
            self.i = 0
        self.current_average_fps = sum(self.fps_list) / self.moving_average_length
    
    def print_avg_fps_and_particle(self, Particle):
        print(f'Average FPS = {self.current_average_fps:.0f} | Particles = {len(Particle.particle_list)}', end="\r")

