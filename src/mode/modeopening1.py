import jovialengine

import constants
#from .modeopening2 import ModeOpening2
from .modeopening import ModeOpening


class ModeOpening1(ModeOpening):
    _LOGO_TEXT = "JovialKnoll"

    __slots__ = (
        '_time',
        '_step',
    )

    def __init__(self):
        super().__init__()
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen)
        jovialengine.get_default_font_wrap().render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4 * 3 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.BLACK,
            constants.WHITE
        )
        version_width = len(constants.VERSION) * constants.FONT_SIZE
        jovialengine.get_default_font_wrap().render_to(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            constants.VERSION,
            constants.TEXT_COLOR
        )

    def _switch_mode(self):
        pass # self.next_mode = ModeOpening2()
