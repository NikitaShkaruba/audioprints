# coding=utf-8

from math import ceil
from audioprints.objects.Fingerprint import Fingerprint
from audioprints.storage.PostgreSQL import PostgreSQL

# Класс для работы с базой данных отпечатков
class Fingerprints:
    table_name = 'fingerprints'

    def __init__(self):
        pass

    @staticmethod
    def insertOne(fingerprint):
        Fingerprints.insertMany([ fingerprint ])

    @staticmethod
    def insertMany(fingerprints):
        values = []
        for fingerprint in fingerprints:
            values.append("""(%s, %s, '%s')""" % (fingerprint.song_id, fingerprint.offset, fingerprint.hash))

        values_string = ', '.join(values)

        PostgreSQL.execute("""INSERT INTO %s (song_id, song_offset, hash) VALUES %s""" % (Fingerprints.table_name, values_string))

    @staticmethod
    def selectOneByHash(hash):
        fingerprints = Fingerprints.selectManyByHashes([hash]);
        if len(fingerprints) == 0:
            return []

        return fingerprints[0]

    @staticmethod
    def selectManyByHashes(hashes):
        chunkified_hashes = Fingerprints.chunkifyHashes(hashes)

        fingerprints = []
        for hashes_chunk in chunkified_hashes:
            hashes_string = ','.join(map(lambda h: "'%s'" % h, hashes_chunk))

            rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE hash IN (%s)""" % (Fingerprints.table_name, hashes_string))
            for row in rows:
                fingerprints.append(Fingerprint(row[1], row[2], row[3], row[0]))

        return fingerprints

    # Группирует хеши по 500 в каждом чанке
    @staticmethod
    def chunkifyHashes(hashes):
        hashes_amount = len(hashes)

        hashes_in_chunk = 500
        chunks_amount = int(ceil(float(hashes_amount) / hashes_in_chunk))
        if chunks_amount <= 1:
            return [hashes]

        chunks = []
        for chunk_id in range(0, chunks_amount):
            min_index = hashes_in_chunk * chunk_id
            max_index = hashes_in_chunk * (chunk_id + 1)

            if max_index < hashes_amount:
                chunks.append(hashes[min_index:max_index])
            else:
                chunks.append(hashes[min_index:])

        return chunks

    @staticmethod
    def delete(fingerprint_id):
        PostgreSQL.execute("""DELETE FROM %s WHERE id = %s""" % (Fingerprints.table_name, fingerprint_id))

    @staticmethod
    def deleteAll():
        PostgreSQL.execute("""DELETE FROM %s WHERE 1 = 1""" % Fingerprints.table_name)

    @staticmethod
    def createTable():
        PostgreSQL.execute("""
            CREATE TABLE %s (
                 id             SERIAL,
                 song_id        INTEGER,
                 song_offset    INTEGER,
                 hash           VARCHAR(40)
            )""" % Fingerprints.table_name)

    @staticmethod
    def createIndex():
        PostgreSQL.execute("""
            CREATE INDEX hash_index ON %s USING btree (hash);
        """ % Fingerprints.table_name)
