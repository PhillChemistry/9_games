import pytest
import pygame
import games.main as m


class TestInputController:
    ''' tests methods in InputController'''
    @fixture
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
                self.num_esc_calls += 1
                return self._quits

            @quits.setter
            def quits(self, new_value):
                self.num_esc_calls += 1
                self._quits = new_value

            @property
            def turns_left(self):
                self.num_left_calls += 1
                return self._turns_left

            @turns_left.setter
            def turns_left(self, new_value):
                self.num_left_calls += 1
                self._turns_left = new_value

            @property
            def turns_right(self):
                self.num_left_calls += 1
                return self._turns_right

            @turns_right.setter
            def turns_right(self, new_value):
                self.num_left_calls += 1
                self._turns_right = new_value

        return SpyInputController()


    def return_left_list(self):
        ''' returns 3 left keys'''
        return [pygame.K_LEFT, pygame.K_LEFT, pygame.K_LEFT,]

    def return_right_list(self):
        ''' returns 3 right keys'''
        return [pygame.K_RIGHT, pygame.K_RIGHT, pygame.K_RIGHT]

    def return_escape_key(self):
        ''' returns 3 escapes'''
        return [pygame.K_ESCAPE, pygame.K_ESCAPE, pygame.K_ESCAPE]

    def return_empty(self):
        return []


    def test_handle_inputs_k_left(self, monkeypatch, get_input_controller):
        ''' tests if the function sets the left attribute to true'''
        monkeypatch.setattr(pygame.event, 'get', self.return_left_list)
        inp_controller = get_input_controller
        inp_controller.handle_events()
        assert inp_controller.turns_left
        assert inp_controller.num_left_calls == 3
        assert inp_controller.num_right_calls == 0
        assert inp_controller.thrusts, inp_controller.restarts == False, False


    def test_handle_inputs_k_right(self, monkeypatch, get_input_controller):
        monkeypatch.setattr(pygame.event, 'get', self.return_right_list)
        inpt_controller = get_input_controller
        inp_contoller.handle_events()
        assert inp.controller.turns_right
        assert inp_controller.num_right_calls == 3


    def test_handle_inputs_escape(self, monkeypatch, get_input_controller):
        monkeypatch.setattr(pygame.event, 'get', self.return_escape_key)
        get_input_controller.handle_events()
        assert get_input_controller.quits
        assert get_input_controller.num_escape_calls == 3
    
    def test_handle_inputs_empty(self, monkeypatch, get_input_controller):
        monkeypatch.setattr(pygame.event, 'get', self.return_empty)
        get_input_controller.handle_events()
        assert not get_input_controller.thrusts
        assert not get_input_controller.turns_left
        assert not get_input_controller.turns_right 
        assert not get_input_controller.quits
        assert not get_input_controller.restarts
