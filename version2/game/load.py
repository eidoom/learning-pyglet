import pyglet, math, random
from . import physicalobject, resources


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def player_lives(num_icons, batch=None):
    """Generate sprites for player life icons"""
    player_lives_list = []
    image = resources.player_image
    width = image.width
    scale = 0.5
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=image, x=800 - 15 - i * 30, y=600 - scale * width // 2, batch=batch)
        new_sprite.scale = scale
        player_lives_list.append(new_sprite)
    return player_lives_list


def asteroids(num_asteroids, player_position, batch=None):
    """Generate asteroid objects with random positions and velocities, not close to the player"""
    asteroids_list = []
    for i in range(num_asteroids):
        asteroid_x, asteroid_y = player_position
        while distance((asteroid_x, asteroid_y), player_position) < 100:
            asteroid_x = random.randint(0, 800)
            asteroid_y = random.randint(0, 600)
        new_asteroid = physicalobject.PhysicalObject(img=resources.asteroid_image,
                                                     x=asteroid_x, y=asteroid_y, batch=batch)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x, new_asteroid.velocity_y = random.random() * 40, random.random() * 40
        asteroids_list.append(new_asteroid)
    return asteroids_list
