# [learning-pyglet](https://github.com/eidoom/learning-pyglet)

This follows the [in-depth game example](https://pyglet.readthedocs.io/en/latest/programming_guide/examplegame.html) section (with [source](https://github.com/pyglet/pyglet/tree/master/examples/game)) of the [documentation](https://pyglet.readthedocs.io/en/latest/index.html) for [`pyglet`](https://pyglet.org/), which explains the example game Astraea.

## Dependencies

* Uses
    * [`python3`](https://www.python.org/)
    * Python package `pyglet`
* Dependencies managed by [`pdm`](https://pdm-project.org/latest/)
    * Install dependencies with `pdm install`

## Running

* Run with `pdm run ./play.py`
* Control the spaceship with the keyboard WASD keys (although you can only thrust in the forward direction, so that S is redundant) and shoot with the spacebar. 

## Comments

* Currently working on making linear momentum physical
* Angular momentum currently unphysical (really spin since I mean rotations of asteroids)
* Child asteroids appear to orbit one another due to elastic collisions
* Need to calculate how to add random but momentum conserving transverse components when asteroids break apart
* Explosive rounds need to impart more momentum into child asteroid system
* Need to generalise code so can have random number of child asteroids created
* Could add torpedoes, which start with low velocity but accelerate themselves and have more explosive power
* Want to have player-bullet collisions for kinetic rounds, but not sure how to get around player immediately colliding with them since they're accelerating and bullet is not. Have set the initial separation larger for now, and players will have to know not to accelerate while shooting.
* Haven't nailed down the parent asteroid decay yet. Want child products to start closer and move apart
* Would be cool if engine exhaust plume pushed asteroids away, and also if bullets N3L pushed back the spaceship.

## Ad

Climb in your FTL carrot stick and take to the stars!
With your trusty peashooter, nothing can stop you!
But watch out for the ominously red coloured blobs that lurk in the void...
