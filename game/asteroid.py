from random import random, randint

from . import resources, physicalobject, parameters, bullet


class Asteroid(physicalobject.PhysicalObject):
    """An asteroid that divides a little before it dies"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.asteroid_image, *args, **kwargs)

        self.mass = 15.0
        self.rotate_speed = random() * 50.0

    def velocity_update(self, dt):
        super().velocity_update(dt)
        self.rotation += self.rotate_speed * dt

    def handle_collision_with(self, other_object):
        super().handle_collision_with(other_object)

        if (
            self.dead
            and self.scale > parameters.min_asteroid_fraction
            and isinstance(other_object, bullet.Bullet)
        ):
            vx, vy = self.scattering
            # num_asteroids = randint(2, 3)
            num_asteroids = 2
            new_radius = self.radius / num_asteroids
            initial_half_separation = new_radius + 5
            sign = 1
            for i in range(num_asteroids):
                x = self.x + sign * initial_half_separation
                y = self.y + sign * initial_half_separation
                new_asteroid = Asteroid(x=x, y=y, batch=self.batch)
                new_asteroid.mass = self.mass / num_asteroids
                new_asteroid.rotation = randint(0, 360)
                # Need to calculate how to add random but momentum conserving transverse components
                new_asteroid.velocity_x = vx + (random() - 0.5) * 10.0
                new_asteroid.velocity_y = vy + (random() - 0.5) * 10.0
                new_asteroid.scale = self.scale / num_asteroids
                self.new_objects.append(new_asteroid)
                sign = -1
