.PHONY: clean prepare tests

all: prepare tests clean

prepare:
	cp "test/example.conf" "/tmp/example.conf"

tests:
		./test/bats/bin/bats test/tests.bats

clean:
		-rm -f /tmp/example.conf
