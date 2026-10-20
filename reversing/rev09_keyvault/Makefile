CC=gcc
CFLAGS=-O0 -Wall -Wextra -no-pie
all: keyvault
keyvault: src.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm -f keyvault
