from bitarray import bitarray
from cv_3_huffman.tree import build_tree, Leaf, InternalNode
from pathlib import Path
import math
import time


def get_probability(_message):
    char_dict = {}
    for char in _message:
        if char in char_dict:
            char_dict[char] = char_dict[char]+1
        else:
            char_dict[char] = 1

    n = len(_message)

    entropy = 0
    for symb in char_dict:
        p = char_dict[symb] / n
        entropy = entropy + (-p * math.log2(p))

    print(f"entropy = {entropy}")
    return char_dict


def encode(_tree, input_string):
    encoded_chars_list = list()
    for char in input_string:
        if char not in _tree.codes:
            raise ValueError(f"Unknown symbol: {char}")
        char_code = "".join(map(str, _tree.codes[char]))
        encoded_chars_list.append(char_code)
    return "".join(encoded_chars_list)


def decode(_tree, enc_string):
    decoded_chars = []

    current_node = _tree.root
    for _bit in enc_string:
        if _bit == "0":
            next_node = current_node.leftchild
        elif _bit == "1":
            next_node = current_node.rightchild
        else:
            raise ValueError("Invalid value")

        if isinstance(next_node, Leaf):
            decoded_chars.append(next_node.symbol)
            current_node = _tree.root
        elif isinstance(next_node, InternalNode):
            current_node = next_node
        else:
            raise AssertionError("Illegal node type")

    return "".join(decoded_chars)


def get_tree_for_doc(input_string):
    freq_dict = get_probability(input_string)
    print(f"Symbols: {len(freq_dict)}")
    tree = build_tree(freq_dict)
    return tree


if __name__ == '__main__':
    files = ["../data/czech.txt", "../data/english.txt"]
    for path in files:
        name = Path(path).stem
        print(f"-----------{name}----------")
        f = open(path, "r", encoding="utf-8-sig")
        message = f.read()
        f.close()
        print(f"Symbols count: {len(message)}")
        print("Building tree")
        code_tree = get_tree_for_doc(message)
        print("Encoding")
        encoded_string = encode(code_tree, message)
        print(f"Length of encoded string = {len(encoded_string)}")
        print(f"BPS = {len(encoded_string)/len(message)}")
        print("Decoding")
        start = time.time()
        decoded_string = decode(code_tree, encoded_string)
        end = time.time()
        print(f"Time: {end - start}")
        print(f"Symbols count: {len(decoded_string)}")
        # print(decoded_string)


# 1) Which of these codes cannot be Huffman codes for any probability assignment and why?
# a) {0, 10, 11} - yes
# b) {00, 01, 10, 110} - No
# c) {01, 10} - No
#
# 2) Classes of codes. Consider the code {0, 01}.
# b) Is it uniquely decodable? - YES
# c) It it nonsingular? - YES
#
# 3) Optimal word lengths.
# a) Can l=(1, 2, 2) be the word lengths of a binary Huffman code? - YES
# a) Can l=(2, 2, 3, 3) be the word lengths of a binary Huffman code? - NO
