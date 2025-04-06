import jovialengine

import constants


class Ship(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHIP
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SHIP
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY
    _GETS_INPUT = True

    _SPEED = 0.001 * 40

    def update(self, dt, camera):
        dx = 0
        if self._input_frame.get_input_state(0, constants.EVENT_L) > constants.STICK_THRESHOLD:
            dx -= dt * self._SPEED
        if self._input_frame.get_input_state(0, constants.EVENT_R) > constants.STICK_THRESHOLD:
            dx += dt * self._SPEED
        self.rect.move_ip(dx, 0)
