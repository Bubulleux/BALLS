import easygraphics as g
import scenes

FPS = 60

def init(width, height, main_loop, window_size):
    g.init_graph(width, height)
    g.set_render_mode(g.RenderMode.RENDER_MANUAL)
    g.set_window(*window_size)
    main_loop()
    g.close_graph()


def renderBallsSenes(scene: scenes.BallsScene):
    g.clear()
    balls = scene.balls
    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)

    g.set_color(g.Color.BLACK)
    g.set_fill_color(g.Color.WHITE)
    for ball in balls:
        g.circle(ball.x, ball.y, ball.size)
    g.delay_fps(FPS)


def saveFrame(file_name):
    g.save_image(file_name)


def is_runing():
    return g.is_run()


