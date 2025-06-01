''' defines the clock related class'''
import pygame
from games.coord_converter import CoordConverter
from games.settings import Settings


class PyClock(CoordConverter):
    ''' handles the clock as well as the clock image'''
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self._clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self._dimensions = settings.clock_dimensions
        self._image = self.font.render(
            self.clock.get_time(), antialias=False, color=(0, 0, 0)
        )
        self._box = self._get_box()


    def update_image(self):
        ''' updates the image of the clock to reflect the current time'''
        self._image = self.font.render(
            self.clock.get_time(), antialias=False, color=(0, 0, 0)
        )

    def _get_box(self):
        ''' generate the '''
        width, height = self.dimensions
        top = 1
        left = 1 - width
        box = pygame.Rect(
            self.convert_internals_to_px((top, left)),
            self.convert_internals_to_px((width, height))
        )
        return box

    @property
    def clock(self):
        ''' returns the current pygame clock'''
        return self._clock

    @property
    def image(self):
        ''' returns the image as a digital clock'''
        return self._image

    @property
    def dimensions(self):
        ''' returns the dimensions of the clock'''
        return self._dimensions
