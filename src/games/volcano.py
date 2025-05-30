''' Simulate volcanoes on planets in the solar system'''

import pygame

# ======================================================================
#                           INPUTS:
# ======================================================================

PARTICLE_SIZE = 50
VELOCITY_SPREAD = .2
ANGLE_SPREAD = .2
WINDOW_SIZE = (1280, 780)

# ======================================================================
#                           FUNCTIONS:
# ======================================================================

def get_abs_pixels(
    relative_dimension: float | tuple[float,float],
    absolute_size = tuple[int,int], use_x_dimension: bool = True
) -> int:
    ''' generates the absolute pixel count based on relative pixels.
        if x_dimension is tuple,  x_dimension specifies
        if x_dimension == True, outputs x values, if False, outputs y values
    '''
    if isinstance(relative_dimension, tuple):
        if use_x_dimension:
            return int(relative_dimension[0] * absolute_size[0])
        return int(relative_dimension[1] * absolute_size[1])
    if use_x_dimension:
       return int(relative_dimension * absolute_size[0])
    return int(relative_dimension * absolute_size[1])

def to_pygame_coords(coords: tuple[float, float]):
    ''' convert a coordinate tuple to pygame coordinates'''
    max_x = WINDOW_SIZE[0]
    max_y = WINDOW_SIZE[1]
    x, y = coords
    x = int(x * max_x)
    y = int((1 - y) * max_y)
    return (x, y)


class Game:
    # TODO: display a clock at the top right corner of the screen
    ''' a class to define the game window'''
    def __init__(self, size: tuple[int, int]):
        ''' construct the game window'''
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.planet = Planet()
        self.background = pygame.Surface(size)


    def main_loop(self,):
        ''' define the main loop fo the program'''  
        self.clock.tick(60)  # set FPS to 60
        running = True
        while running:
            if self.check_player_quits():
                running = False
            self.planet.eruption_cycle()
            self.planet.destroy_out_of_bounds()
            self.planet.update_particle_movements()
            self.draw_images()
            pygame.display.flip()
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

    def draw_images(self):
        ''' update the positions of all the particles in the game at '''
        self.screen.blit(self.background,(0,0))
        self.background.blit(self.planet.image, self.planet.box)
        for particle in self.planet.particles:
            self.background.blit(particle.image, particle.box)


class Planet:
    ''' a class to create eruptions'''
    def __init__(self, ):
        self.particles = []
        self.dimensions = (.8, .2)
        self.gravity = (0, .2)
        self._eruption_time = 0
        self._last_eruption = -1
        x_left = 1 - self.dimensions[0]
        self.box = pygame.Rect(0,0,0,0)
        self.box.left = get_abs_pixels(x_left, WINDOW_SIZE)
        self.box.top = get_abs_pixels(
            self.dimensions, WINDOW_SIZE, use_x_dimension=False
        )
        self.box.width = get_abs_pixels(self.dimensions, WINDOW_SIZE)
        self.box.height = get_abs_pixels(
            self.dimensions, WINDOW_SIZE, use_x_dimension=False
        )

        self.image = pygame.Surface(self.box[2:])
        self.image.fill('green')


    def eruption_cycle(
        self, erupt_frequency: float = 1.0,
        max_duration: int = 60, wait_time: int = 300
    ):
        ''' keep erupting over a short timeframe, then stop to recover'''
        if self._eruption_time >= 0:
            if self._eruption_time < max_duration:
                triggers_eruption = (
                    round(self._eruption_time / erupt_frequency)
                    != self._last_eruption
                )
                if triggers_eruption:
                    self.erupt()
                    self._last_eruption = self._eruption_time
                self._eruption_time += 1
            else:
                self._eruption_time = -1
        else:
            if self._eruption_time >= -1 * wait_time:
                self._eruption_time -= 1
            else:
                self._eruption_time = 0


    def erupt(
        self, num_particles: int = 1, randomness=False, rand_settings=None
    ):
        ''' generate many different particles at once'''
        for _ in range(num_particles):
            self._create_particle(randomness, rand_settings)


    def destroy_out_of_bounds(self, ):
        '''determine whether particles are out of bounds, then destroy them'''
        for particle in self.particles:
            is_below_screen = particle.position[1] < 0
            too_far_left = particle.position[0] < 0
            too_far_right = particle.position[0] > 1
            if is_below_screen or too_far_left or too_far_right:
                self.particles.remove(particle)


    def update_particle_movements(self):
        ''' calculate the speeds at which the particles move'''
        for particle in self.particles:
            particle.update_position()
            particle.update_velocity(
                self.gravity
            )

    def _create_particle(self, randomness: bool = False, rand_settings=None):
        ''' generate a new particle in the starting position, with 
            randomized absolute velocities and velocity vectors'''
        self.particles.append(Particle(randomness, rand_settings))


class Particle:
    ''' a class to keep track of particle positions and velocity vectors'''
    def __init__(self, randomness: bool = False, rand_settings=None):
        if randomness:
            if rand_settings is None:
                print('Must specify random settings if randomness == True!')
                raise UnboundLocalError
        self._position = (0,0)  # (x, y), relative position (0 to 1)
        self._velocity = (1,0)  # (x, y), movement per pixel * 100
        self.box = pygame.Rect(0,0,0,0)
        self.box.left = self.position[0]
        self.box.top=self.position[1]
        self.box.width = PARTICLE_SIZE
        self.box.height = PARTICLE_SIZE
        self.image = pygame.Surface(self.box[2:])
        self.image.fill('red')

    @property
    def position(self):
        ''' returns the position of the particle'''
        return self._position

    @position.setter
    def position(self, new_value):
        ''' sets the new position of teh particle'''
        self._position = new_value

    @property
    def velocity(self):
        ''' returns the current speed of the particle'''
        return self._velocity

    @velocity.setter
    def velocity(self, new_value: tuple[float, float]):
        self._velocity = new_value

    def update_position(self):
        ''' updates the position of a particle. If particle collides with
            planet surface, destroy the particle
        '''
        self.position = (
            self.position[0] + self.velocity[0] / 100,
            self.position[1] + self.velocity[1] / 100
            )

    def update_velocity(self, acceleration: tuple[float, float]):
        ''' update the velocities based on an acceleration value'''
        self.velocity = (
            self.velocity[0] + acceleration[0],
            self.velocity[1] + acceleration[1]
        )


# ======================================================================
#                           DRIVER CODE:
# ======================================================================

def main():
    ''' driver code'''
    game = Game(WINDOW_SIZE)
    game.main_loop()

if __name__ == '__main__':
    main()
