#!/usr/bin/env python
# coding=UTF-8

import math
import random

import pyglet


class Parameters:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.border = 25
        self.reduced_width = self.width - self.border
        self.reduced_height = self.height - self.border


class Resources:
    def __init__(self):
        pyglet.resource.path = ['../resources']
        pyglet.resource.reindex()

        self.player_image = pyglet.resource.image("player.png")
        self.bullet_image = pyglet.resource.image("bullet.png")
        self.asteroid_image = pyglet.resource.image("asteroid.png")

        self.center_image(self.player_image)
        self.center_image(self.bullet_image)
        self.center_image(self.asteroid_image)

    @staticmethod
    def center_image(image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2


class Load:
    def __init__(self, resources_, parameters_):
        self._parameters = parameters_
        self._resources = resources_

    @staticmethod
    def distance(point_1=(0, 0), point_2=(0, 0)):
        """Returns the distance between two points"""
        return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

    def asteroids(self, num_asteroids, player_position):
        border = 25
        asteroids_list = []
        for i in range(num_asteroids):
            asteroid_x, asteroid_y = player_position
            while self.distance((asteroid_x, asteroid_y), player_position) < 100:
                asteroid_x = random.randint(border, self._parameters.reduced_width)
                asteroid_y = random.randint(border, self._parameters.reduced_height)
            new_asteroid = pyglet.sprite.Sprite(img=self._resources.asteroid_image, x=asteroid_x, y=asteroid_y)
            new_asteroid.rotation = random.randint(0, 360)
            asteroids_list.append(new_asteroid)
        return asteroids_list


parameters = Parameters()
resources = Resources()
load = Load(resources, parameters)

game_window = pyglet.window.Window(width=parameters.width, height=parameters.height)

score_label = pyglet.text.Label(text="Score: 0", x=10, y=parameters.reduced_height)
level_label = pyglet.text.Label(text="Version 1: Static Graphics",
                                x=parameters.width // 2, y=parameters.reduced_height, anchor_x='center')

player_ship = pyglet.sprite.Sprite(img=resources.player_image, x=parameters.width // 2, y=300)

asteroids = load.asteroids(3, player_ship.position)


@game_window.event
def on_draw():
    game_window.clear()

    level_label.draw()
    score_label.draw()

    player_ship.draw()

    for asteroid in asteroids:
        asteroid.draw()


if __name__ == '__main__':
    pyglet.app.run()
