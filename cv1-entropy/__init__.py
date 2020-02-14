import math


def get_manhatton(dict1: dict, dict2: dict):
    unique_chars = set(dict1.keys()).union(set(dict2.keys()))

    result = 0
    for symb in unique_chars:
        x = 0
        y = 0
        if symb in dict1:
            x = dict1[symb]
        else:
            x = 0
        if symb in dict2:
            y = dict2[symb]
        else:
            y = 0

        result = result + abs(x-y)
    return result


def get_probability(message):
    charDict = {}
    for char in message:
        if char in charDict:
            charDict[char] = charDict[char]+1
        else:
            charDict[char] = 1

    n = len(message)

    entropy = 0
    for symb in charDict:
        p = charDict[symb] / n
        charDict[symb] = p
        entropy = entropy + (-p * math.log2(p))

    print(f"entropy = {entropy}")
    return charDict

if __name__ == '__main__':
    f = open("../data/czech.txt", "r", encoding="utf8")
    czech_message = f.read().lower()
    f = open("../data/english.txt", "r", encoding="utf8")
    english_message = f.read().lower()

    print("CZECH")
    cz_dict = get_probability(czech_message)


    print(cz_dict)
    print(len(cz_dict))
    print("ENGLISH")
    en_dict = get_probability(english_message)

    print(get_manhatton(cz_dict, en_dict))
