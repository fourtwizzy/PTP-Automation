#!/usr/bin/python

import cgi
import requests
import shutil
import os
import datetime
import time

# Api user/key from security tab in profile
ApiUser = "<Api User String>"
ApiKey = "<Api Key String>"

# Directory to save the downloaded .torrent to
WatchDirectory = "/home/user1/rwatch"

# Limit the size of the container to this, the site will not send you more torrents
# Once your total container size exceeds this amount. This is a 'soft' limit, allowing one torrent to
# exceed this amount. The site accepts single letter suffix B, K, M, G, T and P
ContainerSize = "1T"

# Max 40 Character free form name. This is only used to define a container for the limit set above and will be used when
# sending you alerts regarding your container.
ContainerName = "PrometheusArchive005"

# The maximum number of partial/stalled torrents. 0 is infinite
MaxStalled = "0"

# Base url
BaseURL = "https://passthepopcorn.me/"


# End configuration

while(True):
    headers = {
        'ApiUser': ApiUser,
        'ApiKey': ApiKey
    }
    payload = {
        'ContainerName': ContainerName,
        'ContainerSize': ContainerSize,
        'MaxStalled': MaxStalled
    }

    now = datetime.datetime.now()
    print("Archive tool started: %s" % now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Fetching json data")
    r = requests.get(BaseURL + 'archive.php?action=fetch', headers=headers, params=payload)
    r.raise_for_status()
    data = r.json()

    print("Parsing")

    # print(r.text)

    if data['Status'] == 'Ok':
        if 'TorrentID' not in data:
            raise ValueError("TorrentID not in json data!")

        payload = {
            'id': data['TorrentID'],
            'ArchiveID': data['ArchiveID']
        }
        print("Fetching torrent file for https://passthepopcorn.me/torrents.php?id=%s&torrentid=%s" % (data['GroupID'], data['TorrentID']))
        r = requests.get(BaseURL + 'torrents.php?action=download', headers=headers, params=payload, stream=True)
        r.raise_for_status()

        params = cgi.parse_header(
            r.headers.get('Content-Disposition', ''))[-1]
        if 'filename' not in params:
            raise ValueError('Could not find a filename')

        filename = os.path.basename(params['filename'])
        abs_path = os.path.join(WatchDirectory, filename)
        with open(abs_path, 'wb') as target:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, target)

        print("Saved %s" % abs_path)

    elif data['Status'] == 'Error':
        raise ValueError("Error: %s" % data['Error'])

    else:
        raise ValueError("Unexpected json result!")

    now = datetime.datetime.now()
    print("Archive tool finished: %s" % now.strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    time.sleep(3)
