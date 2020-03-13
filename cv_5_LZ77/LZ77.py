from bitarray import bitarray


class Compressor:
    MAX_WINDOW_SIZE = 32768
    DISTANCE_BITS = 12
    LENGTH_BITS = 4

    def __init__(self, window_size=20, match_size=15, verbose=False):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = match_size
        self.verbose = verbose

        while self.window_size >= 2 ** self.DISTANCE_BITS:
            self.DISTANCE_BITS += 1
        while self.lookahead_buffer_size >= 2 ** self.LENGTH_BITS:
            self.LENGTH_BITS += 1
        if verbose:
            print(f"Distance bits = {self.DISTANCE_BITS}")
            print(f"Length bits = {self.LENGTH_BITS}")

    def compress(self, input_file, output_file_path=None):
        data = input_file
        i = 0
        output_buffer = bitarray(endian='big')
        triplets = 0

        while i < len(data):
            match = self.find_longest_match(data, i)

            if match:  # WRITE binary to output buffer distance|length|symbol
                (bestMatchDistance, bestMatchLength) = match
                if i + bestMatchLength < len(data):
                    symbol = data[i + bestMatchLength]
                else:
                    symbol = "\x00"
                distance_binary = f"{bestMatchDistance:0{self.DISTANCE_BITS}b}"
                if len(distance_binary) > self.DISTANCE_BITS:
                    raise ValueError(f"Distance binary string > {self.DISTANCE_BITS}")
                output_buffer += bitarray(distance_binary)
                length_binary = f"{bestMatchLength:0{self.LENGTH_BITS}b}"
                if len(length_binary) > self.LENGTH_BITS:
                    raise ValueError(f"Length binary string > {self.LENGTH_BITS}")
                output_buffer += bitarray(length_binary)
                symbol_bytes = symbol.encode()
                if len(symbol_bytes) > 1:
                    raise ValueError("Symbol encode error")
                output_buffer.frombytes(symbol_bytes)
                triplets += 1

                if self.verbose:
                    print("<%i, %i, %s>" % (bestMatchDistance, bestMatchLength, symbol))

                i += bestMatchLength + 1

        if output_file_path:
            with open(output_file_path, "wb") as file:
                output_buffer.tofile(file)
        return output_buffer, triplets

    def decompress(self, input_file_path):
        data = bitarray(endian='big')
        output_buffer = []

        # read the input file
        try:
            with open(input_file_path, 'rb') as input_file:
                data.fromfile(input_file)
        except IOError:
            raise IOError('Could not open input file ...')

        while len(data) >= 24:

            distance = int(data[0:self.DISTANCE_BITS].to01(), 2)
            length_end_index = (self.DISTANCE_BITS + self.LENGTH_BITS)
            length = int(data[self.DISTANCE_BITS:length_end_index].to01(), 2)
            symbol = data[length_end_index:length_end_index + 8].tostring()

            del data[0:length_end_index + 8]
            if self.verbose:
                print(f"<{distance}, {length}, {symbol}>")
            if length == 0:
                output_buffer.append(symbol)
            else:
                current_index = len(output_buffer)
                for ref in range(length):
                    char = output_buffer[current_index - distance + ref]
                    output_buffer.append(char)
                output_buffer.append(symbol)

        out_data = ''.join(output_buffer)

        return out_data

    def find_longest_match(self, data, current_position):
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data))
        start_index = max(0, current_position - self.window_size)

        best_match_distance = 0
        best_match_length = 0
        # print(f"Search buffer: {data[start_index:current_position]}")
        # print(f"Ahead buffer: {data[current_position:end_of_buffer]}")

        for j in range(start_index, current_position):  # search buffer
            match_length = 0
            match_distance = current_position - j
            for i in range(current_position, end_of_buffer):  # look-ahead buffer
                if data[j + match_length] == data[i]:
                    match_length += 1
                else:
                    break

            if match_length > best_match_length:
                best_match_distance = match_distance
                best_match_length = match_length

        return best_match_distance, best_match_length
