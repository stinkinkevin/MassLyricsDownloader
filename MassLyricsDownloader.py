import argparse
import codecs
import json
import bs4
import sys
from bs4 import BeautifulSoup
import urllib, urllib2


ACTIONS_DELIMITER = ","



def Extraction(webpage):
	soup = bs4.BeautifulSoup(webpage)
	result = []
	for tag in soup.find('div', 'lyricbox'):
		if isinstance(tag, bs4.NavigableString):
			if not isinstance(tag, bs4.element.Comment):
				result.append(tag)
		elif tag.name == 'br':
			result.append('\n')
	return "".join(result)


def Import(file):
	f = open(file, 'r')
	count = 0
	for line in f:
		data = line.rstrip('\n').split(ACTIONS_DELIMITER)
		ID = data[0]
		ArtistInput = data[2]
		SongInput = data[1]
		print("%s, %s, %s" % (ID, ArtistInput, SongInput))
		Query = urllib.urlencode(dict(artist=ArtistInput, song=SongInput, fmt="realjson"))
		Response = urllib2.urlopen("http://lyrics.wikia.com/api.php?" + Query)
		Output = json.load(Response)

		if (Output['lyrics'] != 'Not found'):
			Lyrics = Extraction(urllib2.urlopen(Output['url']))
			print (Output['lyrics'])
			OutputPath = ("/home/kev/fuck/%s.txt" % (ID))
			with codecs.open(OutputPath, 'w', encoding='utf-8') as output_file:
				output_file.write(Lyrics)
			print("Finished writing '%s'" % OutputPath)
		else:
			print("Lyrics not found")
		count += 1
	f.close()
	print "%s lyrics are imported." %count


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Import lyrics")
	parser.add_argument('--file', default="dataset.csv")
	
	args = parser.parse_args()
	print args

	Import(args.file)
