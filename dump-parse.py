import gzip
import json
import sys

import meta

count = 0

outputs = {}
for language in meta.languages:
	filename = meta.output_dir + "/" + "formlist-" + language + ".txt"
	outputs[language] = open(filename, "w")

errorcount = 0
dictcount = 0

try:
	fh = gzip.open(meta.local_dump_file)
except:
	print("Couldn't read {}".format(meta.local_dump_file))
	sys.exit(1)

for line in fh:
	count += 1
	line = line.decode("utf-8").strip()

	# Not long enough to contain lexeme data
	if len(line) < 2:
		continue

	# Remove trailing comma
	if line[-1] == ",":
		line = line[:-1]

	lexeme = json.loads(line)

	if (lexeme["language"] in meta.mapq) and (meta.mapq[lexeme["language"]] in meta.languages):
		dictcount += 1
		for form in lexeme["forms"]:
			try:
				for lcode in form["representations"]:
					outputs[meta.mapq[lexeme["language"]]].write(form["representations"][lcode]["value"] + "\n")
			except:
				errorcount += 1
				print(errorcount)
				print(lexeme["id"])
				print(lexeme["lemmas"])
				print("")

for language in meta.languages:
	outputs[language].close()

print("{:,} Lexemes total, {:,} used".format(count, dictcount))
