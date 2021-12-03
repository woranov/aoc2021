#include <iostream>
#include <fstream>
#include <vector>


int compute(std::vector<std::string> numbers) {
    auto n = numbers.size();
    auto bitCount = numbers[0].size();

    auto gamma = 0;
    auto epsilon = 0;

    for (int i = 0; i < bitCount; ++i) {
        gamma <<= 1;
        epsilon <<= 1;

        int oneBitCount = 0;
        for (auto num : numbers) {
            if (num[i] == '1') {
                oneBitCount++;
            }
        }

        if (oneBitCount >= n - oneBitCount) {
            gamma += 1;
        } else {
            epsilon += 1;
        }
    }

    return gamma * epsilon;
}


int main() {
    std::string sourceFilePath = __FILE__;
    auto sourceDirPath = sourceFilePath.substr(0, sourceFilePath.rfind('\\'));
    auto inputPath = sourceDirPath + "/input.txt";

    std::ifstream file(inputPath);

    std::vector<std::string> numbers;

    if (!file) {
        std::cerr << "Couldn't open file " << inputPath << std::endl;
        return 1;
    }

    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            if (!line.empty()) {
                numbers.push_back(line);
            }
        }
        std::cout << compute(numbers) << std::endl;
        file.close();
    }

    return 0;
}
