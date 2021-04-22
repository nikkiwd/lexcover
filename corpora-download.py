import gzip
import os.path
import re
import tarfile
import urllib.request

import meta

# Download files
for language in meta.languages:
	local_file = meta.corpora_dir + "/" + meta.data[language]["remotefile"]

	if os.path.exists(local_file):
		continue

	remote_file = meta.data[language]["remoteurl"]
	urllib.request.urlretrieve(remote_file, local_file)

	print("Downloaded " + language)

# Convert Uni Leipzig files
for language in meta.languages:
	if meta.data[language]["source"] != "unileipzig":
		continue

	remote_file = meta.data[language]["remotefile"]
	local_file = meta.corpora_dir + "/" + remote_file
	new_local_file = meta.corpora_dir + "/" + language + ".txt.gz"

	if os.path.exists(new_local_file):
		continue

	filename = re.sub(r"^(.*)\.tar.gz$", r"\1/\1-sentences.txt", remote_file)

	with tarfile.open(local_file, "r:gz") as f_in:
		with gzip.open(new_local_file, "wb") as f_out:
			for line in f_in.extractfile(filename):
				f_out.write(line.split(b"\t")[1])

	print("Converted " + language)
