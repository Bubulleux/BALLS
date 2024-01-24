import easygraphics as g

COLORS = g.Color


class Render:
    def __init__(self, width, height, view_port=(0, 0, 2), fps=60):
        self.width = int(width)
        self.height = int(height)
        self.center_x, self.center_y, self.real_width = view_port
        self.real_height = self.height * self.real_width / self.width

        self.offset_x = self.real_width / 2
        self.offset_y = self.real_height / 2

        self.factor_x = self.width / self.real_width
        self.factor_y = self.height / self.real_height

        self.fps = fps

    def _get_virtual_x(self, x):
        return (x + self.offset_x) * self.factor_x

    def _get_virtual_y(self, y):
        return (y + self.offset_y) * self.factor_y

    def run(self, main_loop):
        g.init_graph(self.width, self.height)
        g.set_render_mode(g.RenderMode.RENDER_MANUAL)
        main_loop(self)
        g.close_graph()

    def render_circle(self, x, y, size, border_color=COLORS.BLACK,
                      background_color=COLORS.WHITE, line_width=5):
        g.set_color(border_color)
        g.set_fill_color(background_color)
        g.set_line_width(line_width)
        g.draw_ellipse(self._get_virtual_x(x),
                        self._get_virtual_y(y),
                        size * self.factor_x,
                        size * self.factor_y)

    def set_bg_color(self, color):
        g.set_background_color(color)

    def clear(self):
        g.clear()

    def is_running(self):
        return g.is_run()

    def save_frame(self, file_name):
        g.save_image(file_name)

    def wait_next_frame(self):
        g.delay_fps(self.fps)
