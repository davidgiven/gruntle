all: db/minimal.db

MOOFILES = \
	src/_init.moo
	
db/minimal.db: db/Stunt.db src/bootstrap.expect $(MOOFILES) \
		files/primitive-0.0.4.json
	expect src/bootstrap.expect -- $(MOOFILES)

db/Stunt.db:
	if [ ! -f $@ ]; then wget -O $@ http://stunt.io/Stunt.db; fi

files/primitive-0.0.4.json:
	if [ ! -f $@ ]; then wget -O $@ http://stunt.io/packages/primitive/0.0.4.json; fi
