# components
from env import *
from utils_array_to_string import UtilsArrayToString

# packages
import style
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX

def TaggerWriteData(files, discogs, folder):

    print("processing " + folder)

    # print("\n".join(files))

    # artist
    artist = discogs['json'].get('artists_sort')
    if artist.lower() == "various":
        artist = 'Compilations'
    print("artist is " + artist)

    # album
    album = discogs['json'].get('title')
    print("album is " + album)

    # label
    label = discogs['json'].get('labels')[0]['name']
    print("label is " + label)

    # country
    country = discogs['json'].get('country')
    if country is None:
        country = ''
    print("country is " + country)

    # date
    date = discogs['json'].get('year')
    print("date is " + str(date))

    # genres
    genres = UtilsArrayToString(discogs['json'].get('genres'))
    print("genres is " + genres)
    
    # styles
    styles = UtilsArrayToString(discogs['json'].get('styles'))
    print("styles is " + styles)

    catalog = discogs['json'].get('labels')[0].get('catno')
    print("catalog is " + catalog)
    label_id = discogs['json'].get('labels')[0].get('id')
    print("label_id is " + str(label_id))
    released = discogs['json'].get('released')
    print("released is " + released)
    # rating = discogs['json'].get('community').get('rating').get('average')
    # print("rating is " + rating)
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
    print("total_discs is " + total_discs)

    i = 0
    tracknumber = 1
    last_disc = 1
    disc_number = ''

    for file in files:

        track_artist = ''
        track_artist_id = ''
        track_title = ''
        track_position = ''
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
            track_position = positions[1]

        if not track_position.isnumeric:
            vinyltrack = track_position

        if last_disc != disc_number:
            tracknumber = 1
        
        track_title = track_info.get('title')
        track_artists = track_info.get('artists')
        if track_artists is not None and len(track_artists) > 0:
            track_artist = track_artists[0].get('name')
            track_artist_id = track_artists[0].get('id')
        else:
            track_artist = artist

        print("track_artist is " + track_artist)
        print("track_artist_id is " + str(track_artist_id))
        print("track_position is " + track_position)
        print("tracknumber is " + str(tracknumber))
        print("track_title is " + track_title)
        print("disc_number is " + disc_number)
        print("total_discs is " + total_discs)

        try:
            file_extension = file.rsplit('.', 1)[1]

            if file_extension == 'flac':
                f = FLAC(file)
                f['artist'] = track_artist
                f['albumartist'] = artist
                f['album'] = album
                f['title'] = track_title
                f['tracknumber'] = str(tracknumber)
                if vinyltrack != '': f['vinyltrack'] = vinyltrack
                f['organization'] = label
                f['genre'] = genres
                f['discnumber'] = disc_number
                f['total_discs'] = total_discs
                if date is not None: f['date'] = str(date)
                f['country'] = country
                f['DISCOGS_ARTIST_ID'] = str(track_artist_id)
                f['DISCOGS_CATALOG'] = catalog
                f['DISCOGS_COUNTRY'] = country
                f['DISCOGS_LABEL'] = label
                f['DISCOGS_LABEL_ID'] = str(label_id)
                f['DISCOGS_RELEASED'] = released
                f['STYLE'] = styles

                print("saving flac...")
                f.save()

                print("saved flac!")
                print(f['tracknumber'][0] + ' done')
            
            if file_extension == 'mp3':
                f = EasyID3(file)

                f['organization'] = label
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
        tracknumber += 1
        last_disc = disc_number
        print("i is " + str(i))
