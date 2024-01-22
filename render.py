import easygraphics as g
import scenes

FPS = 60
COLORS = g.Color

def init(width, height, main_loop, window_size):
    g.init_graph(width, height)
    g.set_render_mode(g.RenderMode.RENDER_MANUAL)
    g.set_window(*window_size)
    main_loop()
    g.close_graph()


def renderBallsSenes(scene: scenes.BallsScene):
    g.clear()
    balls = scene.balls
    g.set_line_width(5)
    g.set_background_color(g.Color.BLACK)
    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)

    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)
    for ball in balls:
        g.draw_ellipse(ball.x, ball.y, ball.size, ball.size)
    g.delay_fps(FPS)


def saveFrame(file_name):
    g.save_image(file_name)


def is_runing():
    return g.is_run()


class Render:
    def __init__(self, width, height, view_port=(0, 0, 2)):
        self.width = width
        self.height = height
        self.center_x, self.center_y, self.real_width = view_port
        self.real_height = self.height * self.real_width / self.width

        self.offset_x = self.real_width / 2
        self.offset_y = self.real_height / 2

        self.factor_x = self.width / self.real_width
        self.factor_y = self.height / self.real_height

    def _get_virtual_x(self, x):
        return (x + self.offset_x) * self.factor_x

    def _get_virtual_y(self, y):
        return (y + self.offset_y) * self.factor_y

    def run(self, main_loop):
        g.init_graph(self.width, self.height)
        g.set_render_mode(g.RenderMode.RENDER_MANUAL)
        main_loop()
        g.close_graph()

    def render_circle(self, x, y, size, border_color=COLORS.BLACK,
                      background_color=COLORS.WHITE)


