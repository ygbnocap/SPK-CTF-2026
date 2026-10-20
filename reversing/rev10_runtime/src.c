#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <zlib.h>
static const char p0[]="SPKctf{";
static const char p1[]="runti";
static const char p2[]="me_fla";
static const char p3[]="g_asse";
static const char p4[]="mbly}";
int main(void){char b[128]={0};size_t o=0;const char *parts[]={p0,p1,p2,p3,p4};for(int i=0;i<5;i++){size_t k=strlen(parts[i]);memcpy(b+o,parts[i],k);o+=k;}unsigned long crc=crc32(0L,(const Bytef*)b,(uInt)o);if(crc==0x3d09921cUL)puts(b);else puts("CRC ERROR");return 0;}
