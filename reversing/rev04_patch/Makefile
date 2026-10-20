CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: patch
patch: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f patch
