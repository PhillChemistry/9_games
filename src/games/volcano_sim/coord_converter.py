''' coordinate conversion class'''
from games.volcano_sim.settings import Settings

class CoordConverter:
    ''' class to save'''
    def __init__(self, settings: Settings | None = None):
        ''' define the settings for the converter'''
        if settings is not None:
            self.window_size = settings.window_size
        else:
            self.window_size = (0, 0)


    def convert_x_to_px(self, internal_coord: float) -> int:
        ''' calculate a pixel x coordinate based on internal coordinates'''
        x_max = self.window_size[0]
        x = int(round(internal_coord * x_max))
        return x


    def convert_y_to_px(self, internal_coord: float) -> int:
        ''' calculate a pixel x coordinate based on internal coordinates'''
        y_max = self.window_size[1]
        # internal coords count bottom-up, pygame counts top-down:
        y = 1 - internal_coord
        y = int(round(y * y_max))
        return y


    def convert_internals_to_px(
        self, internal_coords: tuple[float, float]
    ) -> tuple[int, int]:
        ''' calculate a pixel coordinate TUPLE based on internal coordinates'''
        self._validate_coords(internal_coords)
        x, y = internal_coords
        x = self.convert_x_to_px(x)
        y = self.convert_y_to_px(y)
        return (x, y)


    def convert_dimensions_to_px(
        self, internal_coords: tuple[float, float]
    ) -> tuple[int, int]:
        ''' convert the dimensions (width, height) to pixels'''
        self._validate_coords(internal_coords)
        x, y = internal_coords
        x = self.convert_x_to_px(x)
        y = int(round(y * self.window_size[1]))
        return (x, y)


    def _validate_coords(self, coords) -> None:
        ''' raises error when the coordinate type/dimensions don't fit'''
        try:
            assert len(coords) == 2
        except AssertionError as e:
            print('ERROR: the lenght of the tuple must be 2!')
            raise e