CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: strings
strings: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f strings
