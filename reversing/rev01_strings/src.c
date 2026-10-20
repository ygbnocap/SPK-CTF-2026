#include <stdio.h>
static const char secret[]="SPKctf{hardcoded_credentials}";
int main(void){puts("Search the binary, not the screen.");if(secret[0]==0)puts(secret);return 0;}
