import math

import jovialengine
import pygame

import constants
import utility
from .ship import Ship
from .explosion import Explosion



class SubShot(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _IMAGE_SECTION_SIZE = (9, 9)
    _COLLISION_MASK_LOCATION = constants.SHOT
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
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = -90
        self._accel = self._INITIAL_ACCEL
        self._speed = self._INITIAL_SPEED
        self._age = 0

    def _start(self, mode):
        ship_pos = mode.ship.rect.center
        self_pos = self.rect.center
        rads = math.atan2(self_pos[1] - ship_pos[1], self_pos[0] - ship_pos[0])
        rads %= 2 * math.pi
        self.angle = 180 - math.degrees(rads)
        print(self.angle)
        sublaunch = jovialengine.load.sound(constants.SUBLAUNCH)
        sublaunch.play()

    def update(self, dt, camera):
        # shot thrust
        old_accel = self._accel
        self._accel += dt * self._JERK
        self._accel = min(self._accel, self._MAX_ACCEL)
        distance = dt * self._speed + (old_accel + self._accel) * dt * dt / 4
        self._speed += dt * self._accel
        self._speed = min(self._speed, self._MAX_SPEED)
        distance = min(-distance, dt * self._MAX_SPEED)
        vec = utility.angle_vector(distance, self.angle)
        self.rect.move_ip(vec.x, vec.y)
        # aging
        self._age += dt
        new_seq = (self._age // 100) % 2
        if self.seq != new_seq:
            self.seq = new_seq
        # check bounds
        space_size = jovialengine.get_current_mode().get_space_size()
        if self.rect.top > space_size[1] \
                or self.rect.right < 0 or self.rect.left > space_size[0]:
            self.kill()
        if self.rect.centery <= constants.HORIZON:
            self.kill()
            explosion = Explosion(center=self.rect.midbottom)
            explosion.start()

    def collide_Ship(self, other: Ship):
        self.kill()
        other.kill()
        pos = (pygame.Vector2(self.rect.center) + pygame.Vector2(other.rect.center)) / 2
        explosion = Explosion(center=pos)
        explosion.start()

    def collide_Explosion(self, other: Explosion):
        if self.alive():
            jovialengine.get_state().score += constants.SCORE_SUBSHOT_EXPLOSION
        self.kill()
