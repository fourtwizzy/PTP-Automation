import random
import socket
import ssl
import os
import sys
import requests
import shutil
import cgi

server = "irc.passthepopcorn.me"
user = "<username>"
key = "<irc key>"
channel = "#ptp-announce"
botnick = "prometheusbot"
watchdirectory = "/home/user1/dwatch"
headers = {
	"ApiUser": "<Api User String>",
	"ApiKey": "<Api Key String>"
}

def downloadTorrent(url):
	print("Fetching torrent file for %s", url)
	r = requests.get(url, headers=headers, stream=True)
	r.raise_for_status()

	params = cgi.parse_header(
		r.headers.get('Content-Disposition', ''))[-1]
	if 'filename' not in params:
		raise ValueError('Could not find a filename')

	filename = os.path.basename(params['filename'])
	abs_path = os.path.join(watchdirectory, filename)
	with open(abs_path, 'wb') as target:
		r.raw.decode_content = True
		shutil.copyfileobj(r.raw, target)

	print("Saved %s" % abs_path)

print "Creating socket"
rawirc = socket.socket()

print "Enabling SSL"
irc = ssl.wrap_socket(rawirc)

print "Connecting to " + server
irc.connect((server, 7000))

print "Registering"
irc.send("USER " + botnick + " 0 * " + ":" + botnick + "\n")

print "Sending nick"
irc.send("NICK " + botnick + "\n")
			
try:
	while 1:
		text = irc.recv(8192)
		
##		if len(text) > 0:
##			print "\n" + repr(text)
##		else:
##			continue

		if ("PING") in text:
			irc.send("PONG " + text.split()[1] + "\n")

		if ("255 " + botnick) in text:
			print "Connecting to channel"
			irc.send("PRIVMSG Hummingbird ENTER " + user + " " + key + " " + channel + "\n")
		
		if ("JOIN :" + channel) in text:
			print "Joined channel"

		if ("PRIVMSG #ptp-announce :") in text:
			data = text.split(" :")
			torrentinfo = data[1].split(" - ")
			print "\n"
			print torrentinfo[0]
			print torrentinfo[1]
			print torrentinfo[3]
			mediainfo = torrentinfo[1].split(" / ")
			if (
			   mediainfo[0] == "x264" and
			   mediainfo[1] == "Blu-ray" and
			   mediainfo[2] == "MKV" and
			   (mediainfo[3] == "720p" or mediainfo[3] == "1080p")
			):
				print "Download"
				torrenturls = torrentinfo[2].split(" / ")
				downloadTorrent(torrenturls[1])
				sys.exit()
				
except KeyboardInterrupt:
	irc.send("QUIT :I have to go for now!\n")
	print "\n"
	sys.exit()
