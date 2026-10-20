#include <stdio.h>
#include <string.h>
enum {HALT=0,PUSH=1,XOR=2,CMP=3};
static const unsigned char expected[]={ 6,5,30,54,33,51,46,35,56,10,55,44,33,48,54,58,49,48,10,38,58,57,35,48,49,40 };
static const unsigned char bytecode[]={PUSH,0x55,XOR,CMP,HALT};
static int run(unsigned char input,unsigned char target){unsigned char st[8];int sp=0;unsigned char val=input;for(size_t pc=0;pc<sizeof bytecode;){switch(bytecode[pc++]){case PUSH:st[sp++]=bytecode[pc++];break;case XOR:val^=st[--sp];break;case CMP:return val==target;case HALT:return 0;default:return 0;}}return 0;}
int main(void){char s[128];if(!fgets(s,sizeof s,stdin))return 1;s[strcspn(s,"\n")]=0;if(strlen(s)!=sizeof expected){puts("wrong");return 0;}for(size_t i=0;i<sizeof expected;i++)if(!run((unsigned char)s[i],expected[i])){puts("wrong");return 0;}puts("correct");return 0;}
