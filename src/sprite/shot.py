import jovialengine

import constants
import utility


class Shot(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SHIP
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY

    __slots__ = (
        'angle',
    )

    def _start(self, mode):
        self.angle: float = mode.arrow_angle

    def update(self, dt, camera):
        distance = dt * 0.001 * 20
        vec = utility.angle_vector(distance, self.angle)
        self.rect.move_ip(vec.x, vec.y)
