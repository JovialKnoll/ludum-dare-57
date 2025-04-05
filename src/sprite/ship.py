import jovialengine

import constants


class Ship(jovialengine.GameSprite):
    _IMAGE_LOCATION = constants.SHIP
    _ALPHA_OR_COLORKEY = constants.COLORKEY
    _COLLISION_MASK_LOCATION = constants.SHIP
    _COLLISION_MASK_ALPHA_OR_COLORKEY = constants.COLORKEY
    #_GETS_INPUT = True

    def update(self, dt, camera):
        pass
