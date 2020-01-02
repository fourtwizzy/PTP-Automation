import socket
import ssl
import sys
import requests
from deluge_client import DelugeRPCClient

DelugeIp = "<Deluge IP>"
DelugePort = <Deluge Port>
DelugeUser = "<Deluge Username>"
DelugePass = "<Deluge Password>"

server = "irc.morethan.tv"
channel = "#announce"
botnick = "prometheusbot"
AuthKey = "<Auth Key>"
TorrentKey = "<Torrent Key>"

def downloadTorrent(url):
	url = url + "&authkey=" + AuthKey + "&torrent_pass=" + TorrentKey
	print("Downloading: " + url)
	client = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
	client.connect()
	hash = client.core.add_torrent_url(url, [], [])
	print("Hash: " + str(hash))
	client.disconnect()

print "Creating socket"
rawirc = socket.socket()

print "Enabling SSL"
irc = ssl.wrap_socket(rawirc)

print "Connecting to " + server
irc.connect((server, 6669))

print "Registering"
irc.send("USER " + botnick + " 0 * " + ":" + botnick + "\n")

print "Sending nick"
irc.send("NICK " + botnick + "\n")
			
try:
	count = 0
	while 1:
		text = irc.recv(8192)
		
		# if len(text) > 0:
			# print "****************************************************************************************************\n" + text
		# else:
			# continue

		if ("PING") in text:
			irc.send("PONG " + text.split()[1] + "\n")

		if ("255 " + botnick) in text:
			print "Connecting to channel"
			irc.send("JOIN " + channel + "\n")
		
		if ("JOIN :" + channel) in text:
			print "Joined channel"

		if ("PRIVMSG " + channel + " :") in text:
			data = text.split(" :")
			torrentinfo = data[1].split(" - ")
			print "\n"
			print torrentinfo[0]
			print torrentinfo[1]
			print torrentinfo[3]
			mediainfo = torrentinfo[1].split(" / ")
			if (
				mediainfo[2] == "HDTV" or mediainfo[2] == "Web-DL" or mediainfo[2] == "WEB"
			):
				torrenturls = torrentinfo[2].split(" / ")
				downloadTorrent(torrenturls[1])
				count+=1
				if(count>=100):
					sys.exit()
				
except KeyboardInterrupt:
	irc.send("QUIT :I have to go for now!\n")
	print "\n"
	sys.exit()
