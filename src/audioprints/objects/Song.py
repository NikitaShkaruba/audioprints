# coding=utf-8

# Класс, описывающий объект песни в базе данных
class Song:
    id = 0
    name = None
    is_fingerprinted = False
    file_hash = None

    def __init__(self, name, file_sha1, is_fingerprinted, id = 0):
        self.id = id
        self.name = name
        self.file_hash = file_sha1
        self.is_fingerprinted = is_fingerprinted
