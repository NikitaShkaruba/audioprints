#!/usr/bin/python
# coding=utf-8

# Точка входа в audioprints

import sys
import argparse
from audioprints import AudioPrints

if __name__ == '__main__':
    parser = argparse.ArgumentParser("audioprints", None, "AudioPrints: Audio Fingerprinting made with ease", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', '--add', metavar="file_path", help="Adds audio from file_path to fingerprints database")
    parser.add_argument('-m', '--match', metavar="file_path", help="Matches audio from file_path with ones from our database")
    parser.add_argument('-v', '--view', metavar="file_path", help="Creates gui with spectogram and peaks for audio from file_path")
    parser.add_argument('-s', '--search', metavar="song_name", help="Searches for added to database audio by song_name, using 'LIKE %song_name%'")
    parser.add_argument('-d', '--delete', metavar="song_id", help="Deletes song from database by song_id")

    args = parser.parse_args()

    if args.add:
        file_path = args.add

        try:
            song_name = AudioPrints.add(file_path)
            print "Song %s successfully fingerprinted" % song_name
        except BaseException:
            print sys.exc_info()[1]

    elif args.match:
        file_path = args.match

        try:
            song = AudioPrints.match(file_path)
            print "Song matched: %s - %s" % (song.id, song.name)
        except BaseException:
            print sys.exc_info()[1]

    elif args.view:
        file_path = args.view
        AudioPrints.view(file_path)

    elif args.search:
        song_name = args.search

        songs = AudioPrints.search(song_name)
        if len(songs) == 0:
            print "Songs not found"

        print "Found songs:"
        for song in songs:
            print "\tid: %s, name: %s" % (song.id, song.name)

    elif args.delete:
        song_id = args.delete

        try:
            deleted_song = AudioPrints.delete(song_id)
            print "Song deleted: %s - %s" % (deleted_song.id, deleted_song.name)
        except BaseException:
            print sys.exc_info()[1]

    else:
        parser.print_help()
        sys.exit(0)
