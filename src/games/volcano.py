''' includes Volcano and Expulsable classes'''
from abc import ABC
from abc import abstractmethod
from games.settings import Settings
from games.coord_converter import CoordConverter
from games.planet import Eruptor

class Expulsable(ABC, CoordConverter):
    ''' abstract base class to determine particles'''

    @abstractmethod
    def __init__(self, settings, atr1, atr2):
        ''' create an expulsable'''
        super().__init__(settings)
        # TODO: add correct attribute names

    @classmethod
    @abstractmethod
    def like_particle(
        cls, particle, rand_atr1=None, rand_atr2=None, rand_atr3=None
    ):
        # TODO: add correct attribute names
        ''' alternative constructor for the class'''

    @abstractmethod
    def update_positions(self):
        ''' requires a way to update all particle positions'''

    @abstractmethod
    def update_velocities(self):
        ''' requires a way to update particle positions'''


class Volcano(CoordConverter, Eruptor):
    ''' class to manage the volcano emissions created in the simulation'''
    def __init__(
            self, settings: Settings, default_particle: Expulsable,
    ):
        ''' generate the volcano class to manage the particles'''
        super().__init__(settings)
        self._particles = []
        self._gravity = settings.gravity
        self._eruption_timer = -1
        self._concurrent_expulsions = settings.concurrent_expulsions
        self._eruption_properties = {
            'frequency': settings.eruption_frequency,
            'downtime': settings.eruption_downtime,
            'duration': settings.eruption_time,
            'last_erupt': -1
        }
        self._eruption_frequency = 2  # every second frame
        self._default_particle = default_particle
        if settings.randomness:
            self._random_attributes = {
                'randomness': True,
                'angle_spread': settings.angle_spread,
                'velocity_spread': settings.velocity_spread,
                'avg_velocity': settings.default_velocity,
            }
        else:
            self._random_attributes['randomness'] = False

    @property
    def particles(self):
        return self._particles

    @particles.setter
    def particles(self, new_value):
        if isinstance(new_value, list):
            self._particles = new_value
        else:
            print('particles must be list of Particle objects!')
            raise ValueError

    @property
    def gravity(self):
        return self._gravity

    @property
    def concurrent_expulsions(self):
        ''' return the number of particles created at once 
            during an eruption cycle
        '''
        return self._concurrent_expulsions

    @concurrent_expulsions.setter
    def concurrent_expulsions(self, new_num: int):
        if isinstance(new_num, int) and new_num > 0:
            self._concurrent_expulsions = new_num
        else:
            print('ERROR: new_num must be positive integer!')
            raise ValueError

    def erupt(self):
        ''' manages particle creation, respecting the eruption frequency
            eruption_properties: frequency, downtime, duration, and last_erupt
        '''
        if (self._eruption_timer >= 0
            and self._eruption_timer < self._eruption_properties['duration']):
            if self._determine_if_erupts(
                self._eruption_timer,
                self._eruption_properties['last_erupt'],
                self._eruption_properties['frequency']
            ):
                self.single_expulsion()
            self._eruption_timer += 1
        elif self._eruption_timer >= self._eruption_properties['duration']:
            self._eruption_timer = -1
        elif (self._eruption_timer < 0
            and self._eruption_timer > -1*self._eruption_properties['downtime']
        ):
            # using negative int numbers as wait time
            self._eruption_properties['last_erupt'] = self._eruption_timer
            self._eruption_timer -= 1
        elif self._eruption_timer <= self._eruption_properties['downtime']:
            self._eruption_timer = 0
        else:
            print('This shouldn\'t happen!')
            raise AssertionError


    def _erupt2(self):
        ''' keep erupting over a short timeframe, then stop to recover'''
        if self._eruption_timer >= 0:
            if self._eruption_timer < self._eruption_properties['duration']:
                triggers_eruption = (
                    round(self._eruption_timer / self._eruption_properties[
                        'frequency'
                    ])
                    != self._eruption_properties['last_erupt']
                )
                if triggers_eruption:
                    self.erupt()
                    self._eruption_properties[
                        'last_erupt'
                    ] = self._eruption_timer
                self._eruption_timer += 1
            else:
                self._eruption_timer = -1
        else:
            if (self._eruption_timer
                >= -1 * self._eruption_properties['downtime']):
                self._eruption_timer -= 1
            else:
                self._eruption_timer = 0


    def single_expulsion(self):
        ''' defines a single expulsion event during an eruption'''
        for _ in range(self.concurrent_expulsions):
            if self._random_attributes['randomness']:
                self.particles.append(
                    Expulsable.like_particle(
                        self._default_particle,
                        self._random_attributes['avg_velocity'],
                        self._random_attributes['velocity_spread'],
                        self._random_attributes['angle_spread'],
                    )
                )
            else:
                self.particles.append(
                    Expulsable.like_particle(self._default_particle)
                )


    def _determine_if_erupts(
            self, current_time: int, last_erupt_time: int, frequency: float
    ):
        return (current_time // frequency
                    != last_erupt_time)

    def update_particle_velocities(self):
        ''' updates the velocities of all current particles'''
        for particle in self.particles:
            particle.update_velocity()

    def update_particle_positions(self):
        ''' updates the positions and rects/ boxes of the particles'''
        for particle in self.particles:
            particle.update_position(self)

    def update_particle_movements(self):
        ''' calculate the speeds at which the particles move'''
        for particle in self.particles:
            particle.update_position()
            particle.update_velocity(
                self.gravity
            )

    def destroy_out_of_bounds(self, ):
        '''determine whether particles are out of bounds, then destroy them'''
        for particle in self.particles:
            is_below_screen = particle.position[1] < 0
            too_far_left = particle.position[0] < 0
            too_far_right = particle.position[0] > 1
            if is_below_screen or too_far_left or too_far_right:
                self.particles.remove(particle)
