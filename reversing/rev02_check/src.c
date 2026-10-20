#include <stdio.h>
#include <string.h>
int main(void){char b[160];puts("Password:");if(!fgets(b,sizeof b,stdin))return 1;b[strcspn(b,"\n")]=0;if(strcmp(b,"SPKctf{simple_input_check}")==0)puts("correct");else puts("wrong");return 0;}
