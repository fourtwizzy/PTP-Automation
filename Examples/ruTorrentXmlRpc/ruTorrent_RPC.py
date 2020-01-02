import xmlrpclib

url = "https://<Username>:<Password>@<XmlRpc Url>";
server = xmlrpclib.ServerProxy(url);

# Get torrents in the main view
# mainview = server.download_list("", "main")
# For each torrent in the main view
# for torrent in mainview:

    # # Print the name of torrent
    # print(server.d.get_name(torrent))
    # # Print the directory of torrent
    # print(server.d.get_directory(torrent))

# print(server.system.methodSignature("add_peer"));
# server.d.custom1.set("AD4206DB051CC11D3A78D3E4DC24E9DF9425DC41", "Test");
# print(server.system.methodHelp("load_start"));
	
# t = server.load_start("/home/user1/dwatch/Napszállta AKA Sunset.2018.1080p.Blu-ray.x264.MKV.729388.torrent");
# print(t);

# with open("/home/user1/scripts/TorrentLabels.json") as json_file:
	# data = json.load(json_file)
	# for d in data:
		# print("Hash: " + d["hash"] + " Label: " + d["category"] + "\n");
		# try:
			# server.d.custom1.set(d["hash"], d["category"]);
		# except:
			# pass;

# print(server.load_start_verbose("/home/user1/temp/test.torrent", "d.custom1.set=Test", "d.directory.set=/home/user/torrents/rtorrent/test/", "d.delete_tied="))