

def elias_decode(encoded_string):
    numbers = list()
    index = 0
    length = 0
    while index < len(encoded_string):
        for n in encoded_string[index: len(encoded_string)]:
            if n == '0':
                length += 1
            else:
                break
        index += length
        binary = encoded_string[index: index + length + 1]
        numbers.append(int(binary, 2))
        index = index + length + 1
        length = 0
    return numbers


def elias_encode(number):
    beta = bin(number)[2:]
    alpha = ""
    for i in range(len(beta) - 1):
        alpha = alpha + '0'
    gamma = alpha + beta
    return gamma


def fibonacci_decode(number):
    pass


def fibonacci_encode(number):
    pass


if __name__ == '__main__':
    test_number = 14
    test_number2 = 5
    elias_encoded = elias_encode(test_number)
    elias_encoded2 = elias_encode(test_number2)
    print(str(test_number) + " = " + str(elias_encoded))
    print(str(test_number2) + " = " + str(elias_encoded2))
    print("Decode")
    print(elias_decode(elias_encoded + elias_encoded2))

