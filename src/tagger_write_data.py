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

    i = 0

    for file in files:
        i += 1
        track_title = discogs['json'].get('tracklist')[i].get('title')
        print("track_title is " + track_title)
        try:
            file_extension = file.rsplit('.', 1)[1]

            if file_extension == 'flac':
                f = FLAC(file)
                f['artist'] = artist
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
