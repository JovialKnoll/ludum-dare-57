import jovialengine
import pygame

import constants
import sprite
from .modeopening import ModeOpening


class ModeEnding(ModeOpening, jovialengine.Saveable):
    _HORIZON = constants.SCREEN_SIZE[1] - constants.HORIZON
    _SCORE_TOP_LINE = constants.SCREEN_SIZE[1] // 6

    def save(self):
        return 0

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        return new_obj

    def __init__(self):
        super().__init__()
        title_screen = jovialengine.load.image(constants.TITLE_SCREEN)
        self._background.blit(title_screen)
        self._background.fill(
            constants.WATER_BLUE,
            (0, self._HORIZON, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        font_wrap = jovialengine.get_default_font_wrap()
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] - constants.HORIZON // 2 - 1),
            "press any key to continue",
            constants.SKY_BLUE,
            constants.WATER_BLUE
        )
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2 + 1, constants.SCREEN_SIZE[1] - constants.HORIZON // 2),
            "press any key to continue",
            constants.SKY_BLUE
        )
        font_wrap.render_to_centered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] - constants.HORIZON // 2),
            "press any key to continue",
            constants.WHITE
        )

        your_score_surf = font_wrap.render_inside(
            font_wrap.font.size("YOUR SCORE")[0],
            "YOUR SCORE",
            constants.DARK_RED,
            constants.CLOUD_GREY
        )
        your_score_surf = pygame.transform.scale2x(your_score_surf)
        your_score_rect = your_score_surf.get_rect()
        your_score_rect.bottomright = (constants.SCREEN_SIZE[0] // 2 - 40, self._SCORE_TOP_LINE)
        self._background.blit(your_score_surf, your_score_rect)
        your_score_rect.move_ip(0, your_score_rect.height)
        next_midtop = your_score_rect.midbottom

        score = jovialengine.get_state().get_score()
        score_surf = font_wrap.render_inside(
            font_wrap.font.size(score)[0],
            score,
            constants.BLACK,
            constants.CLOUD_GREY
        )
        score_surf = pygame.transform.scale2x(score_surf)
        score_rect = score_surf.get_rect()
        score_rect.midtop = next_midtop
        self._background.blit(score_surf, score_rect)

        jovialengine.get_state().enter_score()

        high_scores_surf = font_wrap.render_inside(
            font_wrap.font.size("HIGH SCORE")[0],
            "HIGH SCORE",
            constants.DARK_RED,
            constants.CLOUD_GREY
        )
        high_scores_surf = pygame.transform.scale2x(high_scores_surf)
        high_scores_rect = high_scores_surf.get_rect()
        high_scores_rect.bottomleft = (constants.SCREEN_SIZE[0] // 2 + 40, self._SCORE_TOP_LINE)
        self._background.blit(high_scores_surf, high_scores_rect)
        high_scores_rect.move_ip(0, high_scores_rect.height)
        next_midtop = high_scores_rect.midbottom

        for high_score in jovialengine.get_state().get_high_scores():
            high_score_surf = font_wrap.render_inside(
                font_wrap.font.size(high_score)[0],
                high_score,
                constants.BLACK,
                constants.CLOUD_GREY
            )
            high_score_surf = pygame.transform.scale2x(high_score_surf)
            high_score_rect = high_score_surf.get_rect()
            high_score_rect.midtop = next_midtop
            self._background.blit(high_score_surf, high_score_rect)
            next_midtop = high_score_rect.midbottom

    def _switch_mode(self):
        next_mode_cls = jovialengine.get_start_mode_cls()
        self.next_mode = next_mode_cls()
