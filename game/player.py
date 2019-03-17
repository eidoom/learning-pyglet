from math import radians, cos, sin

import pyglet

from . import physicalobject, resources, bullet


class Player(physicalobject.PhysicalObject):
    """Physical object that responds to user input"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.player_image, *args, **kwargs)

        # Set some easy-to-tweak constants
        self.mass = 10.0
        self.thrust = 2000.0
        self.rotate_speed = 200.0
        self.bullet_speed = 700.0

        # Let pyglet handle keyboard events for us
        self.key_handler = pyglet.window.key.KeyStateHandler()

        # Tell the game handler about any event handlers
        self.event_handlers = [self, self.key_handler]

        # Create a child sprite to show when the ship is thrusting
        self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False

        self.reacts_to_bullets = True

        self.rotation = 270

    def velocity_update(self, dt):
        # Do all the normal physics stuff
        super().velocity_update(dt)

        controls_raw = {
            "forward": "W",
            "rotate_left": "A",
            "rotate_right": "D",
        }
        control = {key: getattr(pyglet.window.key, controls_raw[key]) for key in controls_raw.keys()}

        if self.key_handler[control["rotate_left"]]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[control["rotate_right"]]:
            self.rotation += self.rotate_speed * dt

        if self.key_handler[control["forward"]]:
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle_radians = -radians(self.rotation)
            force = self.thrust * dt
            force_x = cos(angle_radians) * force
            force_y = sin(angle_radians) * force
            acceleration_x = force_x / self.mass
            acceleration_y = force_y / self.mass
            self.velocity_x += acceleration_x
            self.velocity_y += acceleration_y

            # If thrusting, update the engine sprite
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
        else:
            # Otherwise, hide it
            self.engine_sprite.visible = False

    def delete(self):
        # We have a child sprite which must be deleted when this object
        # is deleted from batches, etc.
        self.engine_sprite.delete()
        super().delete()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.fire()

    def fire(self):
        # Note: pyglet's rotation attributes are in "negative degrees"
        angle_radians = -radians(self.rotation)

        # Create a new bullet just in front of the player
        initial_separation = self.radius + resources.bullet_image.width / 2 + 20

        bullet_x = self.x + cos(angle_radians) * initial_separation
        bullet_y = self.y + sin(angle_radians) * initial_separation
        new_bullet = bullet.Bullet(x=bullet_x, y=bullet_y, batch=self.batch)

        # Give it some speed
        bullet_vx = self.velocity_x + cos(angle_radians) * self.bullet_speed
        bullet_vy = self.velocity_y + sin(angle_radians) * self.bullet_speed
        new_bullet.velocity_x, new_bullet.velocity_y = bullet_vx, bullet_vy

        # Add it to the list of objects to be added to the game_objects list
        self.new_objects.append(new_bullet)
