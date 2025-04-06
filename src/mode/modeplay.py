import jovialengine
import pygame

import constants
import utility
import sprite
from .modescreensize import ModeScreenSize


class ModePlay(ModeScreenSize):
    _HORIZON = 40
    _ANGLE_CAP_LEFT = 0
    _ANGLE_CAP_RIGHT = 180 - _ANGLE_CAP_LEFT
    _ANGLE_BASIS = 0.001 * 90
    _SHOT_INIT_DISTANCE = 12
    _MAX_SHOTS = 5
    __slots__ = (
        '_ship',
        '_shots',
        '_arrow_vel',
        'arrow_angle',
    )

    def __init__(self):
        super().__init__()
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen, (0, -260))
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        # should set up background more probably

        self._ship = sprite.Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        self._ship.start(self)
        self._shots: pygame.sprite.Group[sprite.Shot] = pygame.sprite.Group()
        self._arrow_vel: float = 0
        self.arrow_angle: float = 90

    def _take_frame(self, input_frame):
        if input_frame.was_input_pressed(constants.EVENT_S):
            if len(self._shots) < self._MAX_SHOTS:
                pos = self._get_aim_end(self._ship.rect.midbottom, self._SHOT_INIT_DISTANCE)
                shot = sprite.Shot(center=pos)
                shot.start(self)
                self._shots.add(shot)

    def _update_pre_sprites(self, dt):
        self.arrow_angle += dt * self._arrow_vel
        vel_change = 0
        angle_basis = self._ANGLE_BASIS
        #if self._shots:
        #    angle_basis = self._ANGLE_BASIS / 2
        accel_amount = dt * angle_basis * 2
        extra_clamp = None
        if self._input_frame.get_input_state(0, constants.EVENT_LEFT) > constants.STICK_THRESHOLD:
            vel_change -= accel_amount
        if self._input_frame.get_input_state(0, constants.EVENT_RIGHT) > constants.STICK_THRESHOLD:
            vel_change += accel_amount
        if vel_change == 0:
            if self._input_frame.get_input_state(0, constants.EVENT_DOWN) > constants.STICK_THRESHOLD:
                if self.arrow_angle > 90:
                    vel_change -= accel_amount
                    extra_clamp = max
                if self.arrow_angle < 90:
                    vel_change += accel_amount
                    extra_clamp = min
            if self._input_frame.get_input_state(0, constants.EVENT_UP) > constants.STICK_THRESHOLD:
                if self.arrow_angle > 90:
                    vel_change += accel_amount
                if self.arrow_angle < 90:
                    vel_change -= accel_amount
        if self._arrow_vel < -angle_basis * 2 or self._arrow_vel > angle_basis * 2:
            vel_change = 0
        old_vel = self._arrow_vel
        self._arrow_vel += vel_change
        self._arrow_vel = jovialengine.utility.clamp(self._arrow_vel, -angle_basis * 2, angle_basis * 2)
        self.arrow_angle += dt * (self._arrow_vel - old_vel) / 2
        if extra_clamp:
            self.arrow_angle = extra_clamp(self.arrow_angle, 90)
            if self.arrow_angle == 90:
                self._arrow_vel = 0
        if vel_change == 0:
            if self._arrow_vel < 0:
                self._arrow_vel = min(0.0, self._arrow_vel + (accel_amount * 2))
            if self._arrow_vel > 0:
                self._arrow_vel = max(0.0, self._arrow_vel - (accel_amount * 2))
        self.arrow_angle = jovialengine.utility.clamp(self.arrow_angle, self._ANGLE_CAP_LEFT, self._ANGLE_CAP_RIGHT)
        for shot in self._shots.sprites():
            shot.set_angle(self.arrow_angle)

    def _update_pre_draw(self):
        for shot in self._shots.sprites():
            if shot.rect.top > self._SPACE_SIZE[1] \
                    or shot.rect.right < 0 \
                    or shot.rect.left > self._SPACE_SIZE[0]:
                shot.kill()

    def _draw_pre_sprites(self, screen, offset):
        if self._ship.alive():
            start = pygame.Vector2(self._ship.rect.midbottom) + offset
            # line for aiming
            end = self._get_aim_end(start, 20)
            color = "red" if len(self._shots) < self._MAX_SHOTS else constants.DARK_RED
            pygame.draw.line(screen, color, start, end)
            # various angles
            end = self._get_angle_end(start, 20, self._ANGLE_CAP_LEFT)
            screen.fill("red", (end, (1, 1)))
            screen.fill("red", (end + (1, 0), (1, 1)))
            end = self._get_angle_end(start, 20, self._ANGLE_CAP_RIGHT)
            screen.fill("red", (end, (1, 1)))
            screen.fill("red", (end + (-1, 0), (1, 1)))
            end = self._get_angle_end(start, 20, 90)
            screen.fill("red", (end, (1, 1)))
            screen.fill("red", (end + (0, -1), (1, 1)))
            end = self._get_angle_end(start, 20, 45)
            screen.fill("red", (end, (1, 1)))
            end = self._get_angle_end(start, 20, 135)
            screen.fill("red", (end, (1, 1)))

    def _draw_post_sprites(self, screen, offset):
        for shot in self._shots.sprites():
            center = pygame.Vector2(shot.rect.center) + offset
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (-1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (0, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (-1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (-1, -1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_INIT_DISTANCE - 3, center + (1, -1))
            color = constants.GREY if shot.steering else constants.DARK_GREY
            self._draw_shot_trail(screen, color, shot.angle, self._SHOT_INIT_DISTANCE - 2, center + (0, -1))
            self._draw_shot_trail(screen, color, shot.angle, self._SHOT_INIT_DISTANCE - 2, center)

    def _cleanup(self):
        self._shots.empty()
        del self._ship

    @staticmethod
    def _get_angle_end(start: pygame.typing.Point, distance: int, angle: float):
        return utility.angle_vector(distance, angle) + start

    def _get_aim_end(self, start: pygame.typing.Point, distance: int):
        return self._get_angle_end(start, distance, self.arrow_angle)

    def _draw_shot_trail(self, screen, color: pygame.typing.ColorLike,
                         angle: float, length: int, start: pygame.typing.Point):
        end = self._get_angle_end(start, -length, angle)
        pygame.draw.line(screen, color, start, end)
