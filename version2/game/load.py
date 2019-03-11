import math
import pyglet
import random

from . import physicalobject, resources, parameters


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def player_lives(num_icons, batch=None):
    """Generate sprites for player life icons"""
    player_lives_list = []
    image = resources.player_image
    scale = 0.5
    width = image.width * scale
    height = image.height * scale
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(
            img=image, x=int(parameters.width - (i + 0.5) * width), y=int(parameters.height - height / 2), batch=batch)
        new_sprite.scale = scale
        new_sprite.rotation = 270
        player_lives_list.append(new_sprite)
    return player_lives_list


def asteroids(num_asteroids, player_position, batch=None):
    """Generate asteroid objects with random positions and velocities, not close to the player"""
    asteroid_max_velocity = 40
    player_block_radius = 100
    asteroids_list = []
    for i in range(num_asteroids):
        asteroid_x, asteroid_y = player_position
        while distance((asteroid_x, asteroid_y), player_position) < player_block_radius:
            asteroid_x = random.randint(0, parameters.width)
            asteroid_y = random.randint(0, parameters.width)
        new_asteroid = physicalobject.PhysicalObject(
            img=resources.asteroid_image, x=asteroid_x, y=asteroid_y, batch=batch)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x, new_asteroid.velocity_y = \
            random.random() * asteroid_max_velocity, random.random() * asteroid_max_velocity
        asteroids_list.append(new_asteroid)
    return asteroids_list
