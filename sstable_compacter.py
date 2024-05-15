import heapq
import struct

class SSTableCompacter:
    def __init__(self, file_path1, file_path2, output_file_path):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.output_file_path = output_file_path

    def compact(self):
        pq = []
        files = [open(self.file_path1, 'rb'), open(self.file_path2, 'rb')]

        # Initialize the priority queue with the first key from each file
        for i, file in enumerate(files):
            key, offset = self.read_key_offset(file)
            if key is not None:
                heapq.heappush(pq, (key, i, offset))

        with open(self.output_file_path, 'wb') as output_file:
            last_key, last_data = None, None

            while pq:
                key, file_index, data_offset = heapq.heappop(pq)
                data = self.read_data(files[file_index], data_offset)

                # Write to output file
                if key != last_key:
                    if last_key is not None:
                        self.write_key_data(output_file, last_key, last_data)
                    last_key, last_data = key, data

                # Read next key from the same file
                next_key, next_offset = self.read_key_offset(files[file_index])
                if next_key is not None:
                    heapq.heappush(pq, (next_key, file_index, next_offset))

            # Write the last key
            if last_key is not None:
                self.write_key_data(output_file, last_key, last_data)

        for file in files:
            file.close()

    def read_key_offset(self, file):
        header = file.read(8)
        if header == b'\n' or not header:
            return None, None
        return struct.unpack('ii', header)

    def read_data(self, file, offset):
        file.seek(offset)
        return struct.unpack('dd', file.read(16))

    def write_key_data(self, output_file, key, data):
        output_file.write(struct.pack('ii', key, len(data)))
        output_file.write(struct.pack('dd', *data))