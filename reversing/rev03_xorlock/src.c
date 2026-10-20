#include <stdio.h>
#include <string.h>
static const unsigned char enc[]={ 17,18,9,33,54,36,57,58,45,48,29,39,44,33,45,38,39,38,29,33,45,47,50,35,48,39,63 };
int main(void){char s[128];if(!fgets(s,sizeof s,stdin))return 1;s[strcspn(s,"\n")]=0;if(strlen(s)!=sizeof enc){puts("wrong");return 0;}for(size_t i=0;i<sizeof enc;i++)if(((unsigned char)s[i]^0x42)!=enc[i]){puts("wrong");return 0;}puts("correct");return 0;}
