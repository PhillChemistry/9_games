''' tests the particle class '''

import math
import pytest
import pygame
import games.settings as s
import games.particle as p

TEST_ACCEL = (0, -.1)
TEST_ANGLE = 2

class TestParticle:
    ''' tests the class Particle'''
    @pytest.fixture
    def particle(self):
        ''' constructs a Particle object'''
        settings = s.Settings()
        particle = p.Particle(settings)
        return particle


    def test_update_velocity(self, particle):
        ''' tests the update velocity function'''
        part = particle
        part.velocity = (0, .5)
        part.update_velocity(TEST_ACCEL)
        assert part.velocity == (0, .4)
        for _ in range(5):
            part.update_velocity(TEST_ACCEL)
        assert part.velocity == (0, -.1)


    def test_update_position(self, particle):
        ''' tests that the box and the positions are adjusted properly'''
        part = particle
        part.window_size = (100, 100)
        part.position = (.2, .2)
        part.dimensions = (.5, .5)
        part.box = pygame.Rect((0, 0), (50, 50))
        part.box.center = (20, 80)
        part.velocity = (.1, .1)
        part.update_position()
        assert part.position == (.3, .3)
        assert part.box.width == 50
        assert part.box.height == 50
        assert part.box.center == (30, 70)


    def test_position_velocity(self, particle):
        ''' tests the exact way dimensions, velocities and boxes move'''
        part = particle
        part.window_size = (1000, 1000)
        part.velocity = (0, .1)
        part.dimensions = (.1, .1)
        gravity = (0, -.01)
        part.position = (.5, 0)
        part.box = part._get_box()
        assert part.box == pygame.Rect((450, 950, 100, 100))
        part.update_position()
        assert part.position == (.5, .1)
        assert part.box == pygame.Rect((450, 850, 100, 100))
        part.update_velocity(gravity)
        assert part.velocity == (0, .09)
        part.update_position()
        assert part.position == (.5, .19)
        assert part.box == pygame.Rect((450, 760, 100, 100))
        part.update_velocity(gravity)
        assert part.velocity == (0, .08)
        part.update_position()
        assert part.position == (.5, .27)
        assert part.box == pygame.Rect((450, 680, 100, 100))
    

    def test_random_generation_velocities(self, particle):
        ''' tests the conditions for the random particle generation'''
        class Settings:
            ''' settings'''
            def __init__(self):
                self.particle_size = (.05, .05)
                self.particle_position = (.5, 0)

        particle_list = []
        for _ in range(1_000):
            particle_list.append(
                p.Particle(
                    Settings,
                    abs_velocity=.1, velocity_spread=0,angle_spread=TEST_ANGLE
                )
            )
        x_list = [particle.velocity[0] for particle in particle_list]
        y_list = [particle.velocity[1] for particle in particle_list]
        thetas = []
        for x, y in zip(x_list, y_list):
            thetas.append(math.atan(x, y))
        assert max(thetas) < TEST_ANGLE/360 * 2*math.pi
        assert min(thetas) > - TEST_ANGLE/360 * 2*math.pi
