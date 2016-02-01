hide = @
OBJ = .obj

TESTS = \
	tests/empty.js

LIBS = \
	lib/peg-0.9.0.min.js \
	gen/parser.js \
	src/thickbasic.js \
	src/thickbasic-node.js \

.PHONY: all
all: tests

.PHONY: tests
tests: $(patsubst %.js,$(OBJ)/%.test,$(TESTS))

$(OBJ)/%.test: %.js $(LIBS)
	@echo TEST $<
	@mkdir -p $(dir $@)
	$(hide) nodejs $<
	$(hide) touch $@

gen/parser.js: src/parser.peg
	@echo PEGJS $<
	@mkdir -p $(dir $@)
	$(hide) pegjs -e TBParser --track-line-and-column $< $@

