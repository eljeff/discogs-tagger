# components
from env import *
from utils_array_to_string import UtilsArrayToString

# packages
import style
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX

def TaggerWriteData(files, discogs, folder):

    # print(discogs['json'])
    print("processing " + folder)

    print("\n".join(files))

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

    catalog = discogs['json'].get('labels')[0].get('catno')
    label_id = discogs['json'].get('labels')[0].get('id')
    rating = discogs['json'].get('community').get('rating').get('average')
    released = discogs['json'].get('released')
    master_release_id = ''
    release_month = ''
    votes = ''

    track_list = discogs['json'].get('tracklist')
    total_discs = ''

    for track_info in track_list:
        position = track_info.get('position')
        if position != '':
            if position.find('.') >= 0:
                positions = position.split('.')
                total_discs = positions[0]

    i = 0

    for file in files:

        track_artist = ''
        track_artist_id = ''
        track_title = ''
        disc_number = ''
        track_number = ''
        vinyltrack = ''

        track_info = track_list[i]
        position = track_info.get('position')
        while position == '':
            track_info = track_list[i]
            position = track_info.get('position')
            i += 1

        if position.find('.') >= 0:
            positions = position.split('.')
            disc_number = positions[0]
            track_number = positions[1]
        
        track_title = track_info.get('title')
        track_artists = track_info.get('artists')
        if track_artists is not None and len(track_artists) > 0:
            track_artist = track_artists[0].get('name')
            track_artist_id = track_artists[0].get('id')
        else:
            track_artist = artist


        print("track_artist is " + track_artist)
        print("track_artist_id is " + str(track_artist_id))
        print("track_number is " + track_number)
        print("track_title is " + track_title)
        print("disc_number is " + disc_number)
        print("total_discs is " + total_discs)

# DISCOGS_ARTIST_ID:«multiple values» 27521; 1769553; 106537; 17689
# DISCOGS_CATALOG:VISLTD 3
# DISCOGS_COUNTRY:UK
# DISCOGS_LABEL:20:20 Vision
# DISCOGS_LABEL_ID:15
# DISCOGS_MASTER_RELEASE_ID:224033
# DISCOGS_RATING:3.88
# discogs_release_id:430851
# DISCOGS_RELEASE_MONTH:04
# DISCOGS_RELEASED:2005-04-18
# DISCOGS_VOTES:24
# STYLE:House; Electro; Tech House
# VINYLTRACK:«multiple values» A1; B1; B2
        try:
            file_extension = file.rsplit('.', 1)[1]

            if file_extension == 'flac':
                f = FLAC(file)
                f['artist'] = track_artist
                f['DISCOGS_ARTIST_ID'] = track_artist_id
                f['albumartist'] = artist
                f['album'] = album
                f['title'] = track_title
                f['tracknumber'] = track_number
                f['organization'] = label
                f['composer'] = genres
                f['genre'] = styles
                f['discnumber'] = disc_number
                f['total_discs'] = total_discs
                if date is not None: f['date'] = str(date)
                f['country'] = country
                # f['custom'] = ENV_TAGGING_DONE + ' ' + f['custom'][0]

                print("saving flac...")
                f.save()

                print("saved flac!")
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
        
        i += 1
