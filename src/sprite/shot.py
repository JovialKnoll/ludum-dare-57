import jovialengine

import constants
import utility
from .shottrigger import ShotTrigger
from .explosion import Explosion


class Shot(ShotTrigger):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _IMAGE_SECTION_SIZE = (5, 5)
    _COLLISION_MASK_LOCATION = constants.SHOT_MASK
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
        '_age',
        'steering',
    )

    def _start(self, mode):
        self.angle: float = mode.arrow_angle
        self._accel = self._INITIAL_ACCEL
        self._speed = self._INITIAL_SPEED
        self._age = 0
        self.steering = True
        launch = jovialengine.load.sound(constants.LAUNCH)
        launch.play()

    def set_angle(self, angle):
        if self.steering:
            self.angle = angle

    def update(self, dt, camera):
        # shot thrust
        old_accel = self._accel
        self._accel += dt * self._JERK
        self._accel = min(self._accel, self._MAX_ACCEL)
        distance = dt * self._speed + (old_accel + self._accel) * dt * dt / 4
        self._speed += dt * self._accel
        self._speed = min(self._speed, self._MAX_SPEED)
        distance = min(distance, dt * self._MAX_SPEED)
        vec = utility.angle_vector(distance, self.angle)
        self.rect.move_ip(vec.x, vec.y)
        # shot sinking
        self.rect.move_ip(0, dt * 0.001 * 20)
        # aging
        self._age += dt
        if self.steering and self._age > 1000:
            self.steering = False
            self.seq = 1
            click = jovialengine.load.sound(constants.CLICK)
            click.play()
        # check bounds
        space_size = jovialengine.get_current_mode().get_space_size()
        if self.rect.top > space_size[1] \
                or self.rect.right < 0 or self.rect.left > space_size[0]:
            self.kill()

    def collide_ShotTrigger(self, other: ShotTrigger):
        self.kill()
        explosion = Explosion(center=self.rect.center)
        explosion.start()

    def collide_Explosion(self, other: Explosion):
        self.kill()
