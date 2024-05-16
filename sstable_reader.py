import struct

# TODO: THIS IS BUGGED TO THE MOON
class SSTableReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def query_key(self, query_key):
        with open(self.filepath, 'rb') as file:
            content = file.read()
            # Find the separator to distinguish between the offset table and the data section
            separator_index = content.index(b'\n')
            offset_table_content = content[:separator_index]
            data_section = content[separator_index + 1:]

            # Parse the offset table
            offset_table = {}
            offset_size = struct.calcsize('di')
            print(f"Expected offset size: {offset_size}")
            print(f"Offset table content size: {len(offset_table_content)}")

            for i in range(0, len(offset_table_content), offset_size):
                if i + offset_size <= len(offset_table_content):
                    key, offset = struct.unpack('di', offset_table_content[i:i + offset_size])
                    offset_table[key] = offset
                else:
                    print(f"Skipping incomplete record at index {i}")

            if query_key in offset_table:
                start_offset = offset_table[query_key]
                data_bytes = data_section[start_offset:start_offset + struct.calcsize('dd')]
                data = struct.unpack('dd', data_bytes)
                return data
            else:
                return None