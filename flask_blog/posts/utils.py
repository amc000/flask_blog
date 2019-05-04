import os, secrets
from PIL import Image
from flask import url_for, current_app
from pydub import AudioSegment

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\\post_pics', picture_fn)

    i = Image.open(form_picture)

    i.save(picture_path)

    return picture_fn

def save_track(form_track):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_track.filename)
    track_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static\\full_tracks', track_fn)
    snippet_path = os.path.join(current_app.root_path, 'static\\snippet_tracks', track_fn)

    i = AudioSegment.from_file('static\\full_tracks', track_fn)
    tag = AudioSegment.from_file('static\\WavFarm Tag.wav')

    # Must be a way to make this a bit nicer. Tag the audio at 0s, 10s, 20s outputting a 30s snippet.
    snippet = i.overlay(tag)
    snippet = snippet.overlay(tag, position=10000)
    snippet = snippet.overlay(tag, position=20000)

    return track_fn

'''
from pydub import AudioSegment

sound1 = AudioSegment.from_file("/path/to/my_sound.wav")
sound2 = AudioSegment.from_file("/path/to/another_sound.wav")

combined = sound1.overlay(sound2)

combined.export("tagged.wav", format='wav')
'''