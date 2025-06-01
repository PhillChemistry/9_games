''' includes abcs Eruptor and Map, as well as concrete class Planet'''
from abc import ABC
from abc import abstractmethod
import pygame
from games.pyclock import PyClock
from games.settings import Settings
from games.coord_converter import CoordConverter

class Eruptor(ABC):
    ''' abstract base class for a particle manager'''
    @abstractmethod
    def __init__(self):
        ''' makes sure the concrete class has an __init__ method'''

    @property
    @abstractmethod
    def particles(self):
        ''' concrete class must have a particles property'''

    @property
    @abstractmethod
    def gravity(self):
        ''' concrete class must have a gravity property'''

    @abstractmethod
    def update_particle_velocities(self):
        ''' concrete class must implement a way to update the velocities'''

    @abstractmethod
    def update_particle_positions(self):
        ''' concrete class must have a way 
            to update the positions (and rects)
        '''

    @abstractmethod
    def destroy_out_of_bounds(self):
        ''' concrete class must implement a way to 
            destroy out of bounds particles
        '''

    @abstractmethod
    def erupt(self):
        ''' concrete class must implement a way to generate particles'''


class Map(ABC):
    ''' class to game_map the background and hold the particle effects'''
    @abstractmethod
    def __init__(self, settings: Settings):
        ''' this forces you to implement an __init__ method in concrete cls'''

    def __post_init__(self):
        ''' called from concrete cls, checks that all attributes are present'''
        hasattr(self, 'background')
        hasattr(self, 'eruptor')
        hasattr(self, 'planet_dimensions')

    @property
    @abstractmethod
    def background(self) -> pygame.Surface:
        ''' concrete class must have a background attribute'''

    @property
    @abstractmethod
    def planet_dimensions(self) -> tuple[float, float]:
        ''' concrete class must have a planet dimension attribute'''

    @property
    @abstractmethod
    def eruptor(self):
        ''' concrete class must have an eruptor attribute'''

    @abstractmethod
    def blit_volcano(self) -> None:
        ''' concrete class must be able to blit the eruptor'''

    @abstractmethod
    def blit_planet(self) -> None:
        ''' concrete class must prove a blit_planet method'''


class Planet(CoordConverter, Map):
    ''' a class to create eruptions'''
    def __init__(
        self, eruptor: Eruptor, settings: Settings, clock: PyClock
    ):
        super().__init__(settings)
        self._eruptor = eruptor
        self._planet_dimensions = settings.planet_size #  tuple[0 to 1, 0 to 1]
        self._planet_rect = self._get_planet_rect()
        self._planet_image = pygame.Surface(self._planet_rect)
        self._planet_image.fill(settings.planet_color)
        self._background = pygame.Surface(settings.window_size)
        self._background.fill('purple')
        self.clock = clock


    def blit_clock(self):
        ''' displays the clock on the backgorund'''
        self.clock.update_image()
        self.background.blit(self.clock.image)


    @property
    def eruptor(self):
        ''' returns the object managing the flying particles'''
        return self._eruptor

    @property
    def planet_dimensions(self):
        ''' returns the internal dimensions (x, y) in 
            range 0 to 1 of the planet
        '''
        return self._planet_dimensions

    @property
    def background(self):
        ''' returns the background surface of the planet'''
        return self._background


    def blit_planet(self):
        ''' blits the planet onto the background'''
        self.background.blit(self._planet_image, self._planet_rect)

    def blit_volcano(self):
        ''' blits the particles at their current positions'''
        for particle in self.eruptor.particles:
            self.background.blit(particle.image, particle.box)

    def _get_planet_rect(self) -> pygame.Rect:
        ''' calculate the planet dimensions'''
        planet_top = self.planet_dimensions[1]
        planet_left = .5 - self.planet_dimensions[0] / 2
        planet_width, planet_height = self.planet_dimensions
        planet_rect = pygame.Rect(
            (planet_left, planet_top, planet_width, planet_height)
        )
        return planet_rect
