import calendar
import os.path
import sys
import time
import urllib.request

import meta

filename = meta.local_dump_file

if os.path.exists(filename):
	# Get last modified time of remote file
	req = urllib.request.Request(meta.lexeme_dump_url, method="HEAD")
	res = urllib.request.urlopen(req)
	moddate = res.headers["Last-Modified"]
	remote = calendar.timegm(time.strptime(moddate, "%a, %d %b %Y %H:%M:%S %Z"))

	# Get last modified time of local file
	local = os.path.getmtime(filename)

	# No new dump available
	if local >= remote:
		sys.exit(0)

	print("Remote dump file is newer than local dump file")
else:
	print("Local dump file not found")

print("Downloading dump file...")
urllib.request.urlretrieve(meta.lexeme_dump_url, filename)
print("Downloaded lexeme dump")
