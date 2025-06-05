''' includes the Particle class'''
import random
import math
import pygame
from games.volcano_sim.settings import Settings
from games.volcano_sim.coord_converter import CoordConverter


class Particle(CoordConverter):
    ''' a class to keep track of particle positions and velocity vectors'''
    def __init__(
            self, settings: Settings | None = None,
            abs_velocity: float | None = None,
            velocity_spread: float | None = None,
            angle_spread: float | None = None
    ):
        ''' initializes a particle object 
            random variables: internal coordinates (0 to 1),
            angle_spread: random angle in degrees (0 to 360)
        '''
        if settings is None:
            super().__init__()
        else:
            super().__init__(settings)
            self._dimensions = settings.particle_size
            self._position = settings.starting_position
            self._box = self._get_box()
            self._image = self._get_image(settings)

            # self._velocity:
            all_none = (abs_velocity, velocity_spread, angle_spread) \
                        == (None, None, None)
            if settings.randomness and not all_none:
                self._velocity = self._determine_velocity(
                    abs_velocity, velocity_spread, angle_spread
                )
            else:
                self._velocity = (0, settings.default_velocity)


    @classmethod
    def like_particle(
        cls, particle, abs_velocity: float = None,
        velocity_spread: float = None, angle_spread: float = None
        ):
        ''' generate a particle based on an existing particle'''
        new_particle = Particle()
        new_particle.window_size = particle.window_size
        new_particle.dimensions = particle.dimensions
        new_particle._position = particle.position
        new_particle._box = new_particle._get_box()
        new_particle._image = particle.image
        all_none = (abs_velocity, velocity_spread, angle_spread) \
                    == (None, None, None)
        if not all_none:
            new_particle._velocity = new_particle._determine_velocity(
                abs_velocity, velocity_spread, angle_spread
            )
        else:
            new_particle._velocity = particle.velocity
        return new_particle



    def update_position(self):
        ''' updates the position of a particle. If particle collides with
            planet surface, destroy the particle
        '''
        x, y = self.position
        x_velocity, y_velocity = self.velocity
        x += x_velocity
        y += y_velocity
        self.position = (round(x, 7), round(y, 7))
        width, height = self.convert_dimensions_to_px(self.dimensions)
        self.box = pygame.Rect((0,0,0,0))
        self.box.width = width
        self.box.height = height
        self.box.center = self.convert_internals_to_px(self.position)


    def update_velocity(self, acceleration: tuple[float, float]):
        ''' update the velocities based on an acceleration value'''
        x_velocity, y_velocity = self.velocity
        x_accel, y_accel = acceleration
        self.velocity = (
            round(x_velocity + x_accel, 7), round(y_velocity + y_accel, 7)
        )


    @property
    def position(self):
        ''' returns the position of the particle'''
        return self._position


    @position.setter
    def position(self, new_value):
        ''' sets the new position of teh particle'''
        self._confirm_len2_tuple(new_value)
        self._position = new_value


    @property
    def image(self):
        ''' returns the image surface of the object'''
        return self._image


    @property
    def velocity(self):
        ''' returns the current speed of the particle'''
        return self._velocity


    @velocity.setter
    def velocity(self, new_value: tuple[float, float]):
        self._confirm_len2_tuple(new_value)
        self._velocity = new_value


    @property
    def box(self):
        ''' returns the pygame Rect of the particle'''
        return self._box


    @box.setter
    def box(self, new_box):
        ''' sets the box of the particle'''
        if isinstance(new_box, pygame.Rect):
            self._box = new_box
        else:
            print('ERROR: Box must be pygame.Rect object!')
            raise ValueError


    @property
    def dimensions(self):
        ''' gets the dimension property as a tuple[float, float] 
            (internal coords)
        '''
        return self._dimensions


    @dimensions.setter
    def dimensions(self, new_tuple):
        ''' set the dimensions. must be in internal coordinates'''
        self._confirm_len2_tuple(new_tuple)
        x_val_correct = 0 <= new_tuple[0] <= 1
        y_val_correct = 0 <= new_tuple[1] <= 1
        if not (x_val_correct and y_val_correct):
            raise ValueError
        self._dimensions = new_tuple


    def _get_box(self):
        ''' calculate the image rect based on dimensions and position'''
        center = self.convert_internals_to_px(self.position)
        width, height = self.convert_dimensions_to_px(self.dimensions)
        box = pygame.Rect((0,0), (0,0))
        box.width = width
        box.height = height
        box.center = center
        return box


    def _get_image(self, settings: Settings):
        ''' calculate the image size based on the game state'''
        width, height = self.convert_dimensions_to_px(self.dimensions)
        image = pygame.Surface((width, height))
        image.fill(settings.particle_color)
        return image


    def _determine_velocity(
            self, abs_velocity: float | None = None,
            velocity_spread: float | None = None,
            angle_spread: float | None = None
    ) -> tuple[float, float]:
        '''determines the starting velocity vector based on given settings'''
        if abs_velocity is not None:
            if velocity_spread is not None:
                if angle_spread is not None:
                    velocity = self._randomize_angle(
                        abs_velocity, velocity_spread, angle_spread
                    )
                else:
                    velocity = (0, self._randomize_velocity(
                        abs_velocity, velocity_spread
                        )
                    )
            else:
                velocity = (0, abs_velocity)
        else:
            velocity = (0, Settings.default_velocity)
        return velocity


    def _randomize_angle(
        self, v_absolute: float, spread_v: float, spread_angle: float
    ) -> tuple[float, float]:
        ''' determine the velocity vector based on a random factor'''
        v_absolute = self._randomize_velocity(v_absolute, spread_v)
        angle_rand_adjust = 2 * spread_angle * random.random() - spread_angle
        angle_rad = angle_rand_adjust / 360 * 2 * math.pi
        x = v_absolute  * math.sin(angle_rad)
        y = math.sqrt(v_absolute ** 2 - x ** 2)
        return (x, y)


    def _randomize_velocity(
            self, v_absolute: float, spread_v: float
    ) -> tuple[float, float]:
        ''' determine a random velocity'''
        if spread_v != 0:
            v_rand_adjust = random.random() * 2 * spread_v - spread_v
        else:
            v_rand_adjust = 0
        velocity = v_absolute + v_rand_adjust
        return velocity


    def _confirm_len2_tuple(self, value):
        if not isinstance(value, tuple):
            raise ValueError
        if not len(value) == 2:
            raise ValueError
