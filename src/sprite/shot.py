import jovialengine

import constants


class Shot(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SHIP
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY

    __slots__ = (
        'angle',
    )

    def _start(self, mode):
        self.angle = mode.arrow_angle

    def update(self, dt, camera):
        pass
