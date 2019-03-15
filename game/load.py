import random

import pyglet

from . import resources, parameters, util, asteroid


def player_lives(num_icons, batch=None):
    """Generate sprites for player life icons"""
    player_lives_list = []
    image = resources.player_image
    scale = 0.5
    width = image.width * scale
    height = image.height * scale
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(
            img=image, x=int(parameters.width - (i + 0.5) * width),
            y=int(parameters.height - height / 2 - parameters.margin), batch=batch)
        new_sprite.scale = scale
        new_sprite.rotation = 270
        player_lives_list.append(new_sprite)
    return player_lives_list


def asteroids(num_asteroids, player_position, batch=None):
    """Generate asteroid objects with random positions and velocities, not close to the player"""
    asteroid_max_velocity = parameters.asteroid_max_velocity
    player_block_radius = 100
    asteroid_block_radius = max(resources.asteroid_image.width, resources.asteroid_image.height)
    border_block_radius = 0 if parameters.classic else asteroid_block_radius // 2
    asteroids_list = []
    for i in range(num_asteroids):
        asteroid_x, asteroid_y = player_position
        while util.distance((asteroid_x, asteroid_y), player_position) < player_block_radius or \
                any([util.distance((asteroid_x, asteroid_y), old_asteroid.position) < asteroid_block_radius
                     for old_asteroid in asteroids_list]):
            asteroid_x = random.randint(border_block_radius, parameters.width - border_block_radius)
            asteroid_y = random.randint(border_block_radius, parameters.height - border_block_radius)
        new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x, new_asteroid.velocity_y = \
            random.random() * asteroid_max_velocity, random.random() * asteroid_max_velocity
        asteroids_list.append(new_asteroid)
    return asteroids_list
