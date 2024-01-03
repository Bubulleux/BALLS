import wave
import struct
import math

SAMPLE_RATE = 44100


def lerp(x, a, b):
    return a * (1 - x) + x * b


def generate_audio(audio_trame, duration, file_name):
    audio = [0 for i in range(int(SAMPLE_RATE * duration))]

    for time, cur_audio in audio_trame:
        start_frame = int(SAMPLE_RATE * time)
        max_frame =  max(len(cur_audio), len(audio) - start_frame)
        for i, value in enumerate(cur_audio[:max_frame]):
            audio[i + start_frame] += value
    with wave.open(file_name, "w") as f:
        _save_file(audio, f)


def _save_file(audio, file: wave.Wave_write):
    # Channel count, Sample width, Sample Rate, Sample Count, Compression
    file.setparams((1, 2, SAMPLE_RATE, len(audio), "NONE", "not compressed"))
    for sample in audio:
        file.writeframes(struct.pack('h', int(sample * 32767.0)))


def generate_sin_kick(frequency, start_frequenc, attack, release, start_volume=0.8, end_volume=0):
    audio = []
    duration = attack + release
    for i in range(int(duration * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        if t < attack:
            freq = lerp(t / attack, start_frequenc, frequency)
            volume = lerp(t / attack, end_volume, start_volume)
        else:
            freq = frequency
            volume = lerp((t - attack) / release, start_volume, end_volume)
        audio.append(math.sin(t * freq * 2 * math.pi) * volume)
    
    return audio


if __name__ == "__main__":
    sin_kick = generate_sin_kick(500, 500, 0.00, 0.1)
    trame = [(i, sin_kick) for i in range(4)]
    generate_audio(trame, 5, "test.wav")





