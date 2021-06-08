import requests
import os
import json
import urllib.request

# Get wallpapers via API, save it to a json object

r=requests.get('https://wallhaven.cc/api/v1/search?apikey=QEo7gl7TqgwLhqn5xvsalbKkGt1cbiBu&q=psychedelic&categories=111&purity=111&atleast=1280x720&sorting=random&order=desc')

wallpapersJSON = json.loads(r.content)
WallDir = '/home/bond/.local/share/wallpapers'
i=0
wallpapers=[]
for url in wallpapersJSON['data']:
    for path in url:
        if 'path' in path:
            wallpapers.append(url['path'])



# Take the list of urls from "wallpapers" and loop through, saving each one to "a new file, replacing the old one if it already exists"
if r.status_code==200:
    os.chdir(WallDir)
    for wallpaper in wallpapers:

        os.chdir(WallDir)
        filename = WallDir + '/wallpaper #' + str(i)

        print(filename)
        r = requests.get(wallpaper)
        wallpaperfile = open(filename,"w+b")
        wallpaperfile.write(r.content)
        wallpaperfile.close()

        i+=1

    else:
        pass


