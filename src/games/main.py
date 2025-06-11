''' main code to generate the rocket landing game. 
    For further info, see the docs.
    ideas for extensions after the base game is complete:
    - add space debree to collide with
    - add a second planet to land at 
        (so the player has to escape the first planets gravitational pull)
'''

from abc import ABC, abstractmethod
import pygame
from games.settings import SETTINGS

# ========================================================================
#                          TOP LEVEL CLASSES
# ========================================================================


class CoordinateConverter:
    ''' class to convert between different coordinate systems:
        COORDINATES ARE ON A SCALE OF 0 TO 100!
    ATTRIBUTES:
        window_size
    METHODS:
        convert x
        convert y 
        convert width
        convert length
        convert xy
        convwert width length
    '''
    def __init__(self, settings: dict):
        ''' Coordinate Converter constructor'''
        self.window_size = settings['window_size']
        self.round_to = settings['rounding_digits']

    def convert_x_position(self, internal_x_value: float):
        ''' converts internal x value (scale 0 to 100) to window_size pixels'''
        fraction = round(internal_x_value / 100, self.round_to)
        return self.window_size[0] * fraction

    def convert_y_position(self, internal_y_value: float):
        ''' converts internal y value (scale 0 to 100) to window_size pixels'''
        fraction = round(internal_y_value / 100, self.round_to)
        fraction = 1 - fraction
        return self.window_size[1] * fraction

    def convert_xy_position(self, internal_xy_tuple: tuple[float, float]):
        ''' convert internal positional tuple (0 to 100) to pixels'''
        x, y = internal_xy_tuple
        x = self.convert_x_position(x)
        y = self.convert_y_position(y)
        return (x, y)

    def convert_width(self, internal_width: float):
        ''' converts internal width (scale 0 to 100) to window_size pixels'''
        fraction = round(internal_width / 100, self.round_to)
        return fraction * self.window_size[0]

    def convert_length(self, internal_length: float):
        ''' converts internal length (scale 0 to 100) to window_size pixels'''
        fraction = round(internal_length / 100, self.round_to)
        return fraction * self.window_size[1]

    def convert_width_length(self, internal_tuple: tuple[float, float]):
        ''' convert internal width length tuple (0 to 100) to pixels'''
        x, y = internal_tuple
        x = self.convert_width(x)
        y = self.convert_length(y)
        return (x, y)


class GameObject(CoordinateConverter, ABC):
    ''' base class for game objects
    ATTRIBUTES:
        position
        rect
        image
    METHODS:
        getters / setters
    '''
    @abstractmethod
    def __init__(self, settings: dict):
        ''' generalizzed game object contructor'''
        super().__init__(settings)

    def __post_init__(self):
        ''' post init function to check implementation 
            of  all required attributes'''

    @property
    @abstractmethod
    def position(self) -> tuple[float, float]:
        ''' getter for internal position coordinate'''

    @property
    @abstractmethod
    def hbox(self) -> pygame.Rect:
        ''' getter for the hitbox as a rect'''

    @property
    @abstractmethod
    def image(self) -> pygame.Surface:
        ''' getter for the display image'''


class InputController:
    ''' class to handle the player inputs and its flags
    ATTRIBUTES:
        turns_left: bool
        turns_right: bool
        thrusts
        quits
        restarts
    METHODS:
        handle_inputs
        handle_events
    '''

    def __init__(self):
        ''' InputController objects handle the player inputs'''
        self._turns_left = False
        self._turns_right = False
        self._thrusts = False
        self._quits = False
        self._restarts = False


    def handle_inputs(self):
        ''' receive the current player inputs'''
        current_events = pygame.event.get()
        key_functions = {
            pygame.K_LEFT: self.turns_left,
            pygame.K_RIGHT: self.turns_right,
            pygame.K_UP: self.thrusts,
            pygame.K_ESCAPE: self.quits,
            pygame.K_r: self.restarts
        }
        for event in current_events:
            if event.type == pygame.KEYDOWN:
                for key_pressed, corresp_attribute in key_functions.items():
                    if event.key == key_pressed:
                        corresp_attribute = True
            elif event.type == pygame.KEYUP:
                for key_pressed, corresp_attribute in key_functions.items():
                    if event.key == key_pressed:
                        corresp_attribute = False
        if self.turns_left and self.turns_right:
            self.turns_left = False
            self.turns_right = False

    @property
    def quits(self):
        ''' getter for quits property'''
        return self._quits

    @quits.setter
    def quits(self, new_value):
        ''' setter for quits property'''
        self._quits = new_value

    @property
    def turns_left(self):
        ''' getter for turns_left property'''
        return self._turns_left

    @turns_left.setter
    def turns_left(self, new_value):
        ''' setter for turns_left property'''
        self._turns_left = new_value

    @property
    def turns_right(self):
        ''' getter for turns_right property'''
        return self._turns_right

    @turns_right.setter
    def turns_right(self, new_value):
        ''' setter for turns_right property'''
        self._turns_right = new_value

    @property
    def thrusts(self):
        ''' getter for thrusts property'''
        return self._thrusts

    @thrusts.setter
    def thrusts(self, new_value):
        ''' setter for thrusts property'''
        self._thrusts = new_value

    @property
    def restarts(self):
        ''' getter for restarts property'''
        return self._restarts

    @restarts.setter
    def restarts(self, new_value):
        ''' setter for restarts property'''
        self._restarts = new_value


    def handle_events(self):
        ''' handles quitting and restart events'''
        if self.quits:
            pygame.quit()


class Rocket(CoordinateConverter, GameObject):
    ''' class to manage the player-controlled rocket ship. ATTRIBUTES:
    ATTRIBUTES:
        hbox: pygame.Rect -> controls the position
        position: tuple[float, float] -> relative position of hbox center
        angle: float -> 0 to 2 pi, determines the rocket pointer
        NOTE: you could give the images their own class
        current_image: pygame.Surface -> contains the current Rocket image
        default_image: pygame.Surface -> contains the default image to use
        velocity: tuple[float, float]
        mass
    METHODS:
        getters/ setters
        update_image
    '''
    def __init__(self, settings: dict):
        super().__init__(settings)
        self._position = settings['starting_position']
        # TODO: continue here
    

class Player(ABC):
    ''' class to manage how the player interacts with the world. 
    ATTRIBUTE:
        rocket: Rocket -> the rocket controlled by the player
        inputs: InputController -> manages the inputs and input flags
        fuel: FuelManager -> the remaining fuel in the rocket
        turn_speed
        thrust_speed
    METHODS:
        getters/ settersce 
        turn rocket
        thrust rocket
        adjust_fuel
    '''
    def __init__(
        self, rocket: Rocket, inputs: InputController,
        fuel: FuelManager, settings: dict
    ):
        ''' the player class manages inputs and the player ship'''
        self._rocket = rocket
        self._inputs = inputs
        self._fuel = fuel
        self._turn_speed = settings['turn_speed']
        self._thrust_speed = settings['thrust_speed']


    @property
    def rocket(self) -> Rocket:
        ''' return object to manage the player ship location and velocity'''
        return self._rocket

    @property
    def inputs(self) -> InputController:
        ''' return the object to handle player inputs'''
        return self._inputs

    @property
    def fuel(self) -> FuelManager:
        ''' return the object to manage remaining thrust fuel'''
        return self._fuel

    @property
    def turn_speed(self) -> float:
        ''' return the specified turn speed of the rocket (in rad/sec)'''
        return self._turn_speed

    @property
    def thrust_speed(self) -> float:
        ''' return the rocket's thrust speed in internal coords (0 to 100)'''
        return self._thrust_speed


class HUD:
    ''' class to handle the HUD elements.
    ATTRIBUTES:
        fuel_bar: FuelBar -> blits the remaining player fuel
        time_display -> shows the current time
        hud_background
    METHODS:
        getters / setters
    '''

class FuelManager:
    ''' class to handle the fuel requirements of the space ship.
        tracks the current fuel as well as the current fuel expenses
        based on whether there is rocket thrust or not
    ATTRIBUTES:
        max fuel
        current fuel
        fuel loss by turning
        fuel loss by thrust
    METHODS:
        expend_fuel_turning
        expend_fuel_thrusting
        getters / setters
    '''



class Planet:
    ''' class to handle the planet. 
    ATTRIBUTES:
        hbox: pygame.Rect
        position: tuple[float, float]
        image
        mass: float [in tonnes]
    METHODS:
        getters / setters
    '''


class NonPlayerObjects:
    ''' class to manage non-player characters / objects
    ATTRIBUTES:
        background -> background
        planet -> Planet
    METHODS:
        getters / setters
    '''


class Background:
    ''' class to manage the background:
    ATTRIBUTES:
        position
        image
        hbox
    METHODS:
        getters / setters
    '''


class CollisionHandler:
    ''' class to handle the to check whether two objects collide
    ATTRIBUTES:
        max entrance velocity
        max tolerated angle
    METHODS:
        determine collision
        determine collision with landing site
        check if landing speed is permissible
        check if landing angle is permissible
        check if landing conditions are permissible
    '''


class ForceHandler:
    ''' class to handle the forces acting on the different objects. 
    ATRIBUTES:
        gravitational constant
    METHODS:
        determine gravities
        determine thrust
        calculate total velocity
    '''


class Game:
    ''' class to manage the game assetts. Attributes:
    ATTRIBUTES:
        screen
        collision_handler: CollisionHandler -> handles the collisions
        force_handler: ForceHandler -> determines the current forces objects
            acting on an object
        player
        non_player_objects
        hud
    METHODS:
        main_loop
        end-screen
        display_current_image
        blit(image1, onto_image2) -> blit image1 onto image2
    '''


    def __init__(self, player: Player):
        ''' construct the necessary objects and execute the main loop'''
        pygame.init()
        self.screen = pygame.display.set_mode(SETTINGS['window_size'])
        self.player = player


    def display_current_image(self, current_image):
        '''blit the current screen'''
        self.screen.blit(current_image, dest=(0,0))
        pygame.display.flip()


# ====================================================================
#                        DRIVER CODE
# ====================================================================

def main():
    ''' driver code '''
    game = Game()


if __name__ == '__main__':
    main()
