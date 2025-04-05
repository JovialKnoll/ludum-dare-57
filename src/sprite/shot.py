import jovialengine

import constants
import utility


class Shot(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SHIP
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY

    _JERK = 0.001 * 0.0004
    _INITIAL_ACCEL = 0.001 * -0.2
    _MAX_ACCEL = 0.001 * 0.4
    _INITIAL_SPEED = 0.001 * 240
    _MAX_SPEED = 0.001 * 480

    __slots__ = (
        'angle',
        '_accel',
        '_speed',
    )

    def _start(self, mode):
        self.angle: float = mode.arrow_angle
        self._accel = self._INITIAL_ACCEL
        self._speed = self._INITIAL_SPEED

    def set_angle(self, angle):
        self.angle = angle

    def update(self, dt, camera):
        old_accel = self._accel
        self._accel += dt * self._JERK
        self._accel = min(self._accel, self._MAX_ACCEL)
        distance = dt * self._speed + (old_accel + self._accel) * dt * dt / 4
        self._speed += dt * self._accel
        self._speed = min(self._speed, self._MAX_SPEED)
        distance = min(distance, dt * self._MAX_SPEED)
        vec = utility.angle_vector(distance, self.angle)
        self.rect.move_ip(vec.x, vec.y)
