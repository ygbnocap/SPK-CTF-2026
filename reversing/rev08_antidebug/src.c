#include <stdio.h>
#include <sys/ptrace.h>
#include <errno.h>
int main(void){errno=0;if(ptrace(PTRACE_TRACEME,0,0,0)==-1)puts("SPKctf{fake_debugger_detected}");else puts("SPKctf{antidebug_bypassed}");return 0;}
