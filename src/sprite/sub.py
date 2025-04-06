import jovialengine

import constants
from .shottrigger import ShotTrigger
from .shot import Shot
from .explosion import Explosion


class Sub(ShotTrigger):
    _IMAGE_LOCATION = constants.SUB
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SUB
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY
    __slots__ = (
        '_speed',
    )

    def __init__(self, speed: float, **kwargs):
        super().__init__(**kwargs)
        self._speed = speed

    def _start(self, mode):
        if self._speed > 0:
            # if going right flip so facing right
            self.image = jovialengine.load.flip(self.image, True, False)
            self._mask_image = jovialengine.load.flip(self._mask_image, True, False)
            self.mask = jovialengine.load.mask_surface(self._mask_image)

    def update(self, dt, camera):
        space_size = jovialengine.get_current_mode().get_space_size()
        if (self._speed < 0 and self.rect.right < 0) \
                or (self._speed > 0 and self.rect.left > space_size[0]):
            self.kill()

    def collide_Shot(self, other: Shot):
        self.kill()
        explosion = Explosion(center=self.rect.center)
        explosion.start()
