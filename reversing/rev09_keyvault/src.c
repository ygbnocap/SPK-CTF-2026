#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc,char **argv){if(argc!=2){puts("Usage: ./keyvault <username>");return 1;}char cmd[400];char key[65];char name[128];if(strlen(argv[1])>100)return 1;snprintf(name,sizeof name,"%s",argv[1]);char tmp[140];snprintf(tmp,sizeof tmp,"printf %%s '%s' | sha256sum",name);FILE *fp=popen(tmp,"r");if(!fp)return 1;if(fscanf(fp,"%64s",key)!=1){pclose(fp);return 1;}pclose(fp);snprintf(cmd,sizeof cmd,"tail -c +17 encrypted_flag.bin | openssl enc -d -aes-256-cbc -K %s -iv 31415926535897932384626433832795 2>/dev/null",key);return system(cmd);}
