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
        self.mass = mass
        self.forces = []

    def apply_force(self, fx, fy, dt):
        if self.fix:
            return
        self.forces.append((fx, fy, dt))

    def update(self, dt):
        if self.fix:
            return
        for fx, fy, fdt in self.forces:
            self.dx += fx * fdt
            self.dy += fy * fdt
        self.forces = []

        self.x += self.dx * dt
        self.y += self.dy * dt

    def is_coliding(self, other):
        return ((self.dst(other) > abs(self.size + other.size)) ^ \
                (self.size * other.size > 0))

    def dst(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def apply_bounce(self, other, friction=1):
        dst = self.dst(other)
        invert = -1 if self.size * other.size < 0 else 1
        nx = (self.x - other.x) / dst * invert
        ny = (self.y - other.y) / dst * invert
        limite_dist = abs(self.size + other.size)
        self.x += nx * (limite_dist - dst) * invert
        self.y += ny * (limite_dist - dst) * invert

        mass_factor = (2 * other.mass) / (self.mass + other.mass)
        if other.fix or math.isinf(other.mass):
            mass_factor = 2
        dst_square = self.dst(other) ** 2
        dot_product = (self.dx - other.dx) * (self.x - other.x) + \
            (self.dy - other.dy) * (self.y - other.y)
        factor = mass_factor * dot_product / dst_square
        dx = self.dx - factor * (self.x - other.x)
        dy = self.dy - factor * (self.y - other.y)

        dx *= friction
        dy *= friction
        self.apply_force(dx - self.dx, dy - self.dy, 1)
        # self.dx *= 1.01
        # self.dy *= 1.01
        # self.size *= 1.05


def calculate_energie(balls):
    result = 0
    for ball in balls:
        result += ball.mass * (ball.dx * ball.dx + ball.dy * ball.dy) / 2
    return result


def mainloop():
    X = RADIUS * 2
    Y = RADIUS * 2
    balls = [Ball(x = 0.1, y =  i * -0.1, size = 0.05, dx=1) for i in range(10)]
    # balls = [Ball(size=0.3, mass=2), Ball(x=-0.7, dx=0.5, dy=0.1, size=0.1, mass=1)]
    border = Ball(x = 0, y = 0, size = -1, fix = True)

    last_frame = time.time()
    frame = 0
    # g.set_background_color("black")

    while g.is_run():

        # g.clear_device()
        # if not g.delay_jfps(60):
        #     continue

        g.clear_device()
        img = g.create_image(RADIUS * 2, RADIUS * 2)
        g.set_background_color(g.Color.BLACK)
        g.set_target(img)
        # g.set_fill_color(g.Color.BLACK)
        # g.fill_polygon(0, 0, X, 0, X, Y, 0, Y)
        # g.draw_polygon(50, 50, 350, 250, 50, 150)

        g.save_image(f"./result/{frame}.png")
        g.set_target()
        g.draw_image(0, 0, img)
        img.close()
        frame += 1
        print(1 / delta_time)


def main():
    g.init_graph(RADIUS * 2, RADIUS * 2)
    g.set_render_mode(g.RenderMode.RENDER_MANUAL)
    mainloop()
    g.close_graph()


if __name__ == "__main__":
    g.easy_run(main)
