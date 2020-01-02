from deluge_client import DelugeRPCClient

DelugeIp = "<Deluge IP>"
DelugePort = <Deluge Port>
DelugeUser = "<Deluge Username>"
DelugePass = "<Deluge Password>"

client = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
client.connect()

mtvTorrents = client.core.get_torrents_status({}, ["progress"])
for i in mtvTorrents:
	if float(mtvTorrents[i]["progress"]) <= 94.0:
		print i
		client.core.remove_torrent(i, True)

client.disconnect()