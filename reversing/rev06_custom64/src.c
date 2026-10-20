#include <stdio.h>
#include <string.h>
const char alphabet[]="/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA";
const char encoded[]="rK+0nIuZhJyKjIuQkqCdnoyaycugnpOPl56dmouC";
int main(void){char b[160];puts("Custom base64 password:");if(!fgets(b,sizeof b,stdin))return 1;b[strcspn(b,"\n")]=0;char tmp[256];int pos=0;unsigned acc=0;int bits=0;for(size_t i=0;i<strlen(b);i++){unsigned char ch=b[i];if(ch=='=')break;const char *q=strchr(alphabet,ch);if(!q){puts("wrong");return 0;}acc=(acc<<6)|(unsigned)(q-alphabet);bits+=6;if(bits>=8){bits-=8;tmp[pos++]=(char)((acc>>bits)&255);}}tmp[pos]=0;char verified[256];int k=0;acc=0;bits=0;const unsigned char *s=(const unsigned char*)tmp;for(int i=0;i<pos;i++){acc=(acc<<8)|s[i];bits+=8;while(bits>=6){bits-=6;verified[k++]=alphabet[(acc>>bits)&63];}}if(bits)verified[k++]=alphabet[(acc<<(6-bits))&63];while(k%4)verified[k++]='=';verified[k]=0;puts(strcmp(verified,encoded)==0?"correct":"wrong");return 0;}
