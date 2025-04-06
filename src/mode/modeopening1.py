import jovialengine
import pygame

import constants
import sprite
from .modeplay import ModePlay
from .modeopening import ModeOpening


class ModeOpening1(ModeOpening, jovialengine.Saveable):
    _HORIZON = constants.SCREEN_SIZE[1] // 2

    def save(self):
        return 0

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        return new_obj

    def __init__(self):
        super().__init__()
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen)
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        font_wrap = jovialengine.get_default_font_wrap()
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2 - 1),
            "press any key to start",
            constants.SKY_BLUE,
            constants.WATER_BLUE
        )
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.SKY_BLUE
        )
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.WHITE
        )
        title_surf = font_wrap.render_inside(
            font_wrap.font.size(constants.TITLE)[0],
            constants.TITLE,
            constants.DARK_RED,
            constants.CLOUD_GREY
        )
        title_surf = pygame.transform.scale2x(title_surf)
        title_surf = pygame.transform.rotozoom(title_surf, -1.5, 1)
        title_surf.set_colorkey((0, 0, 0))
        title_rect = title_surf.get_rect()
        title_rect.center = (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4)
        self._background.blit(title_surf, title_rect)
        high_score = str(jovialengine.get_state().high_score)
        high_score_width = len(high_score) * constants.FONT_SIZE
        font_wrap.render_to(
            self._background,
            (constants.SCREEN_SIZE[0] - high_score_width, 0),
            high_score,
            constants.BLACK
        )
        version_width = len(constants.VERSION) * constants.FONT_SIZE
        font_wrap.render_to(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            constants.VERSION,
            constants.TEXT_COLOR
        )
        ship = sprite.Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        ship.start(self)

    def _switch_mode(self):
        self.next_mode = ModePlay()
