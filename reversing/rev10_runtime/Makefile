CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: runtime
runtime: src.c
	$(CC) $(CFLAGS) -o $@ $< -lz
clean:
	rm -f runtime
