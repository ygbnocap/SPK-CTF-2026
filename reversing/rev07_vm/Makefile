CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: vm
vm: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f vm
