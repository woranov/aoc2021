#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>


int findValue(std::vector<std::string> numbers, bool checkForMostCommon) {
    auto bitCount = numbers[0].size();

    for (int i = 0; i < bitCount; ++i) {
        int oneBitCount = 0;
        for (auto num : numbers) {
            if (num[i] == '1') {
                oneBitCount++;
            }
        }

        int mostCommon = oneBitCount >= numbers.size() - oneBitCount;

        int numToCheck;
        if (checkForMostCommon) {
            numToCheck = mostCommon;
        } else {
            numToCheck = mostCommon ^ 1;
        }

        numbers.erase(
            std::remove_if(numbers.begin(), numbers.end(), [&](auto n) {
                return n[i] != std::to_string(numToCheck)[0];
            }),
            numbers.end()
        );

        if (numbers.size() == 1) {
            break;
        }
    }

    return stoi(numbers[0], nullptr, 2);
}


int compute(const std::vector<std::string>& numbers) {
    return findValue(numbers, true) * findValue(numbers, false);
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
