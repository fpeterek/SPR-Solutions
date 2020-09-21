// https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=12&page=show_problem&problem=954

#include <iostream>
#include <string>
#include <cstdint>
#include <vector>


void ignore_line() {
    std::string line;
    std::getline(std::cin, line);
}

void check_carry(std::vector<uint8_t> & num, size_t start) {

    while (num[start] > 9) {

        uint8_t carry = num[start] / 10;
        num[start] %= 10;
        num[--start] += carry;

    }

}

void handle() {

    size_t size;
    std::cin >> size;

    std::vector<uint8_t> res(size);

    for (size_t i = 0; i < size; ++i) {
        uint32_t b1, b2;
        std::cin >> b1 >> b2;
        uint32_t sum = b1 + b2;
        res[i] = sum;
        check_carry(res, i);
    }

    for (size_t i = 0; i < size; ++i) {
        std::cout << (int32_t)res[i];
    }

    std::cout << "\n";

}

int main(int argc, const char * argv[]) {

    std::cout.sync_with_stdio(false);

    uint32_t blocks;
    std::cin >> blocks;
    ignore_line();

    for (uint32_t i = 0; i < blocks; ++i) {
        handle();
        if (i != blocks-1) {
            std::cout << "\n";
        }
    }

    std::flush(std::cout);

}

