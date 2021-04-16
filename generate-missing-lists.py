import meta

for language in meta.languages:
	top = 1000
	forms = set()
	try:
		fh = open(meta.output_dir + "/" + "formlist-" + language + ".txt")
	except:
		print("Couldn't open {}".format("formlist-" + language + ".txt"))
		continue
	for line in fh:
		forms.add(line.strip().lower())

	try:
		output = open(meta.output_dir + "/" + "missing-" + language + ".txt", "w")
	except:
		print("Couldn't open {}".format("missing-" + language + ".txt"))
		continue

	filtered = meta.load_filter(language)

	try:
		fh = open(meta.output_dir + "/" + "wordlist-" + language + ".txt")
	except:
		print("Couldn't open {}".format("wordlist-" + language + ".txt"))
		continue
	for line in fh:
		word, _, count = line.strip().rpartition(" ")
		word = word.lower()

		count = int(count)
		if word in forms or word in filtered:
			pass
		else:
			top -= 1
			if top < 0:
				break
			output.write("# {} ({:,})\n".format(word, count))
	
	output.close()

