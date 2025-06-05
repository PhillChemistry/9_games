'''tests functions and classes in volcano.py'''
import pytest
import games.main as m
import games.settings as s
import games.pyclock as c
import games.planet as p
import games.volcano as v
import games.particle as part
import games.coord_converter as cc

DEFAULT_WINDOW = (100, 100)
HIGH_PRECISION_FLOAT = .243124123476761273


class TestGame:
    ''' tests the game class'''
    @pytest.fixture
    def game(self):
        ''' creates a game object'''
        settings = s.Settings()
        clock = c.PyClock(settings)
        particle = part.Particle(settings)
        volcano = v.Volcano(settings, particle)
        game_map = p.Planet(volcano, settings, clock)
        game = m.Game(game_map, settings, clock)
        return game

    def check_composition(self, game):
        ''' determines the composition of the Game class'''
        game_instance = game
        hasattr(game_instance, 'clock')
        hasattr(game_instance, 'game_map')


class TestCoordConverter:
    ''' tests the coordinate conversion functions'''
    @pytest.fixture
    def converter(self):
        ''' returns a CoordConverter object'''
        class Window:
            ''' settings stub to define the window size'''
            def __init__(self):
                self.window_size = DEFAULT_WINDOW
        example_window = Window()
        converter = cc.CoordConverter(example_window)
        return converter

    def test_attributes(self, converter):
        ex_converter = converter
        assert hasattr(ex_converter, 'window_size')
        assert ex_converter.window_size == (100, 100)


    def test_conversions(self, converter):
        ''' tests whether the conversions work out to be correct'''
        ex_converter = converter
        assert ex_converter.convert_x_to_px(.5) == 50
        assert ex_converter.convert_y_to_px(.5) == 50
        assert ex_converter.convert_internals_to_px((.5, .5)) == (50, 50)
        assert ex_converter.convert_x_to_px(1) == 100
        assert ex_converter.convert_x_to_px(0) == 0
        assert ex_converter.convert_y_to_px(1) == 0
        assert ex_converter.convert_y_to_px(0) == 100
        assert ex_converter.convert_internals_to_px((1, 1,)) == (100, 0)
        assert ex_converter.convert_internals_to_px((0,0)) == (0, 100)


    def test_long_floating_points(self, converter):
        ''' tests that extreme precision is also tolerated'''
        ex_converter = converter
        assert ex_converter.convert_x_to_px(HIGH_PRECISION_FLOAT) == 24
        assert ex_converter.convert_y_to_px(HIGH_PRECISION_FLOAT) == 76
        assert ex_converter.convert_internals_to_px(
            (HIGH_PRECISION_FLOAT, HIGH_PRECISION_FLOAT)
        ) == (24, 76)


    def test_convert_dimensions(self, converter):
        ''' tests the dimension converter function'''
        ex_converter = converter
        assert ex_converter.convert_dimensions_to_px(
            (HIGH_PRECISION_FLOAT, HIGH_PRECISION_FLOAT)
        ) == (24, 24)
        assert ex_converter.convert_dimensions_to_px((1,1,)) == (100, 100)
        assert ex_converter.convert_dimensions_to_px((0, 0,)) == (0, 0)