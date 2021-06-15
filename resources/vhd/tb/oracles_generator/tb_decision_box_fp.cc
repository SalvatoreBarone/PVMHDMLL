#include <iostream>
#include <bitset>
#include <limits>
#include <random>
#include <cassert>

void print_binary_64(std::ostream& stream, void * const data)
{
  unsigned long * udata = (unsigned long *)data;
  stream << std::bitset<64>(*udata);
}

int main()
{
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> distrib;

  for (int i = 0; i < 10000; i++){
    double data_1;
    double data_2;
    data_1 = distrib(gen);
    data_2 = distrib(gen);
    print_binary_64(std::cout, &data_1);
    std::cout << " ";
    print_binary_64(std::cout, &data_2);
    std::cout << " " << (data_1 == data_2) << " " << (data_1 < data_2) << " " << (data_1 > data_2) << std::endl;
  }
}
