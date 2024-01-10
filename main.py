from datetime import datetime
import balls_engine
import render
import audio
import scenes
import random
import time
import os

FPS = 60
render.FPS = FPS


def balls_generator():
    return [balls_engine.Ball(x=0.5, y=0, dx=random.random, size=0.3),
            balls_engine.Ball(x=-0.5, y=0, dx=random.random, size=0.4)]

def saveMovie(scene: scenes.BallsScene, duration):
    sound = audio.generate_sin_kick(400, 500, 0.1, 0.2)
    trame = []
    for t in scene.colisions:
        trame.append((t, sound))
    audio.generate_audio(trame, duration, "audio.wav")
    now = datetime().now()
    os.system(f"ffmpeg -r {FPS} -i result/%01d.png -vcodec mpeg4 -y {str(now)}.mkv")
    os.system("rm result/* audio.wav")



def main():
    scene = scenes.BallsScene()

    last_frame = time.time()
    frame = 0
    while render.is_runing():
        delta_time = time.time() - last_frame
        delta_time = 1 / FPS
        last_frame += delta_time
        
        scene.update(delta_time)
        render.renderBallsSenes(scene)
        render.saveFrame(f"result/{frame}.png")
        frame += 1
        if frame > 120:
            saveMovie(scene, frame / FPS)
            return
        
