''' main code to generate the rocket landing game. 
    For further info, see the docs.
'''

from abc import ABC, abstractmethod
import pygame
from games.settings import SETTINGS

# ========================================================================
#                          TOP LEVEL CLASSES
# ========================================================================

class Player(ABC):
    ''' abstract class setting the requirements for a player function'''
    @abstractmethod
    def __init__(self):
        ''' player object constructor (always only 1 player)'''

    @abstractmethod
    def __post_init__(self):
        ''' ensure that a post_init method is defined
            (to check that all attributes are present)
        '''

    @abstractmethod
    def handle_events(self):
        ''' define the event handler'''

    @abstractmethod
    def get_inputs(self):
        ''' define the input handler'''


class Game:
    ''' class to manage the game assetts'''
    def __init__(self):
        ''' construct the necessary objects and execute the main loop'''
        pygame.init()
        self.screen = pygame.display.set_mode(SETTINGS['window_size'])
        self.player = Player


    def display_current_image(self, current_image):
        '''blit the current screen'''
        self.screen.blit(current_image, dest=(0,0))
        pygame.display.flip()

# ====================================================================
#                        DRIVER CODE
# ====================================================================

def main():
    ''' driver code '''
    pass

if __name__ == '__main__':
    main()
