import random
from dataclasses import dataclass
import arcade
from gnp.arcadelib.actor import Actor, ActorList
from arcade.experimental.lights import Light, LightLayer
from arcade_screensaver_framework import screensaver_framework
from arcade_curtains import Curtains, BaseScene, KeyFrame, Sequence
from arcade_curtains.animation import AnimationManagerProxy


COIL_COUNT = 15
MIN_ARCS = 3
MAX_ARCS = 7
START_RADIUS = 25
RADIUS_STEP = 40
LINE_WIDTH = 30
MAX_ALPHA = 200


@dataclass
class Arc(Actor):
    parent_coil: object
    x: float
    y: float
    radius: float
    color: arcade.Color
    start_angle: float
    end_angle: float
    line_width: float
    angle: float
    angle_velocity: float

    def __post_init__(self):
        self.animate = AnimationManagerProxy(self)

    def start_anim(self):
        if random.random() > 0.85:
            return
        delay1 = random.uniform(0.5, 30.0)
        anim1 = random.uniform(10.0, 20.0)
        delay2 = random.uniform(0.5, 30.0)
        anim2 = random.uniform(10.0, 20.0)
        k1 = KeyFrame(
            angle=0
        )
        k2 = KeyFrame(
            angle=random.choice((-90, -180, -270, -360, 90, 180, 270, 360))
        )
        seq = Sequence(loop=True)
        # animate to given rotation and then bounce back
        seq.add_keyframe(0, k1)
        seq.add_keyframe(delay1, k1)
        seq.add_keyframe(delay1+anim1, k2)
        seq.add_keyframe(delay1+anim1+delay2, k2)
        seq.add_keyframe(delay1+anim1+delay2+anim2, k1)
        self.animate(seq)

    def draw(self):
        arcade.draw_arc_outline(self.x, self.y, self.radius * 2, self.radius * 2, self.color + (int(self.parent_coil.alpha),), self.start_angle, self.end_angle, self.line_width, self.angle)

    def can_reap(self):
        return False


@dataclass
class Coil(Actor):
    parent_scene: "SingleScene"
    x: float
    y: float
    start_radius: float
    radius_step: float
    arc_count: int
    arcs: ActorList = None
    alpha: float = 0
    alive: bool = True

    def __post_init__(self):
        self.animate = AnimationManagerProxy(self)
        self.arcs = ActorList()
        radii = [r*self.radius_step+self.start_radius for r in range(self.arc_count)]
        for idx, radius in enumerate(radii):
            angle_start = random.choice((0, 90, 180, 270))
            angle_size = random.choice((90, 180, 270))
            angle_end = angle_start + angle_size
            color = arcade.color.MIDNIGHT_BLUE if idx % 2 == 0 else arcade.color.DARK_BLUE_GRAY
            arc = Arc(self, self.x, self.y, radius, color, angle_start, angle_end, LINE_WIDTH, 0, 0.0)
            self.arcs.append(arc)

    def start_anim(self, parent_scene):
        for arc in self.arcs:
            arc.start_anim()
        alive_duration = random.uniform(10.0, 90.0)
        seq = Sequence()
        fade_duration = 6.0
        seq.add_keyframe(0.0, KeyFrame(alpha=0))
        seq.add_keyframe(fade_duration, KeyFrame(alpha=MAX_ALPHA))
        seq.add_keyframe(fade_duration + alive_duration, KeyFrame(alpha=MAX_ALPHA))
        seq.add_keyframe(fade_duration + alive_duration + fade_duration, KeyFrame(alpha=0), callback=self.coil_done)
        self.animate(seq)

    def coil_done(self):
        self.alive = False
        for arc in self.arcs:
            arc.animate.kill()
        self.parent_scene.add_coil()

    def draw(self):
        self.arcs.draw()

    def update(self, delta_time: float):
        pass

    def can_reap(self):
        return not self.alive


class SingleScene(BaseScene):
    def setup(self, win):
        left, self.screen_width, bottom, self.screen_height = win.get_viewport()
        self.coils = ActorList()
        self.light_layer = LightLayer(self.screen_width, self.screen_height)
        # self.light_layer.set_background_color(arcade.color.BLACK)
        radius = 1000
        b = arcade.color.MIDNIGHT_BLUE
        darken = 0.2
        light_color = b[0] * darken, b[1] * darken, b[2] * darken
        self.light1 = Light(0, 0, radius=radius, mode='soft', color=light_color)
        self.light_layer.add(self.light1)
        self.light2 = Light(0, 0, radius=radius, mode='soft', color=light_color)
        self.light_layer.add(self.light2)
        self.light3 = Light(0, 0, radius=radius, mode='soft', color=light_color)
        self.light_layer.add(self.light3)
        self.light4 = Light(0, 0, radius=radius, mode='soft', color=light_color)
        self.light_layer.add(self.light4)

    def add_coil(self):
        x = random.randint(0, self.screen_width)
        y = random.randint(0, self.screen_height)
        arc_count = random.randint(MIN_ARCS, MAX_ARCS)
        coil = Coil(self, x, y, START_RADIUS, RADIUS_STEP, arc_count)
        self.coils.append(coil)
        coil.start_anim(self)

    def enter_scene(self, previous_scene):
        for _ in range(COIL_COUNT):
            self.add_coil()
        self.add_anim_to_light(self.light1)
        self.add_anim_to_light(self.light2)
        self.add_anim_to_light(self.light3)
        self.add_anim_to_light(self.light4)

    def add_anim_to_light(self, light):
        light.animate = AnimationManagerProxy(light)
        elapsed = 0.0
        seq = Sequence(loop=True)
        for _ in range(10):
            key = KeyFrame(
                position=(random.randint(0, self.screen_width), random.randint(0, self.screen_height))
            )
            seq.add_keyframe(elapsed, key)
            elapsed += random.uniform(15.0, 30.0)
        light.animate(seq)

    def draw(self):
        with self.light_layer:
            arcade.draw_xywh_rectangle_filled(0, 0, self.screen_width, self.screen_height, arcade.color.WHITE)
        self.light_layer.draw(ambient_color=arcade.color.BLACK)
        self.coils.draw()
        self.coils.update(0.0)  # to make sure coils get reaped from ActorList


class RotatingArcsSaver(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curtains = Curtains(self)
        self.curtains.add_scene('single', SingleScene(self))
        self.curtains.set_scene('single')


def main():
    screensaver_framework.create_screensaver_window(RotatingArcsSaver)
    arcade.run()


if __name__ == "__main__":
    main()
