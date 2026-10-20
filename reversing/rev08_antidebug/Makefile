CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: antidebug
antidebug: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f antidebug
