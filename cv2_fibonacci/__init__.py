from bitarray import bitarray
from cv2_fibonacci import fastfibonacci as ff
from pathlib import Path

fib_numbers = list([1, 2])


def elias_decode(encoded_string):
    numbers = list()
    index = 0
    while index < len(encoded_string):
        length = 0
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
    return numbers


def elias_encode(numbers):
    encoded_string = ""
    for n in numbers:
        beta = bin(int(n))[2:]
        alpha = ""
        for i in range(len(beta) - 1):
            alpha = alpha + '0'
        gamma = alpha + beta
        encoded_string += gamma
    return encoded_string


def fibonacci_decode(encoded_string):
    numbers = list()
    index = 0
    while index < len(encoded_string):
        length = 0
        valid = False
        for n in encoded_string[index: len(encoded_string)]:
            if n == "1" and encoded_string[index + length + 1] == "1":
                length += 2
                valid = True
                break
            else:
                length += 1
        if valid:
            codeword = encoded_string[index: index + length - 1]
            number = 0
            for i, n in enumerate(codeword):
                if n == "1":
                    number += ff.fibonacci(i + 2)
            numbers.append(number)
        index += length
    return numbers


# return largest fibonacci number less or equal to parameter
def get_fib_loe(n: int):
    index = 0
    while fib_numbers[index] < n:
        index += 1
        if index >= len(fib_numbers):
            fib_numbers.append(ff.fibonacci(index + 2))
    if fib_numbers[index] == n:
        return index
    return index - 1


def fibonacci_encode(numbers):
    encoded_string = ""
    for n_str in numbers:
        n = int(n_str)
        if n < 1:
            raise ValueError("Numbers must be greater than 0")
        index = get_fib_loe(n)
        codeword = ['0' for i in range(index + 2)]
        codeword[-1] = '1'
        codeword[-2] = '1'
        actual_number = n - fib_numbers[index]
        while actual_number > 0:
            new_index = get_fib_loe(actual_number)
            codeword[new_index] = '1'
            actual_number -= fib_numbers[new_index]
        encoded_string += "".join(codeword)
    return encoded_string


def save_as_binary(encoded_string, file_path):
    a = bitarray(encoded_string)
    with open(file_path, "wb") as file:
        a.tofile(file)


def load_binary(file_path):
    a = bitarray()
    with open(file_path, "rb") as file:
        a.fromfile(file)
    return a


def elias_test(numbers, file_path):
    print("ELIAS TEST")
    print("Encode")
    print(f"Numbers count: {len(numbers)}")
    elias_encoded = elias_encode(numbers)
    if len(numbers) > 10:
        print(str(numbers[1:10]))
    else:
        print(str(numbers))
    save_as_binary(elias_encoded, file_path)
    loaded_binary = load_binary(file_path)
    print(f"Length of binary: {len(loaded_binary)}")
    print("Decode")
    decoded_numbers = elias_decode(loaded_binary.to01())
    if len(decoded_numbers) > 10:
        print(str(decoded_numbers[1:10]))
    else:
        print(str(decoded_numbers))


def fibonacci_test(numbers, file_path):
    print("FIBONACCI TEST")
    print("Encode")
    print(f"Numbers count: {len(numbers)}")
    fib_encoded = fibonacci_encode(numbers)
    if len(numbers) > 10:
        print(str(numbers[1:10]))
    else:
        print(str(numbers))
    save_as_binary(fib_encoded, file_path)
    loaded_binary = load_binary(file_path)
    print(f"Length of binary: {len(loaded_binary)}")
    print("Decode")
    decoded_numbers = fibonacci_decode(loaded_binary.to01())
    if len(decoded_numbers) > 10:
        print(str(decoded_numbers[1:10]))
    else:
        print(str(decoded_numbers))


if __name__ == '__main__':
    files = ["../data/uniform_8.txt", "../data/gausian_8.txt", "../data/exponential_8.txt"]

    for f in files:
        name = Path(f).stem
        print(f"-----------{name}----------")
        # Load file
        with open(f) as file:
            integers = file.read().split("\n")

        test_numbers = [1, 11, 143]
        # Encoding Elias
        elias_test(integers, f"elias_{name}")
        # Encoding fibonacci
        fibonacci_test(integers, f"fib_{name}")



