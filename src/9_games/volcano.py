''' Simulate volcanoes on planets in the solar system'''

import pygame

# ======================================================================
#                           INPUTS:
# ======================================================================

# ======================================================================
#                           FUNCTIONS:
# ======================================================================

class Game:
    # TODO: display a clock at the top right corner of the screen
    ''' a class to define the game window'''
    def __init__(self,):
        ''' construct the game window'''
        pygame.init()
        self.screen = pygame.display.set_mode(1280, 780)
        self.clock = pygame.time.clock()
        

    def main_loop(self,):
        ''' define the main loop fo the program'''
        running = True
        while running:
            pygame.display.flip()
        pygame.quit()

class Settings:
    ''' defines settings for the program'''
    def __init__(self,):
        ''' settings constructor'''
        self.particle_size = 50
        self.velocity_spread = .2
        self.angle_spread = .2


class Planet:
    ''' a class to create eruptions'''
    def __init__(self, settings: Settings):
        self.particles = []

    def eruption_cycle(self,):
        ''' keep erupting over a short timeframe, then stop to recover'''
        pass

    def erupt(self,):
        ''' generate many different particles at once'''
        pass

    def create_particle(self,):
        ''' generate a new particle in the starting position, with 
            randomized absolute velocities and velocity vectors'''
        self.particles.append(Particle())

    def draw(self,):
        ''' draws the planet graphic as well as all particles'''


class Particle:
    ''' a class to keep track of particle positions and velocity vectors'''
    def __init__(self, settings):
        self.position = (0,0)
        self.velocity = (1,0)
        self.rect = pygame.Rect(
            left=self.position[0], top=self.position[1],
            width= settings.particle_size, height=setttings.particle_size
        )

    def update_position(self, acceleration):
        ''' updates the position of a particle. If particle collides with
            planet surface, destroy the particle
        '''
        pass

    def draw(self):
        ''' draws the particle on the screen'''
        pass


    
# ======================================================================
#                           DRIVER CODE:
# ======================================================================

def main():
    ''' driver code'''
    # initialize the screen
    game = Game()
    # initialize a planet object


    # planet has a function erupt that generates an eruption
    # erupt should be triggered at regular intervals
    # erupt generates particle objects over a given time period
    game.main_loop()

if __name__ == '__main__':
    main()