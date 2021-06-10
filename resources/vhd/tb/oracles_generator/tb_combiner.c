#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void print_binary(int amount, int num)
{
  assert(amount <= 32);
  for (int i = amount-1; i >= 0; i--)
    printf("%d", (num & (1<<i)) ? 1 : 0);
}

int main ()
{
	for (unsigned i = 0; i < (1<<16); i++)
	{
		unsigned number = i, one_count = 0;
		for (unsigned j = 0; j < 16; j++)
			one_count += 1U & (number >> j);		
    print_binary(16, number);
		printf(" %d\n", one_count >= 8);
	}
	return 0;
}