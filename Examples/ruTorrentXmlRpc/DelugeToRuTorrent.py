import os
import shutil
import xmlrpclib
from deluge_client import DelugeRPCClient

DelugeIp = "<Deluge IP>"
DelugePort = <Deluge Port>
DelugeUser = "<Deluge Username>"
DelugePass = "<Deluge Password>"
DelugeStatePath = "/home/user1/.config/deluge/state/"
rTorrentUrl = "https://<Username>:<Password>@<XmlRpc Url>
TorrentLabel = "Archive/MoreThanTV"
TorrentPath = "/home/user1/torrents/rtorrent/archive/morethantv/"
TempPath = "/home/user1/scripts/ruTorrentXmlRpc/temp/"

if not os.path.exists(TempPath):
	os.makedirs(TempPath)

dClient = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
dClient.connect()
rClient = xmlrpclib.ServerProxy(rTorrentUrl);

torrents = dClient.core.get_torrents_status({"tracker_host": "morethantv.net"}, [])
for t in torrents:
	print([t])
	dClient.core.move_storage([t], TorrentPath)
	shutil.copyfile(DelugeStatePath + str(t) + ".torrent", TempPath + str(t) + ".torrent") 
	dClient.core.remove_torrent(t, False)
	rClient.load_start_verbose(TempPath + str(t) + ".torrent", "d.custom1.set=" + TorrentLabel, "d.directory.set=" + TorrentPath, "d.delete_tied=")

dClient.disconnect()
