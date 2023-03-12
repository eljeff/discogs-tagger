# components
from env import *
from utils_array_to_string import UtilsArrayToString

# packages
import style
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX

def addTagIfPresent(tag, destination, file):
    if tag is not None and str(tag) != '':
        file[destination] = str(tag)
        print("writing " + str(tag) + " to " + destination)
    else:
        print(destination + " not present (" + str(tag) + ") - skipping")
    return


def TaggerWriteData(files, discogs, folder):

    print("processing " + folder)

    artist = discogs['json'].get('artists_sort')
    if artist.lower() == "various":
        artist = 'Compilations'
    print("artist is " + artist)

    album = discogs['json'].get('title')
    print("album is " + album)

    label = discogs['json'].get('labels')[0]['name']
    print("label is " + label)

    country = discogs['json'].get('country')
    if country is None:
        country = ''
    print("country is " + country)

    date = discogs['json'].get('year')
    print("date is " + str(date))

    genres = UtilsArrayToString(discogs['json'].get('genres'))
    print("genres is " + genres)
    
    styles = UtilsArrayToString(discogs['json'].get('styles'))
    print("styles is " + styles)

    catalog = discogs['json'].get('labels')[0].get('catno')
    print("catalog is " + catalog)

    label_id = discogs['json'].get('labels')[0].get('id')
    print("label_id is " + str(label_id))

    released = discogs['json'].get('released')
    print("released is " + released)

    track_list = discogs['json'].get('tracklist')
    total_discs = ''

    total_track_count = []

    track_i = 0
    current_disc = 1
    for track_info in track_list:
        position = track_info.get('position')
        if position != '':
            if position.find('.') >= 0:
                positions = position.split('.')
                if current_disc != int(positions[0]):
                    total_track_count.append(track_i)
                    print("got new disc - last track count was " + str(track_i))
                    track_i = 0
                current_disc = int(positions[0])
                total_discs = str(current_disc)
        track_i += 1

    total_track_count.append(track_i)
    print("done counting - last track count was " + str(track_i))
    print("total_discs is " + total_discs)

    i = 0
    tracknumber = 1
    last_disc = 1
    disc_number = 1

    for file in files:

        track_artist = ''
        track_artist_id = ''
        track_title = ''
        track_position = ''
        vinyltrack = ''

        track_info = track_list[i]
        position = track_info.get('position')
        while position == '':
            i += 1
            track_info = track_list[i]
            position = track_info.get('position')

        if position.find('.') >= 0:
            positions = position.split('.')
            disc_number = int(positions[0])
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

        totaltracks = total_track_count[disc_number - 1]

        try:
            file_extension = file.rsplit('.', 1)[1]

            if file_extension == 'flac':
                f = FLAC(file)
                addTagIfPresent(track_artist, 'artist', f)
                addTagIfPresent(artist, 'albumartist', f)
                addTagIfPresent(album, 'album', f)
                addTagIfPresent(track_title, 'title', f)
                addTagIfPresent(tracknumber, 'tracknumber', f)
                addTagIfPresent(totaltracks, 'totaltracks', f)
                addTagIfPresent(vinyltrack, 'vinyltrack', f)
                addTagIfPresent(label, 'organization', f)
                addTagIfPresent(genres, 'genre', f)
                if total_discs != '' and int(total_discs) > 1:
                    addTagIfPresent(disc_number, 'discnumber', f)
                    addTagIfPresent(total_discs, 'totaldiscs', f)
                addTagIfPresent(date, 'date', f)
                addTagIfPresent(country, 'country', f)
                addTagIfPresent(track_artist_id, 'DISCOGS_ARTIST_ID', f)
                addTagIfPresent(catalog, 'DISCOGS_CATALOG', f)
                addTagIfPresent(country, 'DISCOGS_COUNTRY', f)
                addTagIfPresent(label, 'DISCOGS_LABEL', f)
                addTagIfPresent(label_id, 'DISCOGS_LABEL_ID', f)
                addTagIfPresent(released, 'DISCOGS_RELEASED', f)
                addTagIfPresent(styles, 'STYLE', f)

                print("saving flac...")
                f.save()

                print("saved flac!")
            
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
