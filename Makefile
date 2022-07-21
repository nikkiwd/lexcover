updatedata:
	if python3 dump-download.py; then python3 dump-parse.py; fi
	python3 generate-statistics.py 
	python3 generate-missing-lists.py 

de:
	node update-wiki.js de

updatewiki:
	node update-wiki.js 

test:
	flake8
	mypy .

all: updatedata updatewiki
