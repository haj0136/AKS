from pathlib import Path
from cv_5_LZ77 import LZ77
import time

if __name__ == '__main__':
    files = ["../data/czech.txt"]
    for path in files:
        name = Path(path).stem
        print(f"-----------{name}----------")
        f = open(path, "r", encoding="utf-8-sig")
        message = f.read()
        f.close()
        test_text = "a b a b c b a b a b a a"
        test_text2 = 'ABRAKADABRA'
        print(f"Symbols count: {len(message)}")
        compressor = LZ77.Compressor(4)
        print("Encoding")
        encoded_string = compressor.compress(test_text2, verbose=True)
        print(f"Length of encoded string = {len(encoded_string)}")
        print(f"BPS = {len(encoded_string) / len(message)}")
        print("Decoding")
        start = time.time()
        decoded_string = compressor.decompress(encoded_string)
        end = time.time()
        print(f"Time: {end - start}")
        print(f"Symbols count: {len(decoded_string)}")
