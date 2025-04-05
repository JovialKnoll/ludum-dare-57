import jovialengine

import constants
from .modescreensize import ModeScreenSize
from sprite import Ship

class ModePlay(ModeScreenSize):
    __slots__ = (
        '_ship',
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.WHITE)
        self._background.fill((0, 23, 198), (0, 40, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        # should set up background more probably
        self._ship = Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, 40))
        self._ship.start(self)
