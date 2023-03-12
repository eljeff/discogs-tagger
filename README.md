# <img width=25 src="https://www.discogs.com/images/brand/discogs-logo.svg"> Discogs to ID3 tagger

Heavily modified version of https://github.com/bamdadsabbagh/tagger to work with my own tagging style.
- Looks for a tag 'DISCOGS_RELEASE_ID' to pull an exact release from discogs
- Overwrites / clobbers all tags on a file
- Writes sort artist as album artist
- Converts 'Various' album artist to 'Compilations'
- Does not write album artist tag if all track artists match the sort_artist
- Tries to intelligently write tracknumber, total tracks, vinyl tracks, disc number, total discs
- Skips re-running subfolder if release already processed via super-folder parsing (need to look into this)
- Includes sample discogs api output for further inspection

<p align=center>
  <a href="https://github.com/eljeff/discogs-tagger"><img width=150 src="https://www.discogs.com/images/brand/discogs-logo.svg"></a>
</p>

<p align=center>
  Get data from Discogs API and automatically tag audio files
</p>

## Dependencies

- python3
- python3-pip
- python3-venv

## How to install

```bash
git clone git@github.com:eljeff/discogs-tagger.git
cd tagger
./bin-install.sh
```

## Configuration file

change `ENV_PATHS` in `src/env.py` to the directory containing files you'd like to tag.
Files are expected to be in folders per album.

## Run

```bash
./bin-run.sh
```
