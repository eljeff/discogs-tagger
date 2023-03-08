# components
from env import *
from utils_array_to_string import UtilsArrayToString

# packages
import style
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX

def TaggerWriteData(files, discogs):

    # print(discogs['json'])

    # artist
    artist = discogs['json'].get('artists_sort')
    print("artist is " + artist)

    # album
    album = discogs['json'].get('title')
    print("album is " + album)

    # label
    label = discogs['json'].get('labels')[0]['name']
    print("label is " + label)

    # country
    country = discogs['json'].get('country')
    print("country is " + country)

    if country is None:
        country = ''

    # date
    date = discogs['json'].get('year')
    print("date is " + str(date))

    # if date is not None:
    #     date = [date.replace('-', '/').replace('/00', '/01')]

    # genres
    genres = UtilsArrayToString(discogs['json'].get('genres'))
    
    # styles
    styles = UtilsArrayToString(discogs['json'].get('styles'))

    track_list = discogs['json'].get('tracklist')

    i = 0

    for file in files:
        i += 1

        track_artist = ''
        track_title = ''
        
        for track_info in track_list:
            position = track_info.get('position')
            if position != '':
                if int(position) == i:
                    track_title = track_info.get('title')

                    track_artists = track_info.get('artists')
                    if track_artists is not None and len(track_artists) > 0:
                        track_artist = track_artists[0].get('name')
                    else:
                        track_artist = artist

                    print("got info")
                    print(track_info)


        print("track_artist is " + track_artist)
        print("track_title is " + track_title)
        try:
            file_extension = file.rsplit('.', 1)[1]

            if file_extension == 'flac':
                f = FLAC(file)
                f['artist'] = track_artist
                f['albumartist'] = artist
                f['album'] = album
                f['title'] = track_title
                f['organization'] = label
                f['composer'] = genres
                f['genre'] = styles
                if date is not None: f['date'] = str(date)
                f['country'] = country
                # f['custom'] = ENV_TAGGING_DONE + ' ' + f['custom'][0]

                print("saving flac...")
                f.save()

                print("got flac")
                print(f['tracknumber'][0] + ' done')
            
            if file_extension == 'mp3':
                f = EasyID3(file)

                f['organization'] = label
                f['composer'] = genres
                f['genre'] = styles
                if date is not None: f['date'] = date

                f.save()
                
                f2 = ID3(file)

                f2.add(TXXX(
                    desc=u'country',
                    text=[country],
                ))

                f2.add(TXXX(
                    desc=u'Custom',
                    text=[str(ENV_TAGGING_DONE + ' ' + str(f2.get('TXXX:Custom')))]
                ))
                
                f2.save()

                print(f['tracknumber'][0] + ' done')
        except:
            print(style.red(ENV_ERROR_TAGGING))
            continue
