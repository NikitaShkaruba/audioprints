### Audioprints

Audioprints - Audio Fingerprinting made with ease

```
usage: audioprints [-h] [-a file_path] [-m file_path] [-v file_path] [-s song_name] [-d song_id]

optional arguments:
  -h, --help            show this help message and exit
  -a file_path, --add file_path
                        Adds audio from file_path to fingerprints database
  -m file_path, --match file_path
                        Matches audio from file_path with ones from our database
  -v file_path, --view file_path
                        Creates gui with spectogram and peaks for audio from file_path
  -s song_name, --search song_name
                        Searches for added to database audio by song_name, using 'LIKE %song_name%'
  -d song_id, --delete song_id
                        Deletes song from database by song_id
```
