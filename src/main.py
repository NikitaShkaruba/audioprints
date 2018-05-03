#!/usr/bin/python
# coding=utf-8
# Точка входа распознавателя

import sys
import argparse

from audioprints import AudioPrints

if __name__ == '__main__':
    parser = argparse.ArgumentParser("audioprints", None, "AudioPrints: Audio Fingerprinting made with ease", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', '--add', metavar="file_path", help="Adds song to database by file_path")
    parser.add_argument('-v', '--view', metavar="file_path", help="Creates gui for song's spectogram and peaks")
    parser.add_argument('-r', '--recognize', nargs=1, choices=[ 'mic', 'file' ], help="Recognizes audio from microphone or file with some from audioprints database")
    parser.add_argument('-s', '--search', metavar="song_name", help="Searches database by song name, using 'LIKE %song_name%'")
    parser.add_argument('-d', '--delete', metavar="song_id", help="Deletes song from database")

    args = parser.parse_args()

    if args.add:
        file_path = args.add

        try:
            song_name = AudioPrints.add(file_path)
            print "Song %s successfully fingerprinted" % song_name
        except BaseException:
            print sys.exc_info()[1]

    elif args.view:
        file_path = args.view
        AudioPrints.view(file_path)

    elif args.recognize:
        print "Recognize is not implemented yet"
        pass

    elif args.search:
        song_name = args.search

        songs = AudioPrints.search(song_name)
        if len(songs) == 0:
            print "Songs not found"

        print "Found songs:"
        for song in songs:
            print "\tid: %s, name: %s" % (song.id, song.name)

        pass

    elif args.delete:
        print("Delete is not implemented yet")
        pass

    else:
        parser.print_help()
        sys.exit(0)
