import random

from . import resources, physicalobject, parameters


class Asteroid(physicalobject.PhysicalObject):
    """An asteroid that divides a little before it dies"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.asteroid_image, *args, **kwargs)

        self.rotate_speed = random.random() * 50.0

    def velocity_update(self, dt):
        super().velocity_update(dt)
        self.rotation += self.rotate_speed * dt

    def handle_collision_with(self, other_object):
        super().handle_collision_with(other_object)

        if self.dead and self.scale > parameters.min_asteroid_fraction:
            num_asteroids = random.randint(2, 3)
            shrink_factor = 1 / num_asteroids
            for i in range(num_asteroids):
                new_mass = self.mass * shrink_factor
                new_asteroid = Asteroid(x=self.x, y=self.y, mass=new_mass, batch=self.batch)
                new_asteroid.rotation = random.randint(0, 360)
                new_asteroid.velocity_x = (random.random() * 70 + self.velocity_x)
                new_asteroid.velocity_y = (random.random() * 70 + self.velocity_y)
                new_asteroid.scale = self.scale * shrink_factor
                self.new_objects.append(new_asteroid)
