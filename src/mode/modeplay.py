import jovialengine
import pygame

import constants
from .modescreensize import ModeScreenSize
from sprite import Ship

class ModePlay(ModeScreenSize):
    _HORIZON = 40
    __slots__ = (
        '_ship',
        '_draw_arrow',
        '_arrow_angle',
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.WHITE)
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        # should set up background more probably

        self._ship = Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        self._ship.start(self)
        self._draw_arrow = True
        self._arrow_angle = 90

    def _update_pre_sprites(self, dt):
        if self._input_frame.get_input_state(0, constants.EVENT_LEFT) == 1:
            self._arrow_angle -= dt * 0.001 * 90
        if self._input_frame.get_input_state(0, constants.EVENT_RIGHT) == 1:
            self._arrow_angle += dt * 0.001 * 90

    def _update_pre_draw(self):
        self._arrow_angle = jovialengine.utility.clamp(self._arrow_angle, 0, 180)

    def _draw_post_camera(self, screen):
        if self._draw_arrow and self._ship.alive():
            vec = pygame.Vector2(-30, 0)
            vec.rotate_ip(-self._arrow_angle)
            print(vec)
            start = self._ship.rect.midbottom

        pass
