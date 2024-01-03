from balls_engine import Ball
from abc import ABC


class Scene(ABC):
    def __init__(self):
        self.reset()

    def update(self, dt):
        ...

    def reset(self):
        ...


class BallsScene(Scene):
    def __init__(self, balls_generator, gravity, friction=1):
        self.generator = balls_generator
        self.balls = []
        self.gavity = gravity
        self.friction = friction
        super().__init__()

    def update(self, dt):
        for i, ball in enumerate(self.balls):
            # ball.apply_force(math.cos(last_frame), math.sin(last_frame), delta_time)
            gx, gy = self.gavity
            ball.apply_force(0, 1, dt)
            for other in self.balls[i + 1:]:
                if ball.is_coliding(other):
                    ball.apply_bounce(other, friction=self.friction)
                    other.apply_bounce(ball, friction=self.friction)

        for ball in self.balls:
            ball.update(dt)

    def reset(self):
        self.balls = self.generator()
