import easygraphics as g
import math
import time

RADIUS = 400
GRAVITY = 1

def mainloop():
    x, y = 0.3, 0
    dx, dy = 0, 0
    size = 20

    X = RADIUS * 2
    Y = RADIUS * 2

    g.set_fill_color(g.Color.BLACK)
    c = g.get_fill_color()
    g.fill_polygon(0, 0, X, 0, X, Y, 0, Y)
    g.draw_polygon(50, 50, 350, 250, 50, 150)

    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)


    g.draw_ellipse(RADIUS, RADIUS, RADIUS, RADIUS)

    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)
    last_frame = time.time()

    while g.is_run():
        delta_time = time.time() - last_frame
        last_frame += delta_time
        x += dx * delta_time
        y += dy * delta_time
        dy += GRAVITY * delta_time
        dst = math.sqrt(x * x + y * y)
        if dst > 1 - size / RADIUS:
            nx = - x / dst
            ny = -y / dst
            max_dst = 1 - size / RADIUS
            x *= max_dst / dst
            y *= max_dst / dst
            product = ((dx * nx + dy * ny) / (nx * nx + ny * ny))
            wx = dx - product * nx
            wy = dy - product * ny
            dx = wx - product * nx
            dy = wy - product * ny
            dx *= 1.1
            dy *= 1.1
            size *= 1.1

        if not g.delay_jfps(60):
            continue
        # g.clear_device()

        g.draw_ellipse(RADIUS * (x + 1), RADIUS * (y + 1), size, size)


def main():
    g.init_graph(RADIUS * 2, RADIUS * 2)
    g.set_render_mode(g.RenderMode.RENDER_MANUAL)
    mainloop()
    g.close_graph()


g.easy_run(main)
