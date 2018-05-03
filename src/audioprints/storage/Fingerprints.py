from audioprints.objects.Fingerprint import Fingerprint
from audioprints.storage.PostgreSQL import PostgreSQL


class Fingerprints:
    table_name = 'fingerprints'

    def __init__(self):
        pass

    @staticmethod
    def insert(fingerprint):
        PostgreSQL.execute("""INSERT INTO %s (song_id, song_offset, hash) VALUES (%s, %s, '%s')""" % (Fingerprints.table_name, fingerprint.song_id, fingerprint.offset, fingerprint.hash))
        pass

    @staticmethod
    def selectByHash(hash):
        rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE hash = '%s'""" % (Fingerprints.table_name, hash))

        fingerprints = []
        for row in rows:
            fingerprints.append(Fingerprint(row[0], row[1], row[2]))

        return fingerprints

    @staticmethod
    def delete(fingerprint):
        PostgreSQL.execute("""DELETE FROM %s WHERE song_id = %s AND song_offset = %s AND hash = '%s'""" % (Fingerprints.table_name, fingerprint.song_id, fingerprint.offset, fingerprint.hash))

    @staticmethod
    def createTable():
        PostgreSQL.execute("""
            CREATE TABLE %s (
                 song_id    INTEGER,
                 song_offset     INTEGER,
                 hash       VARCHAR(40),
                 PRIMARY KEY(song_id, song_offset, hash)
            )""" % Fingerprints.table_name)

    @staticmethod
    def createIndex():
        PostgreSQL.execute("""
            CREATE INDEX hash_index ON %s USING btree (hash);
        """ % Fingerprints.table_name)
