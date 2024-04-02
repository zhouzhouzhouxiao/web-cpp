#include <primes.h>
#include <iostream>
#include <cmath>

bool isPrime(int number) {
    if (number <= 1) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; i <= sqrt(number); i += 2) {
        if (number % i == 0) return false;
    }
    return true;
}

int main() {
    int sum = 0;
    for (int i = 2; i < 1000; ++i) {
        if (isPrime(i)) {
            sum += i;
        }
    }

    std::cout<< sum << std::endl;

    return 0;
}
