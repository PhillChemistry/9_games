''' determines the settings for the project'''

class Settings:
    ''' class to store the various settings for the project'''
    window_size = (1280, 780)
    planet_size = (.8, .1)
    planet_color = 'green'
    gravity = (0, -0.0000025) #(0,  -0.005)
    particle_size = (0.03, 0.03)
    particle_color = 'red'
    default_velocity = 0.002
    starting_position = (0.5, 0)  # always start at bottom in the middle
    concurrent_expulsions = 1
    clock_dimensions = (.1, .2)

    def __init__(self):
        ''' initialzes a settings object so there are no namespace clashes'''
        self.randomness = True
        self.velocity_spread = .001
        self.angle_spread = 2
        self.eruption_frequency = 10_000  # erupt every nth frame
        self.eruption_time = 20  # seconds
        self.eruption_downtime = 60  # seconds
