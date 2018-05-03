# coding=utf-8

from audioprints.Decoder import Decoder
from audioprints import extractor, Matcher
import matplotlib.pyplot as plt

from audioprints.Matcher import Matcher
from audioprints.objects.Song import Song
from audioprints.storage.Fingerprints import Fingerprints
from audioprints.storage.Songs import Songs

# Главный класс, предоставляющий интерфейс для работы с аудио принтами - их добавлением, удалением и поиском
class AudioPrints:
    def __init__(self):
        print('sht')

    @staticmethod
    def add(audio_file_path):
        song_name = Decoder.getSongNameFromPath(audio_file_path)
        hash = Decoder.getSongFileHash(audio_file_path)
        if not (song_name or hash):
            raise Exception("No song name or hash")

        # Добавляем песню в бд, или же вытаскиваем уже существующую
        song = Songs.selectOneByFileHash(hash)
        if song and song.is_fingerprinted:
            raise Exception("Song already fingerprinted")
        elif not song:
            song_id = Songs.insert(Song(song_name, hash, False))
        else:
            song_id = song.id

        # Декодируем каналы
        channels, frame_rate = Decoder.decodeChannelsFromFile(audio_file_path)

        # Снимаем отпечатки
        fingerprints = set()
        for channel_number, channel_frequencies in enumerate(channels):
            fingerprints |= set(extractor.extractFingerprints(channel_frequencies, song_id, frame_rate))

        Fingerprints.insertMany(fingerprints)

        # Помечаем песню уже обработанной
        Songs.updateIsFingerprinted(song_id, True)

        return song_name

    @staticmethod
    def match(audio_file_path):
        channels, frame_rate = Decoder.decodeChannelsFromFile(audio_file_path)

        # Снимаем отпечатки с каналов
        fingerprints = []
        for channel in channels:
            fingerprints.extend(extractor.extractFingerprints(channel))

        # Ищем сматченную песню
        matched_song_id = Matcher.matchFingerprints(fingerprints)

        # Достаем песню
        return Songs.selectOneById(matched_song_id)

    @staticmethod
    def search(audio_name):
        return Songs.selectByName(audio_name)

    @staticmethod
    def view(audio_file_path):
        song_name = Decoder.getSongNameFromPath(audio_file_path)
        song_hash = Decoder.getSongFileHash(audio_file_path)
        if not (song_name or song_hash):
            raise Exception("No song name or hash")

        channels, frame_rate = Decoder.decodeChannelsFromFile(audio_file_path)

        for channel_number, channel_frequencies in enumerate(channels):
            spectogram = extractor.extractSpectogram(channel_frequencies, frame_rate)
            peaks = extractor.extractPeaks(channel_frequencies, frame_rate)

            # Подгоняем под структуру, в которую умеет matplotlib.pyplot
            frequencies = [peak.frequency for peak in peaks]
            times = [peak.time for peak in peaks]

            # Строим график график
            fig, ax = plt.subplots()
            ax.imshow(spectogram)
            ax.scatter(times, frequencies)
            ax.set_xlabel('Time')
            ax.set_ylabel('Frequency')
            ax.set_title("Spectrogram")
            plt.gca().invert_yaxis()
            plt.show()
