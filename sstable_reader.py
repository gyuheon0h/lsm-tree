import struct

# TODO: THIS IS BUGGED TO THE MOON
class SSTableReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def query_key(self, query_key):
        try:
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

                if len(offset_table_content) % offset_size != 0:
                    print("Warning: Offset table size is not a multiple of expected size. Data might be corrupted.")

                for i in range(0, len(offset_table_content), offset_size):
                    try:
                        key, offset = struct.unpack('di', offset_table_content[i:i + offset_size])
                        offset_table[key] = offset
                    except struct.error as e:
                        print(f"Failed to unpack offset table at index {i}: {e}")
                        continue

                # Check if the query key exists in the offset table
                if query_key in offset_table:
                    start_offset = offset_table[query_key]
                    # Ensure start_offset is within the data section bounds
                    if start_offset + struct.calcsize('dd') <= len(data_section):
                        data_bytes = data_section[start_offset:start_offset + struct.calcsize('dd')]
                        try:
                            data = struct.unpack('dd', data_bytes)
                            return data
                        except struct.error as e:
                            print(f"Failed to unpack data for key {query_key} at offset {start_offset}: {e}")
                            return None
                    else:
                        print(f"Data offset {start_offset} for key {query_key} is out of bounds.")
                        return None
                else:
                    print(f"Key {query_key} not found in offset table.")
                    return None
        except FileNotFoundError:
            print(f"File {self.filepath} not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None