from audioprints.objects.Fingerprint import Fingerprint
from audioprints.storage.PostgreSQL import PostgreSQL


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
    def selectByHash(hash):
        rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE hash = '%s'""" % (Fingerprints.table_name, hash))

        fingerprints = []
        for row in rows:
            fingerprints.append(Fingerprint(row[1], row[2], row[3], row[0]))

        return fingerprints

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
