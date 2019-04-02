SRC_FILES=$(shell find . -maxdepth 1 -name '*.py')

lambda-package.zip: build.sh $(SRC_FILES)
	./build.sh

.PHONY: clean
clean:
	rm -f lambda-package.zip
