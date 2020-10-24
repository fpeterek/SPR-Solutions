#include <iostream>
#include <string>
#include <sstream>
#include <cmath>
#include <array>
#include <vector>
#include <algorithm>
#include <limits>
#include <iomanip>
#include <bitset>


std::array<std::vector<uint64_t>, 8> permutations;

void emplace(const std::vector<uint64_t> & current) {
    uint64_t perm = 0;
    for (int i = 0; i < current.size(); ++i) {
        perm = perm bitor ( (current[i] bitand 0xFF) << (i*8) );
    }
    permutations[current.size() - 1].emplace_back(perm);
}


void generate(const std::vector<uint64_t> left, const std::vector<uint64_t> current) {

    if (left.empty()) {
        return emplace(current);
    }

    for (size_t i = 0; i < left.size(); ++i) {
        uint64_t n = left[i];

        std::vector<uint64_t> copy = current;    
        std::vector<uint64_t> copyLeft = left;

        copyLeft.erase(copyLeft.begin()+i);
        copy.emplace_back(n);

        generate(std::move(copyLeft), std::move(copy));
    }

}

void generate(const int i) {

    std::vector<uint64_t> to_gen;

    for (int c = 1; c <= i; ++c) {
        to_gen.emplace_back(c);
    }

    generate(to_gen, {});
}


void gen_permutations() {

    for (int i = 0; i < 8; ++i) {
        permutations[i] = std::vector<uint64_t>();
    }

    permutations[0].reserve(1);
    permutations[1].reserve(2);
    permutations[2].reserve(6);
    permutations[3].reserve(24);
    permutations[4].reserve(120);
    permutations[5].reserve(720);
    permutations[6].reserve(5040);
    permutations[7].reserve(40320);

    for (int i = 1; i < 9; ++i) {
        generate(i);
    }
}

double distance(const double rad1, const double rad2) {

    const double r = rad1 + rad2;
    const double y = std::abs(rad1 - rad2);
    const double sin = y / r;
    const double sin2 = sin * sin;
    const double cos2 = 1 - sin2;
    const double cos = std::sqrt(cos2);

    return r * cos;

}


struct Circle {

    double x;
    double rad;

};


double run_perm(std::vector<double> line, uint64_t perm) {

    std::vector<Circle> circles;
    circles.reserve(line.size());
    double rightmost = 0;

    for (size_t i = 0; perm; ++i) {

        const size_t index = perm bitand 0xFFll;
        const double rad = line[index-1];
        double center = 0;

        for (const auto & c : circles) {
            const double dist = distance(rad, c.rad);
            center = std::max(center, c.x + dist);
        }

        center = std::max(center, rad);
        rightmost = std::max(center + rad, rightmost);

        circles.emplace_back(Circle{ center, rad });
        perm >>= 8;
    }

    return rightmost;

}


void run_case(std::vector<double> line) {
    const auto & perms = permutations[line.size() - 1];    
    double result = std::numeric_limits<double>::max();

    for (const uint64_t p : perms) {
        result = std::min(run_perm(line, p), result);             
    }
    std::cout << std::fixed << std::setprecision(3) << result << std::endl;
}


std::vector<double> read_line() {
    std::string line;
    std::getline(std::cin, line);
    std::stringstream ss(line);
    std::vector<double> nums;

    int in_size;
    ss >> in_size;

    nums.reserve(in_size);

    for (int i = 0; i < in_size; ++i) {
        double radius;
        ss >> radius;
        nums.emplace_back(radius);
    }
    
    return nums;
}


void handle() {
    std::string line;
    std::getline(std::cin, line);
    std::stringstream ss(line);
    int cases;
    ss >> cases;

    for (int i = 0; i < cases; ++i) {
        run_case(read_line());
    }
}


int main(int argc, const char * argv[]) {
    std::cin.sync_with_stdio(false);
    gen_permutations();
    handle();
}

