''' determines the settings for the project'''

class Settings:
    ''' class to store the various settings for the project'''
    window_size = (1280, 780)
    planet_size = (.8, .2)
    planet_color = 'green'
    gravity = (0, -.2)
    particle_size = (20, 20)
    particle_color = 'red'
    default_velocity = 1.0
    starting_position = (0.5, 0)  # always start at bottom in the middle
    concurrent_expulsions = 4

    def __init__(self):
        ''' initialzes a settings object so there are no namespace clashes'''
        self.randomness = False
        self.velocity_spread = .2
        self.angle_spread = .2
        self.eruption_frequency = 2  # erupt every nth frame
        self.eruption_time = 20  # seconds
        self.eruption_downtime = 60  # seconds
