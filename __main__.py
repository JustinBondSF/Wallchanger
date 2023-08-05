import requests
import os
import json
import urllib.request
from io import BytesIO
from PIL import Image, ImageFile
import PySimpleGUI as sg
import shutil
import glob
from pathlib import Path

API_KEY = '?apikey=QEo7gl7TqgwLhqn5xvsalbKkGt1cbiBu'

layout = [
    [sg.Text('Enter search terms for Wallpapers:')],
    [sg.Input(key='-QUERY-')],

    [sg.Text('Categories:'),
     sg.Checkbox('General', key='General', default=True),
     sg.Checkbox('Anime', key='Anime'),
     sg.Checkbox('People', key='People', default=True)],

    [sg.Text('Purity:'),
     sg.Checkbox('SFW', key='SFW', default=True),
     sg.Checkbox('Sketchy', key='SKETCHY', default=True),
     sg.Checkbox('NSFW', key='NSFW', default=True)],

    [sg.Text('Atleast Resolution:'),
     sg.Combo([f'{i}x{int(9 / 16 * i)}' for i in (720, 900, 1080)], default_value='1280x720', key='-RES-')],

    [sg.Text('Order:'),
     sg.Radio('Ascending', 'RADIO1', key='-ASC-', default=True),
     sg.Radio('Descending', 'RADIO1', key='-DESC-')],

    [sg.Text('Sorting:'),
     sg.Combo(['Toplist', 'Date Added', 'Views', 'Favorites', 'Relevance', 'Random'], default_value='Toplist', key='-SORT-')],

    [sg.Button('Search'), sg.Button('Exit')],

    [sg.ProgressBar(26, orientation='h', size=(30,  10), key='-PROG-')],
    [sg.Image(key='-IMG-', source='')]
]

# Create PySimpleGUI window object


def build_api_url(values):
    api_base_url = 'https://wallhaven.cc/api/v1'
    tags = values['-QUERY-']
    categories = f'{int(values["General"])}{int(values["Anime"])}{int(values["People"])}'
    purity = f'{int(values["SFW"])}{int(values["SKETCHY"])}{int(values["NSFW"])}'
    resolution = values['-RES-']
    sorting = values['-SORT-']
    if values['-SORT-'] == ['-TOP-']:
        sorting = 'toplist'
    elif values['-SORT-'] == ['-DATE-']:
        sorting = 'date_added'
    elif values['-SORT-'] == ['-VIEWS-']:
        sorting = 'views'
    elif values['-SORT-'] == ['-FAV-']:
        sorting = 'favorites'
    elif values['-SORT-'] == ['-REL-']:
        sorting = 'relevance'
    elif values['-SORT-'] == ['-RAND-']:
        sorting = 'random'
    order = 'asc' if values['-ASC-'] else 'desc' if values['-DESC-'] else ''

    api_url = f"{api_base_url}/search{API_KEY}&q={tags}&categories={categories}&purity={purity}&atleast={resolution}&sorting={sorting}&order={order}"
    print(api_url)
    return api_url


def download_wallpapers(url: str) -> None:
    response = requests.get(url)
    wallpapers_json = json.loads(response.content)
    wallpapers = [item['path'] for item in wallpapers_json['data']]
    tags = values['-QUERY-']
    wall_dir = Path('/Users/bond/.local/share/wallpapers/')
    num_of_images = len(wallpapers)

    for filename in os.listdir(wall_dir):
        file_path = os.path.join(wall_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    if not os.path.exists(wall_dir):
        os.makedirs(wall_dir)

    for wallpaper in wallpapers:

        try:
            filename = os.path.join(
                wall_dir, f"{tags}_{wallpaper.split('/')[-1]}")
            with open(filename, 'wb') as file:
                url = wallpaper
                r = requests.get(url, stream=True)

                file.write(r.content)
                print(f'Downloaded {filename}')

        except Exception as e:
            print(f'Caught exception while trying to save {wallpaper}: {e}')


def update_progress_bar():
    prog_bar = window.Element('-PROG-')
    i = 0
    num_of_images = len(wallpapers)
    for i in range(num_of_images):
        # display images while downloading
        try:
            prog_bar.update(i + 1, num_of_images)
            if i == num_of_images - 1:
                prog_bar.update(num_of_images)

            window.refresh()
        except Exception as e:
            print(f'Caught exception while trying to update progress bar: {e}')

    # Increment progress bar by 4% for each downloaded wallpaper
    prog_bar.update(i+1)


window = sg.Window('Wallpaper Downloader', layout)

while True:

    event, values = window.read()
    print(event, values)

    if event in (None, 'Exit'):
        break
    elif event == 'Search':
        query = values['-QUERY-']
        url = build_api_url(values)
        WallDir = os.path.expanduser('~/.local/share/wallpapers/')
        # Prepare the directory for downloaded wallpapers
        if not os.path.exists(WallDir):
            os.mkdir(WallDir)
        else:
            # Clear out any existing images in the folder before downloading new ones
            for f in os.listdir(WallDir):
                try:
                    os.remove(os.path.join(WallDir, f))
                except Exception as e:
                    if f is os.path.isdir(f) is True:
                        os.remove(os.path.join(WallDir, f))

        # Start downloading wallpapersog_bar = window.Element('-PROG-')

        download_wallpapers(url)
        update_progress_bar()

    # End while-loop here, button click events captured above.

window.close()
