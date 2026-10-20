#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){const char *m=getenv("MODE");if(m&&strcmp(m,"admin")==0)puts("SPKctf{branch_patch_success}");else puts("ACCESS DENIED");return 0;}
