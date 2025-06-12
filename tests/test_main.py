''' tests the functions in main'''
import pytest
import pygame
import games.main as m


class TestInputController:
    ''' tests methods in InputController'''
    @pytest.fixture
    def get_input_controller(self):
        ''' returns an input controller'''
        class SpyInputController(m.InputController):
            ''' returns a spy for the input controller class'''
            def __init__(self):
                super().__init__()
                self.num_left_calls = 0
                self.num_right_calls = 0
                self.num_esc_calls = 0

            @property
            def quits(self):
                return self._quits

            @quits.setter
            def quits(self, new_value):
                self.num_esc_calls += 1
                self._quits = new_value

            @property
            def turns_left(self):
                return self._turns_left

            @turns_left.setter
            def turns_left(self, new_value):
                self.num_left_calls += 1
                self._turns_left = new_value

            @property
            def turns_right(self):
                return self._turns_right

            @turns_right.setter
            def turns_right(self, new_value):
                self.num_left_calls += 1
                self._turns_right = new_value

        return SpyInputController()

    def return_keydown(self, pygame_key):
        ''' returns a list of 3 keydown events'''
        events = []
        for _ in range(3):
            event = pygame.event.Event(
                type=pygame.KEYDOWN, key=pygame_key
            )
            events.append(event)
        return events

    def return_keyup(self, pygame_key):
        ''' returns keyup events'''
        events = []
        for _ in range(3):
            event = pygame.event.Event(type=pygame.KEYUP, key=pygame_key)
            events.append(event)
        return events


    def return_left_list(self):
        ''' returns 3 left keys'''
        return [self.return_keydown(pygame.K_LEFT)] * 3

    def return_right_list(self):
        ''' returns 3 right keys'''
        return [self.return_keydown(pygame.K_RIGHT)] * 3

    def return_escape_key(self):
        ''' returns 3 escapes'''
        return [self.return_keydown(pygame.K_ESCAPE)] * 3

    def return_empty(self):
        ''' returns an empty list'''
        return []

    def return_left_keyup(self):
        ''' returns 3 keyup k_left events'''
        return [self.return_keyup(pygame.K_LEFT)] * 3

    def return_escape_keyup(self):
        ''' returns 3 keyup k_left events'''
        return [self.return_keyup(pygame.K_ESCAPE)] * 3


    def test_handle_inputs_k_left(self, monkeypatch, get_input_controller):
        ''' tests if the function sets the left attribute to true'''
        monkeypatch.setattr(pygame.event, 'get', self.return_keydown)
        monkeypatch.setattr()
        inp_controller = get_input_controller
        inp_controller.handle_events()
        assert inp_controller.turns_left
        assert inp_controller.num_left_calls == 3
        assert inp_controller.num_right_calls == 0
        assert ((inp_controller.thrusts, inp_controller.restarts) 
                == (False, False))


    def test_handle_inputs_k_right(self, monkeypatch, get_input_controller):
        ''' chekcs if right key works'''
        monkeypatch.setattr(pygame.event, 'get', self.return_right_list)
        inp_controller = get_input_controller
        inp_controller.handle_events()
        assert inp_controller.turns_right
        assert inp_controller.num_right_calls == 3


    def test_handle_inputs_escape(self, monkeypatch, get_input_controller):
        ''' checks if escape sequence works'''
        monkeypatch.setattr(pygame.event, 'get', self.return_escape_key)
        get_input_controller.handle_events()
        assert get_input_controller.quits
        assert get_input_controller.num_escape_calls == 3


    def test_handle_inputs_empty(self, monkeypatch, get_input_controller):
        ''' checks what happens if inputs are empty'''
        monkeypatch.setattr(pygame.event, 'get', self.return_empty)
        get_input_controller.handle_events()
        assert not get_input_controller.thrusts
        assert not get_input_controller.turns_left
        assert not get_input_controller.turns_right
        assert not get_input_controller.quits
        assert not get_input_controller.restarts


    def test_handle_inputs_keyup_k_left(
            self, monkeypatch, get_input_controller
    ):
        ''' tests the keyup function for inputs'''
        monkeypatch.setattr(pygame.event, 'get', self.return_left_keyup)
        get_input_controller.handle_events()
        assert not get_input_controller.turns_left
        assert get_input_controller.num_left_calls == 3


    def test_handle_inputs_keyup_k_escape(
            self, monkeypatch, get_input_controller
    ):
        ''' tests the keyup function for inputs'''
        monkeypatch.setattr(pygame.event, 'get', self.return_escape_keyup)
        get_input_controller.handle_events()
        assert not get_input_controller.quits
        assert get_input_controller.quits == 3
