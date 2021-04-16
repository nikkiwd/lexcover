import gzip
import json

import meta

for language in meta.languages:
	wordlist = {}
	print("Reading " + language)
		
	errorcount = 0
	tokencount = 0
	
	corpusfile = meta.corpora_dir + "/" + language + ".txt.gz"
	linecount = 0
	first = True

	try:
		fh = gzip.open(corpusfile, "r")
	except:
		print("Can't read {}".format(corpusfile))
		continue

	for line in fh:
		linecount += 1
		if linecount % 100000 == 0:
			print("{:,} articles processed".format(linecount))
		for c in [
				b".", b",", b"_", b"(", b")", b"=", b"\"",
				b"\xe2\x80\x9e", b"\xe2\x80\x9f", b"\xe0\xa5\xa4", b"\xe0\xa5\xa5"
		]:
			line = line.replace(c, b" ")
		words = line.split()
		for word in words:
			tokencount += 1
			try:
				word = word.decode("utf-8")
			except UnicodeDecodeError as e:
				errorcount += 1
				continue
			if word in ["", "NEWLINE"]:
				continue
			if word.isdigit():
				continue
			word = word.lower()
			if word not in wordlist:
				wordlist[word] = 0
			wordlist[word] += 1
	
	output = open(meta.output_dir + "/wordlist-" + language + ".txt", "w")
	
	tencount = 0
	tentokencount = 0
	for l in sorted(wordlist.items(), reverse=True, key=lambda x: x[1]):
		if l[1] > 10:
			tencount += 1
			tentokencount += l[1]
			output.write(l[0] + " " + str(l[1]) + "\n")
	output.close()
	
	with open(meta.output_dir + "/meta-" + language + ".txt", "w") as output:
		json.dump({
			"corpus": meta.data[language]["source"],
			"numberOfFormsInWiki": len(wordlist),
			"numberOfFormsInWikiTen": tencount,
			"numberOfTokens": tokencount,
			"numberOfTokensTen": tentokencount,
			"unicodeErrors": errorcount
		}, output, indent=4)
	print("Read {} with {:,} different word forms, {:,} with 10+ in {:,} words ({:,} errors)".format(language, len(wordlist), tencount, tokencount, errorcount))

