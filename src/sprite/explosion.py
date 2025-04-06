import jovialengine

import constants


class Explosion(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.EXPLOSION
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _IMAGE_SECTION_SIZE = (21, 21)
    _COLLISION_MASK_LOCATION = constants.EXPLOSION
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY

    __slots__ = (
        '_age',
    )

    def _start(self, mode):
        self._age = 0
        boom = jovialengine.load.sound(constants.BOOM)
        boom.play()

    def update(self, dt, camera):
        # aging
        self._age += dt
        seq_max = self._image_count_x * self._image_count_y
        for i in range(seq_max):
            if self.seq == i and self._age >= (i + 1) * 500:
                self.seq = i + 1
                self.mask_seq = i + 1
        if self._age >= (seq_max + 1) * 500:
            self.kill()
