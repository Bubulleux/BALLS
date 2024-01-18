from balls_engine import Ball
from abc import ABC


class Scene(ABC):
    def __init__(self):
        self.reset()

    def update(self, dt):
        ...

    def reset(self):
        ...

    def is_finish(self):
        ...


class BallsScene(Scene):
    def __init__(self, balls_generator, gravity, friction=1, on_colide=None, 
                 finish_check=None):
        self.generator = balls_generator
        self.balls = []
        self.gavity = gravity
        self.friction = friction
        self.colisions = []
        self.time = 0
        self.finish_check = finish_check or (lambda _: False)
        self.on_colide = on_colide or (lambda _: None)
        super().__init__()

    def update(self, dt):
        self.time += dt
        for i, ball in enumerate(self.balls):
            # ball.apply_force(math.cos(last_frame), math.sin(last_frame), delta_time)
            gx, gy = self.gavity
            ball.apply_force(0, 1, dt)
            for other in self.balls[i + 1:]:
                if ball.is_coliding(other):
                    ball.apply_bounce(other, friction=self.friction)
                    other.apply_bounce(ball, friction=self.friction)
                    self.on_colide(ball, other)
                    self.on_colide(other, ball)
                    self.colisions.append(self.time)

        for ball in self.balls:
            ball.update(dt)

    def reset(self):
        self.balls = self.generator()
        self.colisions = []
        self.time = 0

    def is_finish(self):
        return self.finish_check(self)


