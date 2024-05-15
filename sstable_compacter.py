import struct

class SSTableCompacter:
    def __init__(self, file_path1, file_path2, output_file_path):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.output_file_path = output_file_path

    def compact(self):
        entries = {}
        # Read entries from both files
        for file_path in [self.file_path1, self.file_path2]:
            with open(file_path, 'rb') as file:
                # Read until the newline separator
                while True:
                    header = file.read(8)  # Read key and offset pair (4 bytes each)
                    if header == b'\n':
                        break
                    key, offset = struct.unpack('ii', header)
                    # Move to the data offset
                    current_pos = file.tell()
                    file.seek(offset)
                    # Data is a tuple of two doubles
                    data = struct.unpack('dd', file.read(16))
                    entries[key] = data
                    file.seek(current_pos)

        with open(self.output_file_path, 'wb') as file:
            offset = 0
            offset_table = bytearray()
            data_section = bytearray()
            for key in sorted(entries.keys()):
                value = entries[key]
                value_bytes = struct.pack('dd', *value)
                offset_table.extend(struct.pack('ii', key, offset))
                data_section.extend(value_bytes)
                offset += len(value_bytes)
            file.write(offset_table)
            file.write(b'\n')
            file.write(data_section)