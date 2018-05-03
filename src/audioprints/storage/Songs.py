# coding=utf-8

from audioprints.objects.Song import Song
from audioprints.storage.PostgreSQL import PostgreSQL

# Класс для работы с базой данных songs
class Songs:
    table_name = 'songs'

    def __init__(self):
        pass

    @staticmethod
    def insert(song):
        return PostgreSQL.executeInsert("""INSERT INTO %s (name, file_hash, is_fingerprinted) VALUES ('%s', '%s', %s) RETURNING id""" % (Songs.table_name, song.name, song.file_hash, song.is_fingerprinted))

    @staticmethod
    def selectOneByFileHash(file_hash):
        rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE file_hash = '%s'""" % (Songs.table_name, file_hash))
        if len(rows) == 0:
            return []

        row = rows[0]
        return Songs.mapRowToSong(row)

    @staticmethod
    def selectOneById(song_id):
        rows = PostgreSQL.executeFetch("""SELECT * FROM %s WHERE id = %s""" % (Songs.table_name, song_id))
        if len(rows) == 0:
            return []

        row = rows[0]
        return Songs.mapRowToSong(row)

    @staticmethod
    def selectByName(audio_name):
        rows = PostgreSQL.executeFetch("SELECT * FROM %s WHERE name ILIKE '%%%s%%'" % (Songs.table_name, audio_name))

        songs = []
        for row in rows:
            songs.append(Songs.mapRowToSong(row))

        return songs

    @staticmethod
    def mapRowToSong(row):
        return Song(row[1], row[2], row[3], row[0])

    @staticmethod
    def updateIsFingerprinted(song_id, is_fingerprinted):
        PostgreSQL.execute("""UPDATE %s SET is_fingerprinted = %s WHERE id = %s""" % (Songs.table_name, is_fingerprinted, song_id))

    @staticmethod
    def delete(song_id):
        PostgreSQL.execute("""DELETE FROM %s WHERE id = %s""" % (Songs.table_name, song_id))

    @staticmethod
    def deleteAll():
        PostgreSQL.execute("""DELETE FROM %s""" % Songs.table_name)

    @staticmethod
    def createTable():
        PostgreSQL.execute("""
            CREATE TABLE %s (
                 id                 SERIAL,
                 name               VARCHAR(40),
                 file_hash          VARCHAR(40),
                 is_fingerprinted   BOOLEAN
            )""" % Songs.table_name)
