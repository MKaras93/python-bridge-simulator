import random

import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions

from game.hyperspace.classes import Hyperspace

options = DrawOptions()

window = pyglet.window.Window(800, 600, "Brackets")


# space
space = Hyperspace()
space.gravity = 0, 0
space.damping = 0.2
ct = 0

def create_circle_for_body(body: pymunk.Body, radius=10):
    circle = pymunk.Circle(body, radius=radius)
    space.add(circle)


# create initial bodies:


def get_ship():
    ship = space.create_ship((random.randint(0, 500), random.randint(0, 500)), 0)
    ship.engine_power = 500
    ship.engine_percent = 10
    create_circle_for_body(ship._body)
    ship.rotation_engine_power = 90
    ship.rotation_engine_percent = 50
    ship.angle = 0
    ship.target_angle = 160
    return ship


ships = [get_ship() for i in range (0, 4)]

# ship._body.apply_force_at_local_point((-900, 0))
# ship._body.apply_force_at_local_point((-1000, 0))

# _body = pymunk.Body(body_type=pymunk.Body.KINEMATIC, mass=0)
# _body.position = 500, 500
# _body.angle = math.radians(45)
# force = (10000, 10000)
# _body.apply_impulse_at_local_point(force)
# _body.velocity = -10, 0
# circle = pymunk.circle.create_box(_body, size=(100, 10))
# space.add(_body, circle)
# loop


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)


def update(dt):
    space.step(dt)  # Step the simulation one step forward
    try:
        update.ct += 1
    except AttributeError:
        update.ct = 0

    # if update.ct % 100 == 0:
    #     ship.angle += 90

    space.tick()

    if update.ct % 300 == 0:
        sign = random.choice((-1, 1))
        for ship in ships:
            new_value = random.randint(0, 360)
            print(f"setting new target angle to {new_value}. Current angle: {ship.angle}.")
            ship.target_angle = new_value
            pass
        # ship
        # if ship.engine_percent == 20:
        #     ship.engine_percent = 0
        # else:
        #     ship.engine_percent = 20

        # ship.angle += 25
        # pass

    # if update.engines_on:
    #     ship._body.apply_force_at_local_point((500, 0))
    # ship._body.apply_force_at_local_point((1000, 0))
    # print(ship._body.force)
    # print(ship._body.velocity)


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()


# def _fly_to_point(ship: HyperspaceShip, target_x, target_y):
#     ship.rotation_engine_percent = 0
#     ship.engine_percent = 0
#     angle = ship._body.position.get_angle_degrees_between(Vec2d(target_x, target_y))
#     print("angle:", angle)
#     ship.target_angle = ship.angle - angle
#     if ship.target_angle:
#         ship.rotation_engine_percent = 50
#
#     if ship.angle - ship.target_angle < 5:
#         ship.rotation_engine_percent = 0
#         distance = ship._body.position.get_distance((target_x, target_y))
#         print("distance to target:", distance)
#         ship.engine_percent = distance
#         if distance <= 10:
#             print("Target in sight!")