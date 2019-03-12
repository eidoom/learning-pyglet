import pyglet

from game import load, player, parameters, asteroid

# Set up a window
game_window = pyglet.window.Window(width=parameters.width, height=parameters.height)

main_batch = pyglet.graphics.Batch()

score = 0
level = 1
game_over = False
num_asteroids = parameters.init_num_asteroids

# Set up the two top labels
score_label = pyglet.text.Label(
    text=f"Score: {score}", x=parameters.margin, y=parameters.reduced_height, batch=main_batch,
    font_size=parameters.std_text_size
)
level_label = pyglet.text.Label(
    text=f"Level: {level}", x=parameters.half_width, y=parameters.reduced_height, anchor_x='center', batch=main_batch,
    font_size=parameters.std_text_size
)

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0


def reset_level(num_lives=parameters.num_lives):
    global player_ship, player_lives, game_objects, event_stack_size, level, num_asteroids

    # Clear the event stack of any remaining handlers from other levels
    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    # Initialize the player sprite
    player_ship = player.Player(x=parameters.half_width, y=parameters.half_height, batch=main_batch)

    # Make a number of sprites to represent remaining lives
    player_lives = load.player_lives(num_lives, batch=main_batch)

    # Make some asteroids so we have something to shoot at
    asteroids = load.asteroids(num_asteroids, player_ship.position, batch=main_batch)

    # Store all objects that update each frame in a list
    game_objects = [player_ship] + asteroids

    # Add any specified event handlers to the event handler stack
    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1

    level_label.text = f"Level: {level}"


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    global score, level, game_over, num_asteroids

    player_dead = False
    victory = False

    # To avoid handling collisions twice, we employ nested loops of ranges.
    # This method also avoids the problem of colliding an object with itself.
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            # Make sure the objects haven't already been killed
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

    # Let's not modify the list while traversing it
    to_add = []

    # Initialise check for win condition
    asteroids_remaining = 0

    for obj in game_objects:
        obj.velocity_update(dt)

        to_add.extend(obj.new_objects)
        obj.new_objects = []

        # Check for win condition
        if isinstance(obj, asteroid.Asteroid):
            asteroids_remaining += 1

    if asteroids_remaining == 0:
        # Don't act on victory until the end of the time step
        victory = True

    # Get rid of dead objects
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True

        # Remove the object from any batches it is a member of
        to_remove.delete()

        # Remove the object from our list
        game_objects.remove(to_remove)

        # Bump the score if the object to remove is an asteroid
        if isinstance(to_remove, asteroid.Asteroid):
            score += 1
            score_label.text = f"Score: {score}"

    # Add new objects to the list
    game_objects.extend(to_add)

    # Check for win/lose conditions
    if player_dead:
        # We can just use the length of the player_lives list as the number of lives
        if len(player_lives) > 0:
            reset_level(len(player_lives) - 1)
        else:
            if not game_over:
                pyglet.text.Label(
                    text="GAME OVER", x=parameters.half_width, y=parameters.half_height, anchor_x='center',
                    batch=main_batch, font_size=4 * parameters.std_text_size
                )
                pyglet.text.Label(
                    text=f"Score: {score}", x=parameters.half_width,
                    y=parameters.half_height - 4 * parameters.std_text_size, anchor_x='center', batch=main_batch,
                    font_size=2 * parameters.std_text_size
                )
                game_over = True
            reset_level(0)
    elif victory:
        try:
            player_ship.delete()
        except AttributeError:
            pass
        score += 10
        level += 1
        num_asteroids += parameters.num_new_asteroids_on_reset
        reset_level(num_lives=len(player_lives))


if __name__ == "__main__":
    # Start it up!
    reset_level()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
