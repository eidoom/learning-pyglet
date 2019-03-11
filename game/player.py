import math
from pyglet.window import key
from . import physicalobject, resources


class Player(physicalobject.PhysicalObject):
    """Physical object that responds to user input"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.player_image, *args, **kwargs)

        # Set some easy-to-tweak constants
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.mass = 1.0

        # Let pyglet handle keyboard events for us
        self.key_handler = key.KeyStateHandler()

    def velocity_update(self, dt):
        # Do all the normal physics stuff
        super().velocity_update(dt)

        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force = self.thrust * dt
            force_x = math.cos(angle_radians) * force
            force_y = math.sin(angle_radians) * force
            acceleration_x = force_x / self.mass
            acceleration_y = force_y / self.mass
            self.velocity_x += acceleration_x
            self.velocity_y += acceleration_y
