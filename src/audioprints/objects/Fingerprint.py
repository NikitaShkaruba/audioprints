# coding=utf-8

# Класс, описывающий объект отпечатка в базе данных
class Fingerprint:
    song_id = 0
    offset = 0
    hash = None

    def __init__(self, song_id, offset, hash):
        self.song_id = song_id
        self.offset = offset
        self.hash = hash
