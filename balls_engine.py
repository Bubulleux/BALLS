
import easygraphics as g
import math
import time

RADIUS = 400
GRAVITY = 1


class Ball:
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0, size = 1, mass = 1, fix = False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.fix = fix
        self.have_colide = False

    def apply_force(self, fx, fy, dt):
        if self.fix:
            return
        self.dx += fx * dt
        self.dy += fy * dt

    def update(self, dt):
        if self.fix:
            return
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.have_colide = False

    def is_coliding(self, other):
        return ((self.dst(other) > abs(self.size + other.size)) ^ \
                (self.size * other.size > 0)) and not self.have_colide

    def dst(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def apply_bounce(self, other):
        dst = self.dst(other)
        invert = -1 if self.size * other.size < 0 else 1
        nx = (self.x - other.x) / dst * invert
        ny = (self.y - other.y) / dst * invert
        limite_dist = abs(self.size + other.size)
        # self.x += nx * (limite_dist - dst) * invert
        # self.y += ny * (limite_dist - dst) * invert
        product = self.dx * nx + self.dy * ny
        wx = self.dx - product * nx
        wy = self.dy - product * ny
        self.dx = wx - product * nx
        self.dy = wy - product * ny
        self.have_colide = True
        # self.dx *= 1.01
        # self.dy *= 1.01
        # self.size *= 1.05



def mainloop():

    X = RADIUS * 2
    Y = RADIUS * 2
    balls = [Ball(x = 0.1, y =  i * -0.1, size = 0.05, dx=1) for i in range(10)]
    balls = [Ball(size=0.3), Ball(x=-0.7, dx=0.5, size=0.1)]
    border = Ball(x = 0, y = 0, size = -1, fix = True)

    last_frame = time.time()

    while g.is_run():
        delta_time = time.time() - last_frame
        last_frame += delta_time
        for i, ball in enumerate(balls):
            # ball.apply_force(math.cos(last_frame), math.sin(last_frame), delta_time)
            ball.update(delta_time)
            if ball.is_coliding(border):
                ball.apply_bounce(border)
            for other in balls[i + 1:]:
                if ball.is_coliding(other):
                    ball.apply_bounce(other)
                    other.apply_bounce(ball)
                    print("Ball colide")
        


        if not g.delay_jfps(60):
            continue
        # g.clear_device()

        g.clear()
        g.set_fill_color(g.Color.BLACK)
        g.fill_polygon(0, 0, X, 0, X, Y, 0, Y)
        g.draw_polygon(50, 50, 350, 250, 50, 150)

        g.set_color(g.Color.BLACK)
        g.set_fill_color(g.Color.WHITE)


        g.draw_ellipse(RADIUS, RADIUS, RADIUS, RADIUS)

        g.set_color(g.Color.BLACK)
        g.set_fill_color(g.Color.WHITE)
        for ball in balls:
            g.draw_ellipse(RADIUS * (ball.x + 1), RADIUS * (ball.y + 1), ball.size * RADIUS, ball.size * RADIUS)


def main():
    g.init_graph(RADIUS * 2, RADIUS * 2)
    g.set_render_mode(g.RenderMode.RENDER_MANUAL)
    mainloop()
    g.close_graph()


g.easy_run(main)
