0:
	mkzero-gfxmonk -v `cat VERSION` -p autonose -p setup.py autonose.xml

tasks:
	echo "\n\n`egrep -o '^[[:alnum:]]+' Makefile`"

clean:
	find . -iname '*.pyc' -or -iname '.*.pickle' | xargs rm

autonose-local.xml: autonose.xml
	0local autonose.xml

test: autonose-local.xml
	0test autonose-local.xml

.PHONY: test
