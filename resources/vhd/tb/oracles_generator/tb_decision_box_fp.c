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

typedef union {
  float f;
  unsigned u;
} ufloat;

int main()
{
  srand(time(NULL));
  for (int i = 0; i < 10000; i++){
    ufloat data_1;
    ufloat data_2;
    data_1.f = rand() / rand();
    data_2.f = rand() / rand();
    print_binary(32, data_1.u);
    printf(" ");
    print_binary(32, data_2.u);
    printf(" %d %d %d\n", data_1.f == data_2.f, data_1.f < data_2.f, data_1.f > data_2.f);
  }
}
