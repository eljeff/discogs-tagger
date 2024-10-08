# components
from env import *
from discogs_sleep import DiscogsSleep
from discogs_get_release_from_master import DiscogsGetReleaseFromMaster

# packages
import requests
import json
import mutagen
from mutagen.mp3 import MP3

def Discogs(files, sample_json, processed_ids):
    # get json
    discogs_api_base_url = 'https://api.discogs.com/releases/'
    file_extension = files[0].rsplit('.', 1)[1]

    # logics by extensions
    # FLAC
    if file_extension == 'flac':
        file = mutagen.File(files[0])
        
        release_id_arr = file.get('discogs_release_id')

        if release_id_arr is None:
            return None
        else:
            release_id = release_id_arr[0]
            discogs_id = release_id
            discogs_url = "https://www.discogs.com/release/" + str(release_id)

        print("discogs_id IS " + discogs_id)

    # MP3
    elif file_extension == 'mp3':
        file = MP3(files[0])

        if file.get('TXXX:Custom') is None:
            return None
        
        if str(file.get('TXXX:Custom'))[:4] == ENV_TAGGING_DONE:
            return ENV_TAGGING_DONE
        
        if str(file.get('TXXX:Custom'))[:4] == ENV_TAGGING_TODO:
            return ENV_TAGGING_TODO
        
        discogs_url = str(file.get('TXXX:Custom'))
        discogs_slug = discogs_url.rsplit('/', 1)[1]
        discogs_id = discogs_slug.split('-', 1)[0]

    if sample_json != '':
        return {
            'json': sample_json,
            'url': discogs_api_base_url + discogs_id,
            'discogs_id': discogs_id,
        }
    
    if discogs_id not in processed_ids:
        DiscogsSleep()
        response = requests.get(discogs_api_base_url + discogs_id)
        return {
            'json': json.loads(response.text),
            'url': discogs_api_base_url + discogs_id,
            'discogs_id': discogs_id,
        }
    else:
        print("already processed " + discogs_id)
        return ENV_ALREADY_PROCESSED

    