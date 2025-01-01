import meta

for language in meta.languages:
	filtered = meta.load_filter(language)
	forms = set()
	try:
		fh = open(meta.output_dir + "/" + "formlist-" + language + ".txt")
	except Exception:
		print("Couldn't read {}".format("formlist-" + language + ".txt"))
		continue
	for line in fh:
		form = line.strip().lower()
		form = form.replace(".", "")
		forms.add(form)

	tokencount = 0
	wordcount = 0
	coveredtokens = 0
	uncoveredtokens = 0
	coveredwords = 0
	uncoveredwords = 0
	try:
		fh = open(meta.output_dir + "/" + "wordlist-" + language + ".txt")
	except Exception:
		print("Couldn't read {}".format("wordlist-" + language + ".txt"))
		continue
	for line in fh:
		word, _, num = line.strip().rpartition(" ")
		count = int(num)
		tokencount += count
		wordcount += 1
		if word in forms or word in filtered:
			coveredwords += 1
			coveredtokens += count
		else:
			uncoveredwords += 1
			uncoveredtokens += count

	try:
		output = open(meta.output_dir + "/" + "stats-" + language + ".txt", "w")
	except Exception:
		print("Couldn't open {}".format("stats-" + language + ".txt"))
		continue

	if meta.data[language]["source"] == "unileipzig":
		output.write(
			"These statistics use corpus data from the "
			"[{} Leipzig Corpora Collection].\n"
			.format(meta.data[language]["infopage"])
		)

	output.write(
		"<table><tr><td>\n"
		"* Forms in Wikidata: {:,}\n"
		"* Forms in Wikipedia: {:,}\n"
		"* Tokens: {:,}\n"
		"* Covered forms: {:,} ({:.1%})\n"
		"* Missing forms:  {:,} ({:.1%})\n"
		"* Covered tokens: {:,} ({:.1%})\n"
		"* Missing tokens: {:,} ({:.1%})\n"
		"* [[Wikidata:Lexicographical coverage/{}/Missing"
		"|Most frequent missing forms]]\n"
		"</td><td>\n"
		"{{{{#invoke:Chart"
		"|pie chart"
		"|width=100"
		"|legend=Forms"
		"|slices=({}:Covered)({}:Missing)}}}}\n"
		"</td><td>"
		"{{{{#invoke:Chart"
		"|pie chart"
		"|width=100"
		"|legend=Tokens"
		"|slices=({}:Covered)({}:Missing)}}}}\n"
		"</td></td></table>\n"
		"\n"
		.format(
			len(forms),
			wordcount,
			tokencount,
			coveredwords,
			1.0 * coveredwords / wordcount,
			uncoveredwords,
			1.0 * uncoveredwords / wordcount,
			coveredtokens,
			1.0 * coveredtokens / tokencount,
			uncoveredtokens,
			1.0 * uncoveredtokens / tokencount,
			language,
			coveredwords,
			uncoveredwords,
			coveredtokens,
			uncoveredtokens
		)
	)

	output.close()
