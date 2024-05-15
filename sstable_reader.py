import struct

class SSTableReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def query_key(self, query_key):
        with open(self.file_path, 'rb') as file:
            # Read the entire file content
            content = file.read()
            # Find the separator to distinguish between the offset table and the data section
            separator_index = content.index(b'\n')
            offset_table_content = content[:separator_index]
            data_section = content[separator_index + 1:]

            # Parse the offset table
            offset_table = {}
            offset_size = struct.calcsize('ii')
            for i in range(0, separator_index, offset_size):
                key, offset = struct.unpack('ii', offset_table_content[i:i + offset_size])
                offset_table[key] = offset

            # Check if the query_key exists in the offset table
            if query_key in offset_table:
                # Get the offset of the data for the query_key
                start_offset = offset_table[query_key]
                # Data is stored as doubles and we know the length of each entry
                # Each entry has 2 doubles TODO: look over this
                data_bytes = data_section[start_offset:start_offset + struct.calcsize('dd')]
                data = struct.unpack('dd', data_bytes)
                return data
            else:
                return None