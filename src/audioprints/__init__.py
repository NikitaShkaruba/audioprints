# coding=utf-8

from audioprints import decoding, extracting
import matplotlib.pyplot as plt

# Главный класс, предоставляющий интерфейс для работы с аудио принтами - их добавлением, удалением и поиском
class AudioPrints:
    def __init__(self):
        print('sht')

    @staticmethod
    def add(audio_file_path):
        song_name = decoding.getSongNameFromPath(audio_file_path)
        song_hash = decoding.getSongHash(audio_file_path)
        if not (song_name or song_hash):
            raise Exception("No song name or hash")

        channels, frame_rate, file_hash = decoding.decodeChannelsFromFile(audio_file_path)

        hashes = set()
        for channel_number, channel_frequencies in enumerate(channels):
            hashes |= set(extracting.extractFingerprints(channel_frequencies, frame_rate))

        # Todo: add database saving
        return None

    @staticmethod
    def view(audio_file_path):
        song_name = decoding.getSongNameFromPath(audio_file_path)
        song_hash = decoding.getSongHash(audio_file_path)
        if not (song_name or song_hash):
            raise Exception("No song name or hash")

        channels, frame_rate, file_hash = decoding.decodeChannelsFromFile(audio_file_path)

        for channel_number, channel_frequencies in enumerate(channels):
            spectogram = extracting.extractSpectogram(channel_frequencies, frame_rate)
            peaks = extracting.extractPeaks(channel_frequencies, frame_rate)

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
