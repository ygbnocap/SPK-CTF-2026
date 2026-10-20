CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: custom64
custom64: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f custom64
