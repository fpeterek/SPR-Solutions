// https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=7&page=show_problem&problem=535

#include <iostream>
#include <cstdint>


int main(int argc, const char * argv[]) {

    while (not std::cin.eof()) {

        std::string line;
        std::getline(std::cin, line);

        if (line.empty()) {
            break;
        }

        int32_t in = std::stoi(line);
        uint32_t uin = in;
        const int32_t swapped = ((uin & (255      )) << 24) | 
                                ((uin & (255 << 8 )) << 8)  |
                                ((uin & (255 << 16)) >> 8)  |
                                ((uin & (255 << 24)) >> 24);

        std::cout << in << " converts to " << swapped << std::endl;

    }
}

