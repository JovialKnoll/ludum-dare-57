import jovialengine

import constants
import sprite
from .modeplay import ModePlay
from .modeopening import ModeOpening


class ModeOpening1(ModeOpening):
    _HORIZON = constants.SCREEN_SIZE[1] // 2

    def __init__(self):
        super().__init__()
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen)
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2 - 1),
            "press any key to start",
            constants.SKY_BLUE,
            constants.WATER_BLUE
        )
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.SKY_BLUE
        )
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 3 * 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.WHITE
        )
        version_width = len(constants.VERSION) * constants.FONT_SIZE
        jovialengine.get_default_font_wrap().render_to(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            constants.VERSION,
            constants.TEXT_COLOR
        )
        ship = sprite.Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        ship.start(self)

    def _switch_mode(self):
        self.next_mode = ModePlay()
