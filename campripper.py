import urllib2
import re
import json
import os
import wget
import sys

def get_metadata(album_url):
	response = urllib2.urlopen(album_url) 
	html = response.read();

	album_title = re.search(r'album_title : "(.+)"', html).group(1)
	artist = re.search(r'artist : "(.+)",', html).group(1)
	track_info = re.search(r'trackinfo : (.+),', html).group(1)

	tracks = json.loads(track_info)

	queue = {}

	for track in tracks:
		title = track['title']
		url = track['file']['mp3-128']
		queue[title] = url

	return(artist, album_title, queue)

def get_tracks(queue, output_path):
	for title,url in queue.items():
		path = os.path.join(output_path, title + ".mp3")
		print("\nDownloading: " + path)
		wget.download(url, out=os.path.join(output_path, title + ".mp3"))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.exit("Usage: campripper.py <album_url>")

	artist,album_title,queue = get_metadata(sys.argv[1])

	print(artist + " - " + album_title)
	for i in range(0, len(queue)):
		print str(i + 1) + ". " + queue.keys()[i]


	album_path = os.path.join(artist, album_title);

	if not os.path.exists(album_path):
		os.makedirs(album_path)

	get_tracks(queue, album_path)