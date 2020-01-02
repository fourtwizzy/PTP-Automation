import traceback
import requests
import json
import time
import datetime
from deluge_client import DelugeRPCClient

BaseURL = "https://passthepopcorn.me/"
ApiUser = "<Api User String>"
ApiKey = "<Api Key String>"
AuthKey = ""
PassKey = ""

DelugeIp = "<Deluge IP>"
DelugePort = <Deluge Port>
DelugeUser = "<Deluge Username>"
DelugePass = "<Deluge Password>"

headers = {
	"ApiUser": ApiUser,
	"ApiKey": ApiKey
}

payload = {
	"action": "advanced",
	"json": "noredirect",
	"freetorrent": "1",
	"page": 1
}

def logprint(data):
	print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + str(data))

while True:
	try:
		logprint("Querying")
		movies = []
		page = 1
		while True:
			payload["page"] = page
			r = requests.get(BaseURL + "torrents.php", headers=headers, params=payload)
			r.raise_for_status()
			data = r.json()
			if(len(data["Movies"])>0):
				movies += data["Movies"]
				page += 1
				time.sleep(1)
			else:
				AuthKey = data["AuthKey"]
				PassKey = data["PassKey"]
				break

		logprint("Downloading")
		with open('TorrentList.json', 'r') as f:
			currentTorrents = json.load(f)
		for movie in movies:
			for torrent in movie["Torrents"]:
				if(
					"FreeleechType" in torrent and
					torrent["FreeleechType"] == "Freeleech" and
					torrent["Checked"] and
					int(torrent["Seeders"])>0 and
					not str(torrent["Id"]) in currentTorrents
				):
					success = False
					while(not success):
						try:
							logprint("Adding: " + str(torrent["Id"]))
							url = BaseURL + "torrents.php?action=download&id=" + str(torrent["Id"]) + "&authkey=" + str(AuthKey) + "&torrent_pass=" + str(PassKey)
							logprint("URL: " + url)
							client = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
							client.connect()
							hash = client.core.add_torrent_url(url, [], [])
							logprint("Hash: " + str(hash))
							client.disconnect()
							currentTorrents[str(torrent["Id"])] = str(hash)
							success = True
						except Exception, e:
							logprint("Error adding torrent")
							logprint(e)
							time.sleep(5)
							
		logprint("Getting torrents from client")
		success = False
		torrentList = []
		while(not success):
			try:
				client = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
				client.connect()
				torrentList = client.core.get_session_state()
				client.disconnect()
				success = True
			except Exception, e:
				logprint("Error getting torrents from client")
				logprint(e)
				time.sleep(5)

		logprint("Removing deleted torrents from torrent list")
		for i in currentTorrents.keys():
			if(currentTorrents[i] not in torrentList):
				logprint("Removing: " + currentTorrents[i])
				del currentTorrents[i]
		
		logprint("Saving torrent list")
		with open('TorrentList.json', 'w') as f:
			json.dump(currentTorrents, f)
		
		time.sleep(1)
		
	except Exception, e:
		logprint("Error in main loop")
		logprint(e)
		time.sleep(60)