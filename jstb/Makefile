hide = @
OBJ = .obj

TESTS = \
	tests/empty.js \
	tests/expression.js \

LIBS = \
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

gen/parser.js: src/parser.peg Makefile
	@echo PEGJS $<
	@mkdir -p $(dir $@)
	$(hide) pegjs \
		-e TBParser \
		--allowed-start-rules program \
		--cache \
		$< $@

