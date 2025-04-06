import random

import jovialengine
import pygame

import constants
import utility
import sprite
from .modescreensize import ModeScreenSize
from .modeending import ModeEnding


class ModePlay(ModeScreenSize):
    _ANGLE_CAP_LEFT = 0
    _ANGLE_CAP_RIGHT = 180 - _ANGLE_CAP_LEFT
    _ANGLE_BASIS = 0.001 * 90
    _MAX_ANGLE_VEL = _ANGLE_BASIS * 2
    _SHOT_INIT_DISTANCE = 4
    _SHOT_TAIL_LENGTH = 9
    _MAX_SHOTS = 5
    __slots__ = (
        '_time',
        'ship',
        '_shots',
        '_arrow_vel',
        'arrow_angle',
        '_next_sub_positions',
    )

    def __init__(self):
        super().__init__()
        random.seed()
        announcement = jovialengine.load.sound(constants.ANNOUNCEMENT)
        announcement.play()
        # setup background
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen, (0, -260))
        self._background.fill(
            constants.WATER_BLUE,
            (0, constants.HORIZON, self._SPACE_SIZE[0], self._SPACE_SIZE[1]))
        # setup game objects
        self._time = 0
        self.ship = sprite.Ship(midbottom=(self._SPACE_SIZE[0] // 2, constants.HORIZON))
        self.ship.start(self)
        self._shots: pygame.sprite.Group[sprite.Shot] = pygame.sprite.Group()
        self._arrow_vel: float = 0
        self.arrow_angle: float = 90
        self._next_sub_positions = list(range(18))
        self._spawn_sub(1.0)

    def _take_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self._end_mode()

    def _take_frame(self, input_frame):
        if input_frame.was_input_pressed(constants.EVENT_S):
            if self._can_fire():
                pos = self._get_aim_end(self.ship.rect.midbottom, self._SHOT_INIT_DISTANCE)
                shot = sprite.Shot(self.arrow_angle, center=pos)
                shot.start(self)
                self._shots.add(shot)

    def _update_pre_sprites(self, dt):
        # aiming
        self.arrow_angle += dt * self._arrow_vel
        vel_change = 0
        accel_amount = dt * self._ANGLE_BASIS / 50
        clamp = False
        if self._input_frame.get_input_state(0, constants.EVENT_LEFT) > constants.STICK_THRESHOLD:
            vel_change -= accel_amount
        if self._input_frame.get_input_state(0, constants.EVENT_RIGHT) > constants.STICK_THRESHOLD:
            vel_change += accel_amount
        if vel_change == 0:
            if self._input_frame.get_input_state(0, constants.EVENT_DOWN) > constants.STICK_THRESHOLD:
                if self.arrow_angle > 90:
                    vel_change -= accel_amount
                if self.arrow_angle < 90:
                    vel_change += accel_amount
                clamp = True
            if self._input_frame.get_input_state(0, constants.EVENT_UP) > constants.STICK_THRESHOLD:
                if self.arrow_angle > 90:
                    vel_change += accel_amount
                if self.arrow_angle < 90:
                    vel_change -= accel_amount
        if self._arrow_vel < -self._MAX_ANGLE_VEL or self._arrow_vel > self._MAX_ANGLE_VEL:
            vel_change = 0
        old_vel = self._arrow_vel
        self._arrow_vel += vel_change
        self._arrow_vel = jovialengine.utility.clamp(self._arrow_vel, -self._MAX_ANGLE_VEL, self._MAX_ANGLE_VEL)
        self.arrow_angle += dt * (self._arrow_vel - old_vel) / 2
        if clamp:
            if abs(self.arrow_angle - 90) <= dt * self._MAX_ANGLE_VEL:
                self.arrow_angle = 90
                self._arrow_vel = 0
        elif vel_change == 0:
            if self._arrow_vel < 0:
                self._arrow_vel = min(0.0, self._arrow_vel + (accel_amount * 2))
            if self._arrow_vel > 0:
                self._arrow_vel = max(0.0, self._arrow_vel - (accel_amount * 2))
        self.arrow_angle = jovialengine.utility.clamp(self.arrow_angle, self._ANGLE_CAP_LEFT, self._ANGLE_CAP_RIGHT)
        for shot in self._shots.sprites():
            shot.set_angle(self.arrow_angle)
        # time progression
        self._time += dt
        if self.ship.alive():
            jovialengine.get_state().score += dt / 1000
        # ending
        if not self.sprites_all:
            self._end_mode()

    def _draw_pre_sprites(self, screen, offset):
        if self.ship.alive():
            start = pygame.Vector2(self.ship.rect.midbottom) + offset
            # line for aiming
            end = self._get_aim_end(start, 20)
            color = "red" if self._can_fire() else constants.DARK_RED
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
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (-1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (0, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (1, 1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (-1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (1, 0))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (-1, -1))
            self._draw_shot_trail(screen, constants.DARK_GREY, shot.angle, self._SHOT_TAIL_LENGTH, center + (1, -1))
            color = constants.GREY if shot.steering else constants.DARK_GREY
            self._draw_shot_trail(screen, color, shot.angle, self._SHOT_TAIL_LENGTH + 1, center + (0, -1))
            self._draw_shot_trail(screen, color, shot.angle, self._SHOT_TAIL_LENGTH + 1, center)

    def _draw_post_camera(self, screen: pygame.Surface):
        font_wrap = jovialengine.get_default_font_wrap()
        high_score = jovialengine.get_state().get_high_score()
        high_score_width = len(high_score) * constants.FONT_SIZE
        font_wrap.render_to(
            screen,
            (constants.SCREEN_SIZE[0] - high_score_width, 0),
            high_score,
            constants.BLACK
        )
        score = jovialengine.get_state().get_score()
        font_wrap.render_to(
            screen,
            (0, 0),
            score,
            constants.BLACK
        )

    def _cleanup(self):
        self._shots.empty()
        del self.ship

    @staticmethod
    def _get_angle_end(start: pygame.typing.Point, distance: int, angle: float):
        return utility.angle_vector(distance, angle) + start

    def _get_aim_end(self, start: pygame.typing.Point, distance: int):
        return self._get_angle_end(start, distance, self.arrow_angle)

    def _draw_shot_trail(self, screen, color: pygame.typing.ColorLike,
                         angle: float, length: int, start: pygame.typing.Point):
        end = self._get_angle_end(start, -length, angle)
        pygame.draw.line(screen, color, start, end)

    def _can_fire(self):
        return self.ship.alive() \
            and len(self._shots) < self._MAX_SHOTS

    def _spawn_sub(self, speed_factor: float):
        if self.ship.alive():
            self._spawn_sub_base(
                speed_factor,
                self._next_sub_positions.pop(),
                bool(random.getrandbits(1)))

    def _spawn_sub_base(self, speed_factor: float, position_factor: int, on_right: bool):
        # speed_factor=0.0: 0.001 * 120
        # speed_factor=1.0: 0.001 * 200
        # continuously varying speeds
        speed = 0.001 * (120 + speed_factor * 120)
        # position_factor=0: 181
        # position_factor=17: 351
        # 18 possible positions
        position = (
            self._SPACE_SIZE[0] if on_right else 0,
            self._SPACE_SIZE[1] // 2 + 10 * position_factor + 1,
        )
        if on_right:
            s = sprite.Sub(speed * -1, topleft=position)
        else:
            s = sprite.Sub(speed, topright=position)
        s.start(self)

    def _end_mode(self):
        self._stop_mixer()
        self.next_mode = ModeEnding()
