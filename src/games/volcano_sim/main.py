''' Simulate volcanoes on planets in the solar system'''

import pygame
from games.volcano_sim.settings import Settings
from games.volcano_sim.coord_converter import CoordConverter
from games.volcano_sim.pyclock import PyClock
from games.volcano_sim.planet import Planet, Map
from games.volcano_sim.particle import Particle
from games.volcano_sim.volcano import Volcano

# ==========================================================================
#                         HIGHEST-LEVEL CLASS
# ==========================================================================

#TODO: for some reason, the length of the particles increases/decreases with speed!
#TODO: for some reason, negative gravities are not tolerated

class Game(CoordConverter):
    ''' a class to define the game window'''
    def __init__(self, game_map: Map, settings: Settings, clock: PyClock):
        ''' construct the game window'''
        super().__init__(settings)
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = clock
        self.game_map = game_map


    def main_loop(self,):
        ''' define the main loop fo the program'''  
        self.clock.clock.tick(1)  # TODO: set FPS to 60
        running = True
        while running:
            if self.check_player_quits():
                running = False
            self.game_map.blit_volcano()
            self.screen.blit(self.game_map.background, (0,0))
            self.game_map.blit_planet()
            self.blit_screen()
            pygame.display.flip()

            self.game_map.eruptor.destroy_out_of_bounds()
            self.game_map.eruptor.erupt()
            self.game_map.eruptor.update_particle_velocities()
            self.game_map.eruptor.update_particle_positions()
        pygame.quit()


    def check_player_quits(self):
        ''' grab the inputs connected to this frame'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        current_keys = pygame.key.get_pressed()
        if current_keys[pygame.K_x]:  # if x is pressed
            return True
        return False


    def blit_screen(self):
        ''' pblits the default background'''
        self.screen.blit(self.game_map.background, dest=(0,0))
        self.game_map.refresh_background()

# ======================================================================
#                           DRIVER CODE:
# ======================================================================

def main():
    ''' driver code'''
    pygame.font.init()
    settings = Settings()
    default_particle = Particle(settings)
    volcano = Volcano(settings, default_particle)
    clock = PyClock(settings)
    planet = Planet(volcano, settings, clock)
    game = Game(planet, settings, clock)
    game.main_loop()


if __name__ == '__main__':
    main()
