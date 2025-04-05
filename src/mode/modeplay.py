import jovialengine
import pygame

import constants
import sprite
from .modescreensize import ModeScreenSize


class ModePlay(ModeScreenSize):
    _HORIZON = 40
    _ANGLE_CAP_LEFT = 6
    _ANGLE_CAP_RIGHT = 180 - _ANGLE_CAP_LEFT
    _ANGLE_BASIS = 0.001 * 90
    _SHOT_INIT_DISTANCE = 12
    _MAX_SHOTS = 1
    __slots__ = (
        '_ship',
        '_shots',
        '_arrow_vel',
        '_arrow_angle',
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.WHITE)
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        # should set up background more probably

        self._ship = sprite.Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        self._ship.start(self)
        self._shots = pygame.sprite.Group()
        self._arrow_vel: float = 0
        self._arrow_angle: float = 90

    def _take_frame(self, input_frame):
        if input_frame.was_input_pressed(constants.EVENT_A):
            if len(self._shots) < self._MAX_SHOTS:
                pos = self._get_aim_end(self._ship.rect.midbottom, self._SHOT_INIT_DISTANCE)
                shot = sprite.Shot(center=pos)
                shot.start(self)
                self._shots.add(shot)

    def _update_pre_sprites(self, dt):
        self._arrow_angle += dt * self._arrow_vel
        vel_change = 0
        angle_basis = self._ANGLE_BASIS
        if self._shots:
            angle_basis = self._ANGLE_BASIS / 2
        accel_amount = dt * angle_basis * 2
        extra_clamp = None
        if self._input_frame.get_input_state(0, constants.EVENT_LEFT) == 1:
            vel_change -= accel_amount
        if self._input_frame.get_input_state(0, constants.EVENT_RIGHT) == 1:
            vel_change += accel_amount
        if vel_change == 0:
            if self._input_frame.get_input_state(0, constants.EVENT_DOWN) == 1:
                if self._arrow_angle > 90:
                    vel_change -= accel_amount
                    extra_clamp = max
                if self._arrow_angle < 90:
                    vel_change += accel_amount
                    extra_clamp = min
            if self._input_frame.get_input_state(0, constants.EVENT_UP) == 1:
                if self._arrow_angle > 90:
                    vel_change += accel_amount
                if self._arrow_angle < 90:
                    vel_change -= accel_amount
        if self._arrow_vel < -angle_basis * 2 or self._arrow_vel > angle_basis * 2:
            vel_change = 0
        old_vel = self._arrow_vel
        self._arrow_vel += vel_change
        self._arrow_vel = jovialengine.utility.clamp(self._arrow_vel, -angle_basis * 2, angle_basis * 2)
        self._arrow_angle += dt * (self._arrow_vel - old_vel) / 2
        if extra_clamp:
            self._arrow_angle = extra_clamp(self._arrow_angle, 90)
            if self._arrow_angle == 90:
                self._arrow_vel = 0
        if vel_change == 0:
            if self._arrow_vel < 0:
                self._arrow_vel = min(0.0, self._arrow_vel + (accel_amount * 2))
            if self._arrow_vel > 0:
                self._arrow_vel = max(0.0, self._arrow_vel - (accel_amount * 2))

    def _update_pre_draw(self):
        self._arrow_angle = jovialengine.utility.clamp(self._arrow_angle, self._ANGLE_CAP_LEFT, self._ANGLE_CAP_RIGHT)

    def _draw_pre_sprites(self, screen, offset):
        if self._ship.alive() and len(self._shots) < self._MAX_SHOTS:
            start = pygame.Vector2(self._ship.rect.midbottom) + offset
            end = self._get_aim_end(start, 20)
            pygame.draw.line(screen, "red", start, end)

    def _draw_post_sprites(self, screen, offset):
        for shot in self._shots.sprites():
            center = pygame.Vector2(shot.rect.center) + offset
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (-1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (0, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (-1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (-1, -1))
            self._draw_shot_trail(screen, constants.DARK_GREY, self._SHOT_INIT_DISTANCE - 3, center + (1, -1))
            self._draw_shot_trail(screen, constants.GREY, self._SHOT_INIT_DISTANCE - 2, center + (0, -1))
            self._draw_shot_trail(screen, constants.GREY, self._SHOT_INIT_DISTANCE - 2, center)

    def _cleanup(self):
        self._shots.empty()
        del self._ship

    @staticmethod
    def _get_angle_end(start: pygame.typing.Point, distance: int, angle: float):
        vec = pygame.Vector2(-distance, 0)
        vec.rotate_ip(-angle)
        return start + vec

    def _get_aim_end(self, start: pygame.typing.Point, distance: int):
        return self._get_angle_end(start, distance, self._arrow_angle)

    def _draw_shot_trail(self, screen, color: pygame.typing.ColorLike, length: int, start: pygame.typing.Point):
        end = self._get_aim_end(start, -length)
        pygame.draw.line(screen, color, start, end)
