import os.path
import urllib.request

import meta

filename = meta.local_dump_file

if not os.path.exists(filename):
	urllib.request.urlretrieve(meta.lexeme_dump_url, filename)
	print("Downloaded lexeme dump")
