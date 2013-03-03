all: db/minimal.db

MOOFILES = \
	$(shell find src/*/ -name '*.moo' | LC_ALL=C sort)
	
ALLFILES = \
	src/_first.moo \
	src/_classes.moo \
	$(MOOFILES) \
	src/_last.moo
	
PATCHFILES = \
	src/_classes.moo \
	$(MOOFILES)
	
new: db/minimal.db

patch::
	expect src/bootstrap.expect -- current.db $(PATCHFILES)

db/minimal.db: db/Stunt.db src/bootstrap.expect $(ALLFILES) \
		files/primitive-0.0.4.json
	cp db/Stunt.db db/minimal.db
	expect src/bootstrap.expect -- db/minimal.db $(ALLFILES)

db/Stunt.db:
	mkdir -p db
	if [ ! -f $@ ]; then wget -O $@ http://stunt.io/Stunt.db; fi

files/primitive-0.0.4.json:
	mkdir -p files
	if [ ! -f $@ ]; then wget -O $@ http://stunt.io/packages/primitive/0.0.4.json; fi
