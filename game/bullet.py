import pyglet

from . import physicalobject, resources, parameters


class Bullet(physicalobject.PhysicalObject):
    """Bullets fired by the player"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.bullet_image, *args, **kwargs)

        if parameters.explosive_rounds:
            # Bullets shouldn't stick around forever
            pyglet.clock.schedule_once(self.die, 0.5)
            self.mass = 1.0
        else:
            self.mass = 2.0

        self.is_bullet = True

        print(self.radius)

    def die(self, dt):
        self.dead = True
