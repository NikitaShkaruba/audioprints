# coding=utf-8

from audioprints.storage.Fingerprints import Fingerprints

# Класс для матчинга аудиозаписей
class Matcher:
    def __init__(self):
        pass

    #
    @staticmethod
    def matchFingerprints(matching_fingerprints):
        # Вытаскиваем идиентичные оптечатки с базы
        hashes = map(lambda f: f.hash, matching_fingerprints)
        stored_fingerprints = Fingerprints.selectManyByHashes(hashes)

        # Сдвигаем нашедшие с оффсетами, чтобы находить отрывки
        return Matcher.alignFingerprints(matching_fingerprints, stored_fingerprints)

    # Ищем отпечатки в одинаковых сдвигах по времени
    @staticmethod
    def alignFingerprints(fragment_fingerprints, stored_fingerprints):
        hash_offsets = {}
        for fingerprint in fragment_fingerprints:
            hash_offsets[fingerprint.hash] = fingerprint.offset

        same_offset_counter = {}
        largest_count = 0
        matched_song_id = -1

        for fingerprint in stored_fingerprints:
            offset_diff = fingerprint.offset - hash_offsets[fingerprint.hash]

            # Создаем ячейку в same_offset_counter, если таковой нет
            if offset_diff not in same_offset_counter:
                same_offset_counter[offset_diff] = {}
            if fingerprint.song_id not in same_offset_counter[offset_diff]:
                same_offset_counter[offset_diff][fingerprint.song_id] = 0

            # Увеличиваем количество
            same_offset_counter[offset_diff][fingerprint.song_id] += 1

            # Ищем максимального
            if same_offset_counter[offset_diff][fingerprint.song_id] > largest_count:
                largest_count = same_offset_counter[offset_diff][fingerprint.song_id]
                matched_song_id = fingerprint.song_id

        return matched_song_id
