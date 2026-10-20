CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: check
check: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f check
