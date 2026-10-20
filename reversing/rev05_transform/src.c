#include <stdio.h>
#include <string.h>
static const unsigned char enc[]={ 0,247,232,48,99,57,120,93,54,105,54,93,96,54,36,99,93,42,81,96,57,84,93,78,36,75,84,60,66,48,126 };
int main(void){char s[128];if(!fgets(s,sizeof s,stdin))return 1;s[strcspn(s,"\n")]=0;if(strlen(s)!=sizeof enc){puts("wrong");return 0;}for(size_t i=0;i<sizeof enc;i++)if((((unsigned char)s[i]*3+7)&255)!=enc[i]){puts("wrong");return 0;}puts("correct");return 0;}
