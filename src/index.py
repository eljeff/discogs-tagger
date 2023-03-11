# components
from env import *
from folder import Folder
from file import File
from discogs import Discogs
from tagger import Tagger

# packages
import style
import logging
import traceback
import os
import json

folders = Folder(ENV_PATHS)
sample_json = ''

if DISCOGS_SAMPLE_FILE != '':
    print(DISCOGS_SAMPLE_FILE)
    sample_file_path = os.getcwd() + '/' + DISCOGS_SAMPLE_FILE
    json_file = open(sample_file_path)
    sample_json = json.load(json_file)

completed_releases = []

for folder in folders:

    print(style.yellow('\n---\n'))

    print(style.green(folder))

    files = File(folder)
    try:
        discogs = Discogs(files, sample_json, completed_releases)
        
    except Exception as e:
        print(style.red('some error happened...'))
        logging.error(traceback.format_exc())
        continue

    if discogs == ENV_TAGGING_DONE:
        print(style.yellow(ENV_TAGGING_DONE))
        continue
    
    if discogs == ENV_TAGGING_TODO:
        print(style.yellow(ENV_TAGGING_TODO))
        continue

    if discogs == ENV_ALREADY_PROCESSED:
        print(style.yellow(ENV_ALREADY_PROCESSED))
        continue

    if discogs == None:
        print(style.yellow(ENV_ERROR_DISCOGS_NULL))
        continue


    discogs_id = discogs['discogs_id']
    if discogs_id not in completed_releases:
        Tagger(files, discogs, folder)
        completed_releases.append(discogs_id)
    else:
        print("already processed " + discogs_id)

print('\n')