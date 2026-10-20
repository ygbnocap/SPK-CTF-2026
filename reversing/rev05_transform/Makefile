CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: transform
transform: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f transform
