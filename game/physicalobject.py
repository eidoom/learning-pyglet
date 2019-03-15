from math import cos

import pyglet

from . import parameters, util, asteroid


class PhysicalObject(pyglet.sprite.Sprite):
    """A sprite with physical properties such as velocity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Flag to remove this object from the game_object list
        self.dead = False

        # In addition to position, we have velocity
        self.velocity_x, self.velocity_y = 0.0, 0.0

        # List of new objects to go in the game_objects list
        self.new_objects = []

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers = []

        # Flags to toggle collision with bullets
        self.reacts_to_bullets = True
        self.is_bullet = False

        self.scattering = False

    def velocity_update(self, dt):
        """This method should be called every frame."""

        if self.scattering:
            if isinstance(self, asteroid.Asteroid):
                # v1 = (self.velocity_x, self.velocity_y)
                # v2 = self.scattering
                # axis = util.add_vectors(v1,v2)
                # # n = reversed(a)
                # # an = [c/sqrt(sum([x**2 for x in a])) for c in a]
                # cos_angle1 = util.angle_between_vectors(v1, axis)
                self.velocity_x = -self.velocity_x
                self.velocity_y = -self.velocity_y
            self.scattering = False

        # Update position according to velocity and time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if parameters.classic:
            # Wrap around the screen if necessary
            self.check_bounds()
        else:
            # Bouncy borders
            self.check_bounds_for_bounce()

    def check_bounds_for_bounce(self):
        radius = (self.width + self.height) / 4
        min_x = radius
        min_y = radius
        max_x = parameters.width - radius
        max_y = parameters.height - radius
        if self.x < min_x or self.x > max_x:
            self.velocity_x = - self.velocity_x
        if self.y < min_y or self.y > max_y:
            self.velocity_y = - self.velocity_y

    def check_bounds(self):
        """Use the classic Asteroids screen wrapping behavior"""
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = parameters.width + self.image.width / 2
        max_y = parameters.height + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):
        """Determine if this object collides with another"""

        # Ignore bullet collisions if we're supposed to
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False

        # Calculate distance between object centers that would be a collision,
        # assuming square resources
        collision_distance = self.image.width / 2 + other_object.image.width / 2

        # Get distance using position tuples
        actual_distance = util.distance(self.position, other_object.position)

        return actual_distance <= collision_distance

    def handle_collision_with(self, other_object):
        if isinstance(self, asteroid.Asteroid) and isinstance(other_object, asteroid.Asteroid):
            self.scattering = (other_object.velocity_x, other_object.velocity_y)
        elif other_object.__class__ is not self.__class__:
            # Set to False for testing
            self.dead = True
