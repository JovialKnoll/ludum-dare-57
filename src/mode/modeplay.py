import jovialengine
import pygame

import constants
from .modescreensize import ModeScreenSize
from sprite import Ship

class ModePlay(ModeScreenSize):
    _HORIZON = 40
    _ANGLE_BASIS = 0.001 * 90
    _MAX_SHOTS = 1
    __slots__ = (
        '_ship',
        '_shots',
        '_draw_arrow',
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

        self._ship = Ship(midbottom=(constants.SCREEN_SIZE[0] // 2, self._HORIZON))
        self._ship.start(self)
        self._shots = pygame.sprite.Group()
        self._draw_arrow = True
        self._arrow_vel = 0
        self._arrow_angle = 90

    def _take_frame(self, input_frame):
        if input_frame.was_input_pressed(constants.EVENT_A):
            if len(self._shots) < self._MAX_SHOTS:
                # create shot here
                pass
        pass

    def _update_pre_sprites(self, dt):
        self._arrow_angle += dt * self._arrow_vel
        vel_change = 0
        accel_amount = dt * self._ANGLE_BASIS * 2
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
        if self._arrow_vel < -self._ANGLE_BASIS * 2 or self._arrow_vel > self._ANGLE_BASIS * 2:
            vel_change = 0
        old_vel = self._arrow_vel
        self._arrow_vel += vel_change
        self._arrow_vel = jovialengine.utility.clamp(self._arrow_vel, -self._ANGLE_BASIS * 2, self._ANGLE_BASIS * 2)
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
        self._arrow_angle = jovialengine.utility.clamp(self._arrow_angle, 0, 180)

    def _draw_post_sprites(self, screen, offset):
        if self._draw_arrow and self._ship.alive():
            start = pygame.Vector2(self._ship.rect.midbottom) + offset
            end = self._get_aim_end(start)
            pygame.draw.line(screen, "red", start, end)

    def _cleanup(self):
        self._shots.empty()
        del self._ship

    def _get_aim_end(self, start: pygame.Vector2):
        vec = pygame.Vector2(-30, 0)
        vec.rotate_ip(-self._arrow_angle)
        return start + vec
