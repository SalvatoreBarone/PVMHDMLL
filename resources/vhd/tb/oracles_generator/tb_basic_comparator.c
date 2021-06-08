#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>

void print_binary(int amount, int num)
{
  assert(amount <= 32);
  for (int i = amount-1; i >= 0; i--)
    printf("%d", (num & (1<<i)) ? 1 : 0);
}

int main()
{
  srand(time(NULL));
  for (int i = 0; i < 10000; i++){
    unsigned data_1 = rand();
    unsigned data_2 = rand();
    print_binary(32, data_1);
    printf(" ");
    print_binary(32, data_2);
    printf(" %d %d %d\n", data_1 == data_2, data_1 < data_2, data_1 > data_2);
  }
}
