import json
import os
import sys
import urllib.request

with open("language-data.json") as f:
	data = json.load(f)
	f.close()

corpora_dir = "corpora"
wdexport_dir = "dump"
output_dir = "output"

for directory in [corpora_dir, wdexport_dir, output_dir]:
	if not os.path.exists(directory):
		os.mkdir(directory)

lexeme_dump_file = "latest-lexemes.json.gz"
lexeme_dump_url = "https://dumps.wikimedia.org/wikidatawiki/entities/" \
	+ lexeme_dump_file
local_dump_file = wdexport_dir + "/" + lexeme_dump_file

mapq = {}
qmap = {}

for language in data:
	assert "source" in data[language]
	source = data[language]["source"]

	if source == "wiki40b":
		if "remotefile" not in data[language]:
			data[language]["remotefile"] = language + ".txt.gz"
		data[language]["remoteurl"] = \
			"https://download.wmcloud.org/corpora/" + data[language]["remotefile"]

	elif source == "unileipzig":
		# TODO: Find out if this hostname is stable
		data[language]["remoteurl"] = \
			"https://pcai056.informatik.uni-leipzig.de/downloads/corpora/" \
			+ data[language]["remotefile"]

	else:
		print("ERROR: Unrecognised source for " + language + ": " + source)

	qmap[language] = data[language]["qid"]
	mapq[data[language]["qid"]] = language

	if len(sys.argv) > 1:
		languages = sys.argv[1:]
	else:
		languages = list(data.keys())


def load_filter(language):
	try:
		url = "https://www.wikidata.org/wiki/Wikidata:Lexicographical_coverage/" \
			+ language + "/Filter?action=raw"
		page = urllib.request.urlopen(url)
		text = page.read().decode("utf-8")
		lines = text.split("\n")
		filtered = set()
		for line in lines:
			if not (line.startswith("*") or line.startswith("#")):
				continue
			word = line[1:].strip().lower()
			filtered.add(word)
		return filtered
	except Exception:
		return []
