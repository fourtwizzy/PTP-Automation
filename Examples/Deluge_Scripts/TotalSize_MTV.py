from deluge_client import DelugeRPCClient

DelugeIp = "<Deluge IP>"
DelugePort = <Deluge Port>
DelugeUser = "<Deluge Username>"
DelugePass = "<Deluge Password>"

client = DelugeRPCClient(DelugeIp, DelugePort, DelugeUser, DelugePass)
client.connect()

mtvTorrents = client.core.get_torrents_status({"tracker_host": "morethantv.net"}, ["total_wanted"])
mtvTotalSize = 0
for i in mtvTorrents:
	mtvTotalSize += int(mtvTorrents[i]["total_wanted"])
mtvTotalSize = mtvTotalSize / 1024 / 1024 / 1024
print("MTV:   " + str(mtvTotalSize))

ptpTorrents = client.core.get_torrents_status({"tracker_host": "passthepopcorn.me"}, ["total_wanted"])
ptpTotalSize = 0
for i in ptpTorrents:
	ptpTotalSize += int(ptpTorrents[i]["total_wanted"])
ptpTotalSize = ptpTotalSize / 1024 / 1024 / 1024
print("PTP:   " + str(ptpTotalSize))

torrents = client.core.get_torrents_status({}, ["total_wanted"])
totalSize = 0
for i in torrents:
	totalSize += int(torrents[i]["total_wanted"])
totalSize = totalSize / 1024 / 1024 / 1024
print("Total: " + str(totalSize))

client.disconnect()