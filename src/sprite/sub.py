import jovialengine

import constants
import utility


class Sub(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SUB
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SUB
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY
    __slots__ = (
        '_speed',
    )

    def _start(self, mode):
        # facing left by default
        if self._speed > 0:
            pass
            #self.image = pygame.transform.flip(self.image, True, False)
            #self._mask_image = pygame.transform.flip(self._mask_image, True, False)

    def update(self, dt, camera):
        pass
