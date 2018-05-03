from audioprints.objects.Song import Song
from audioprints.storage.PostgreSQL import PostgreSQL

# Класс CRUD для работы с таблицей songs
class Songs:
    table_name = 'songs'

    def __init__(self):
        pass

    @staticmethod
    def insert(song):
        PostgreSQL.execute("""INSERT INTO %s (name, file_hash, is_fingerprinted) VALUES ('%s', '%s', %s)""" % (Songs.table_name, song.name, song.file_hash, song.is_fingerprinted))

    @staticmethod
    def selectByFileHash(file_hash):
        rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE file_hash = '%s'""" % (Songs.table_name, file_hash))

        songs = []
        for row in rows:
            songs.append(Song(row[1], row[2], row[3], row[0]))

        return songs

    @staticmethod
    def delete(song_id):
        PostgreSQL.execute("""DELETE FROM %s WHERE id = %s""" % (Songs.table_name, song_id))

    @staticmethod
    def createTable():
        PostgreSQL.execute("""
            CREATE TABLE %s (
                 id                 SERIAL,
                 name               VARCHAR(40),
                 file_hash          VARCHAR(40),
                 is_fingerprinted   BOOLEAN
            )""" % Songs.table_name)
