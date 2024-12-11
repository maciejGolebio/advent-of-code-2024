#include <iostream>
#include <vector>
#include <cstdint>
#include <map>
#include <string>

using namespace std;

std::unordered_map<string, int> calculated;

inline string toKey(const unsigned long long &num, const int &depth)
{
    return to_string(num) + "|" + to_string(depth);
}

inline long digitCount(const long long &x)
{

    if (x == 0)
        return 1;
    long count = 0;
    long long temp = (x < 0) ? -x : x;

    while (temp > 0)
    {
        temp /= 10;
        count++;
    }
    return count;
}

inline void splitEvenDigits(const unsigned long long &num, unsigned long long &leftPart, unsigned long long &rightPart)
{
    long count = digitCount(num);
    long half = count / 2;
    long long p = 1;
    for (long i = 0; i < half; ++i)
    {
        p *= 10;
    }
    leftPart = num / p;
    rightPart = num % p;
}

long long blink(const unsigned long long &num, const int &depth)
{
    auto cached = calculated.find(toKey(num, depth));
    if (cached != calculated.end())
    {
        // cout << "cached " << toKey(num, depth) << " : " << cached->second << endl;

        return cached->second;
    }
    if (depth == 0)
    {
        return 1;
    }

    if (num == 0)
    {
        long long result = blink(1, depth - 1);
        calculated[toKey(num, depth)] = result;
        return result;
    }

    if (digitCount(num) % 2 == 0)
    {
        unsigned long long leftPart, rightPart;
        splitEvenDigits(num, leftPart, rightPart);

        unsigned long long result = blink(leftPart, depth - 1) + blink(rightPart, depth - 1);
        calculated[toKey(num, depth)] = result;
        return result;
    }
    else
    {
        unsigned long long result = blink(num * 2024, depth - 1);
        calculated[toKey(num, depth)] = result;
        return result;
    }
}

int main(int argc, char *argv[])
{
    // UNSIGNED LONG LONG IS TO SMALL FOR THIS PROBLEM: SEE PYTHON SOLUTION
    unsigned long long sum = 0;
    std::vector<unsigned long long> initialStones = {890, 0, 1, 935698, 68001, 3441397, 7221, 27};
    int depth = atoi(argv[1]);
    for (auto stone : initialStones)
    {
        unsigned long long partialSum = blink(stone, depth);
        sum += partialSum;
        cout << "Stone: " << stone << " Current Result: " << sum << " Partial Result: " << partialSum << endl;
    }
    cout << "Result: " << sum << endl;
    return 0;
}