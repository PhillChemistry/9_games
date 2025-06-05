''' test the functions inside the volcano class '''

import pytest
import games.volcano as v
import games.settings as s
import games.particle as p

class TestVolcano:
    ''' class to test the methods in the Volcano class'''
    @pytest.fixture
    def volcano(self):
        ''' sets the volcano object'''
        volcano = v.Volcano(s.Settings(), p.Particle(s.Settings()))
        return volcano

    def test_erupt(self, volcano):
        '''tests the erupt function'''
        volc = volcano
        volc.