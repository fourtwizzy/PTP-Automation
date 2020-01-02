import os
import subprocess

def getIndex(item):
	return item.split(":")[0]

def getItem(list, index):
	for i in list:
		if getIndex(i) == str(index):
			return i
		
def getLanguage(item):
	return item.split(", ")[1].replace(" ", "")

def getAudio(root, source, choice, list, index):
	audio = []
	audio.append("eac3to " + source + " " + str(choice) + ") " + index + ":\"" + root.replace("\"", "") + "\\Audio\\" + getLanguage(getItem(list, index)) + "_Surround_576p.ac3\" -448")
	audio.append("eac3to " + source + " " + str(choice) + ") " + index + ":\"" + root.replace("\"", "") + "\\Audio\\" + getLanguage(getItem(list, index)) + "_Surround_720p_1080p.ac3\" -640")
	audio.append("eac3to " + source + " " + str(choice) + ") " + index + ":stdout.wav | qaac -V 127 -i --no-delay -o \"" + root.replace("\"", "") + "\\Audio\\" + getLanguage(getItem(list, index)) + "_Stereo_576p_720p.m4a\" -")
	audio.append("eac3to " + source + " " + str(choice) + ") " + index + ":\"" + root.replace("\"", "") + "\\Audio\\" + getLanguage(getItem(list, index)) + "_Stereo_1080p.flac\"")
	return audio
	
def getSubtitles(root, source, choice, list):
	subtitles = []
	for i in list:
		if "Subtitle" in i.split(", ")[0]:
			subtitles.append("eac3to " + source + " " + str(choice) + ") " + getIndex(i) + ":\"" + rootDir.replace("\"", "") + "\\Subtitles\\" + str(getIndex(i)) + "_" + getLanguage(i) + ".sup\"")
	return subtitles
	
def getChapters(root, source, choice, list):
	chapters = []
	for i in list:
		if "Chapters" in i.split(", ")[0]:
			chapters.append("eac3to " + source + " " + str(choice) + ") " + getIndex(i) + ":\"" + rootDir.replace("\"", "") + "\\Subtitles\\Chapters.txt\"")
	return chapters

rootDir = raw_input("Root Directory: ")
sourceDir = raw_input("Source Directory: ")

if not os.path.exists(rootDir.replace("\"", "") + "\\Audio\\"):
	os.makedirs(rootDir.replace("\"", "") + "\\Audio\\")

if not os.path.exists(rootDir.replace("\"", "") + "\\Subtitles\\"):
	os.makedirs(rootDir.replace("\"", "") + "\\Subtitles\\")

p = subprocess.Popen("eac3to " + sourceDir, stdout=subprocess.PIPE, shell=True)
output,err = p.communicate()
p.wait()
output = output.decode("UTF-8")
print(output)

playlist = raw_input("Playlist: ")

p = subprocess.Popen("eac3to " + sourceDir + " " + str(playlist) + ")", stdout=subprocess.PIPE, shell=True)
output,err = p.communicate()
p.wait()
output = output.decode("UTF-8")
print(output)
outputList = output.replace("\x08", "").split("\r\n")

audio = raw_input("Audio: ")

commands = []
commands += getAudio(rootDir, sourceDir, playlist, outputList, audio)
commands += getSubtitles(rootDir, sourceDir, playlist, outputList)
commands += getChapters(rootDir, sourceDir, playlist, outputList)

for command in commands:
	print("\n" + command)
	p = subprocess.Popen(command, shell=True)
	p.wait()

print("\nCleaning up ...")

for file in os.listdir(rootDir.replace("\"", "") + "\\Audio\\"):
	if "Log" in file:
		os.remove(rootDir.replace("\"", "") + "\\Audio\\" + file)

for file in os.listdir(rootDir.replace("\"", "") + "\\Subtitles\\"):
	if "Log" in file:
		os.remove(rootDir.replace("\"", "") + "\\Subtitles\\" + file)

print("\nDone!")