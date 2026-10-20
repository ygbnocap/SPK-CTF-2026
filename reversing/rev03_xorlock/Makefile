CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: xorlock
xorlock: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f xorlock
