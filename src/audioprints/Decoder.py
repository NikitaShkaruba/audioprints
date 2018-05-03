# coding=utf-8

import os
import numpy as np
from pydub import AudioSegment
from hashlib import sha1

# Класс для декодирования mp3 фаила на каналы через ffmpeg
class Decoder:

    def __init__(self):
        pass

    # Читает все фаилы, поддерживаемые в pudub (ffmpeg) и возвращает данные
    # @param limit - количество секунд с начала фаила, если нужно ограничить время
    @staticmethod
    def decodeChannelsFromFile(filename, limit=None):
        audio_file = AudioSegment.from_file(filename)

        if limit:
            audio_file = audio_file[:limit * 1000]

        data = np.fromstring(audio_file._data, np.int16)

        channels = []
        for chn in xrange(audio_file.channels):
            channels.append(data[chn::audio_file.channels])

        return channels, audio_file.frame_rate

    # Генерирует хеш по содержимому для названия фаила
    @staticmethod
    def getSongFileHash(file_path, block_size =2 ** 20):
        name = sha1()

        with open(file_path, "rb") as opened_file:
            while True:
                buf = opened_file.read(block_size)
                if not buf:
                    break
                name.update(buf)

        return name.hexdigest().upper()

    # Вытаскивает название песни по @param path. Используется для понимания, какие по каким песням уже были расчитаны отпечатки
    @staticmethod
    def getSongNameFromPath(path):
        return os.path.splitext(os.path.basename(path))[0]
