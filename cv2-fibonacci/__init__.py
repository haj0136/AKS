from bitarray import bitarray


def elias_decode(encoded_string):
    numbers = list()
    index = 0
    length = 0
    while index < len(encoded_string):
        valid = False
        for n in encoded_string[index: len(encoded_string)]:
            if n == '0':
                length += 1
            else:
                valid = True
                break
        index += length
        if valid:
            binary = encoded_string[index: index + length + 1]
            numbers.append(int(binary, 2))
            index = index + length + 1
            length = 0
    return numbers


def elias_encode(numbers):
    encoded_string = ""
    for n in numbers:
        beta = bin(n)[2:]
        alpha = ""
        for i in range(len(beta) - 1):
            alpha = alpha + '0'
        gamma = alpha + beta
        encoded_string += gamma
    return encoded_string


def fibonacci_decode(number):
    pass


def fibonacci_encode(number):
    pass


def save_as_binary(encoded_string, file_path):
    a = bitarray(encoded_string)
    with open(file_path, "wb") as file:
        a.tofile(file)


def load_binary(file_path):
    a = bitarray()
    with open(file_path, "rb") as file:
        a.fromfile(file)
    return a


if __name__ == '__main__':
    print("Encode")
    test_numbers = [14, 5]
    elias_encoded = elias_encode(test_numbers)
    print(str(test_numbers) + " = " + str(elias_encoded))
    print(len(elias_encoded))
    save_as_binary(elias_encoded, "encoded_file.bin")
    loaded_binary = load_binary("encoded_file.bin")
    print(loaded_binary.to01())
    print(loaded_binary.length())
    print("Decode")
    print(elias_decode(loaded_binary.to01()))

