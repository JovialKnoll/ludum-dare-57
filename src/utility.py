import pygame


def angle_vector(distance: float, angle: float):
    vec = pygame.Vector2(-distance, 0)
    vec.rotate_ip(-angle)
    return vec


def get_angle_end(start: pygame.typing.Point, distance: int, angle: float):
    return angle_vector(distance, angle) + start
