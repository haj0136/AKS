from pathlib import Path
from cv_5_LZ77 import LZ77
import time
import os

VERBOSE = False


def save_text_file(text, file_path):
    with open(file_path, 'w') as output_file:
        output_file.write(text)


def print_results(file, _triplets, _file_size, _win_size, _max_match, enc_size, bps):
    print(f"{file} \t {_triplets} \t {_file_size} \t  {_win_size:05} \t\t  {_max_match} \t\t {enc_size} \t  {bps:0.3f}")


if __name__ == '__main__':
    files = ["../data/english.txt"]
    print("File  \t Triplets \t File Size \t Window Size \t Max.match \t Enc.Size \t BPS")
    print("----------------------------------------------------------------------------")
    for path in files:
        for win_size, max_match in [(4096, 16), (16384, 32), (32768, 64)]:
            name = Path(path).stem
            f = open(path, "r", encoding="utf-8-sig")
            message = f.read()
            f.close()
            test_text = "eastman easily grows alfalfa in his garden"
            test_text2 = 'ABRAKADABRA'
            if VERBOSE:
                print(f"Symbols count: {len(message)}")
            file_size = os.path.getsize(path)
            compressor = LZ77.Compressor(window_size=win_size - 1, match_size=max_match - 1, verbose=VERBOSE)
            if VERBOSE:
                print("Encoding")
            encoded_bin, triplets = compressor.compress(message, output_file_path=f"message_{name}.bin")
            if VERBOSE:
                print("Decoding")
            start = time.time()
            decoded_string = compressor.decompress(f"message_{name}.bin")
            end = time.time()
            if VERBOSE:
                print(f"Time: {end - start}")
                print(f"Symbols count: {len(decoded_string)}")
            save_text_file(decoded_string, "text.txt")
            print_results(name, triplets, file_size, win_size, max_match, len(encoded_bin), len(encoded_bin) / file_size)


