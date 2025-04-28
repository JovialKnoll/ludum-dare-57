import jovialengine
import pygame

import constants
import utility
from .sub import Sub
from .subshot import SubShot
from .explosion import Explosion



class Shot(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHOT
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _IMAGE_SECTION_SIZE = (9, 9)
    _COLLISION_MASK_LOCATION = constants.SHOT_MASK
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY

    _JERK = 0.001 * 0.0004
    _INITIAL_ACCEL = 0.001 * -0.2
    _MAX_ACCEL = 0.001 * 0.4
    _INITIAL_SPEED = 0.001 * 240
    _MAX_SPEED = 0.001 * 480
    _SHOT_TAIL_LENGTH = 9

    count = 0

    __slots__ = (
        'angle',
        '_accel',
        '_speed',
        '_age',
        'steering',
    )

    def __init__(self, angle: float, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle
        self._accel = self._INITIAL_ACCEL
        self._speed = self._INITIAL_SPEED
        self._age = 0
        self.steering = True

    def _start(self, mode):
        launch = jovialengine.load.sound(constants.LAUNCH)
        launch.play()
        Shot.count += 1

    def update(self, dt, camera):
        # get angle
        if self.steering:
            self.angle = jovialengine.get_current_mode().arrow_angle
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

    def draw_dynamic(self, screen: pygame.Surface, offset: pygame.typing.IntPoint):
        center = round(pygame.Vector2(self.rect.topleft)) + (4, 4) + offset
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (-1, 1))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (0, 1))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (1, 1))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (-1, 0))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (1, 0))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (-1, -1))
        self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_TAIL_LENGTH, center + (1, -1))
        color = constants.GREY if self.steering else constants.DARK_GREY
        self._draw_shot_trail(screen, color, self._SHOT_TAIL_LENGTH + 1, center + (0, -1))
        self._draw_shot_trail(screen, color, self._SHOT_TAIL_LENGTH + 1, center)

    def _draw_shot_trail(self, screen, color: pygame.typing.ColorLike, length: int, start: pygame.typing.Point):
        end = utility.get_angle_end(start, -length, self.angle)
        pygame.draw.line(screen, color, start, end)

    def kill(self):
        super().kill()
        Shot.count -= 1

    def collide_Sub(self, other: Sub):
        self.kill()
        if other.alive():
            jovialengine.get_state().score += constants.SCORE_SUB
        other.kill()
        pos = (pygame.Vector2(self.rect.center) + pygame.Vector2(other.rect.center)) / 2
        explosion = Explosion(center=pos)
        explosion.start()

    def collide_SubShot(self, other: SubShot):
        self.kill()
        if other.alive():
            jovialengine.get_state().score += constants.SCORE_SUBSHOT
        other.kill()
        pos = (pygame.Vector2(self.rect.center) + pygame.Vector2(other.rect.center)) / 2
        explosion = Explosion(center=pos)
        explosion.start()

    def collide_Explosion(self, other: Explosion):
        self.kill()
