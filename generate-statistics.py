import urllib.request

import meta

for language in meta.languages:
	filtered = meta.load_filter(language)
	forms = set()
	try:
		fh = open(meta.output_dir + "/" + "formlist-" + language + ".txt")
	except:
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
	except:
		print("Couldn't read {}".format("wordlist-" + language + ".txt"))
		continue
	for line in fh:
		word, _, count = line.strip().rpartition(" ")
		count = int(count)
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
	except:
		print("Couldn't open {}".format("stats-" + language + ".txt"))
		continue

	if meta.data[language]["source"] == "unileipzig":
		output.write("These statistics use corpus data from the [{} Leipzig Corpora Collection].\n".format(meta.data[language]["infopage"]))
	output.write("<table><tr><td>\n")
	output.write("* Forms in Wikidata: {:,}\n".format(len(forms)))
	output.write("* Forms in Wikipedia: {:,}\n".format(wordcount))
	output.write("* Tokens: {:,}\n".format(tokencount))
	output.write("* Covered forms: {:,} ({:.1%})\n".format(coveredwords, 1.0*coveredwords/wordcount))
	output.write("* Missing forms:  {:,} ({:.1%})\n".format(uncoveredwords, 1.0*uncoveredwords/wordcount))
	output.write("* Covered tokens: {:,} ({:.1%})\n".format(coveredtokens, 1.0*coveredtokens/tokencount))
	output.write("* Missing tokens: {:,} ({:.1%})\n".format(uncoveredtokens, 1.0*uncoveredtokens/tokencount))
	output.write("* [[Wikidata:Lexicographical coverage/{}/Missing|Most frequent missing forms]]\n".format(language))
	output.write("</td><td>\n")
	output.write("{{{{Graph:Chart|width=100|type=pie|legend=Forms|x=Covered,Missing|y1={},{}}}}}\n".format(
		coveredwords,
		uncoveredwords
	))
	output.write("</td><td>")
	output.write("{{{{Graph:Chart|width=100|type=pie|legend=Tokens|x=Covered,Missing|y1={},{}}}}}\n".format(
		coveredtokens,
		uncoveredtokens
	))
	output.write("</td></td></table>\n")
	output.write("\n")

	output.close()

