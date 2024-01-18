from datetime import datetime
import balls_engine
import render
import audio
import scenes
import random
import time
import os

FPS = 60
VIDEO_COUNT = 10
render.FPS = FPS

RESULT_HEIGHT = 1920
RESULT_WIDTH = 1080
RENDER_SCALE = 0.5


def balls_generator():
    return [balls_engine.Ball(size=-1, fix=True),
            balls_engine.Ball(x=0.5, y=0, dx=random.random() * 2, size=0.1),
            balls_engine.Ball(x=-0.5, y=0, dx=random.random() * 2, size=0.2, mass=5)]


def on_colide(ball: balls_engine.Ball, other: balls_engine.Ball):
    if ball.fix:
        return
    ball.size *= 1.02
    ball.apply_force(ball.dx, ball.dy, 0.005)


def is_finish(scene: scenes.Scene):
    for ball in scene.balls:
        if ball.size >= 1:
            return True
    return False

def saveMovie(scene: scenes.BallsScene, duration):
    os.system("rm audio.wav")
    sound = audio.generate_sin_kick(300, 500, 0.05, 0.1)
    trame = []
    for t in scene.colisions:
        trame.append((t, sound))
    audio.generate_audio(trame, duration, "audio.wav")
    now = datetime.now()
    os.system(f"ffmpeg -framerate {FPS} -i result/%01d.png  -i audio.wav "
              f"-c:a aac -b:a 256k -ar 44100 -c:v libx264 -pix_fmt yuv420p "
              f"-preset faster -tune stillimage -shortest "
          f"-s {RESULT_WIDTH}x{RESULT_HEIGHT} 'movies/{str(now)}.mp4'")
    os.system("rm result/*")



def main():
    scene = scenes.BallsScene(balls_generator, (2, 0),
                              on_colide=on_colide, finish_check=is_finish)

    last_frame = time.time()
    frame = 0
    video_count = 0
    while render.is_runing():
        delta_time = time.time() - last_frame
        delta_time = 1 / FPS
        last_frame += delta_time
        scene.update(delta_time)
        render.renderBallsSenes(scene)
        render.saveFrame(f"result/{frame}.png")
        frame += 1
        if scene.is_finish():
            saveMovie(scene, frame / FPS)
            video_count += 1
            if video_count >= VIDEO_COUNT:
                return
            frame = 0
            last_frame = time.time()
            scene.reset()


if __name__ == "__main__":
    y_offset = (RESULT_HEIGHT - RESULT_WIDTH) / RESULT_WIDTH / 2
    print(y_offset)
    # render.init(int(RESULT_WIDTH * RENDER_SCALE), int(RESULT_HEIGHT * RENDER_SCALE), main, (-1, -1 - y_offset, 2, 2 + 2 * y_offset))
    render.init(int(RESULT_WIDTH * RENDER_SCALE), int(RESULT_WIDTH * RENDER_SCALE), main, (-1, -1, 2, 2))
