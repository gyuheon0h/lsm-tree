import struct 


class SSTableWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.offset_table = {}
        self.data_section = bytearray()
        self.offset = 0

    def add_entry(self, key, value):
        # serialize the key and value into bytes
        key_bytes = struct.pack('d', key)
        value_bytes = struct.pack('d', value)
        # update the offset table with the current offset
        self.offset_table[key] = self.offset
        # append the serialized key and value to the data section
        self.data_section.extend(key_bytes + value_bytes)
        # update the offset for the next entry
        self.offset += len(key_bytes) + len(value_bytes)

    def write_to_disk(self):
        try:
            with open(self.file_path, 'wb') as file:
                # write the offset table
                for key, offset in self.offset_table.items():
                    file.write(struct.pack('d', key) + struct.pack('i', offset))
                # write a separator between the offset table and data section
                file.write(b'\n')
                # write the data section
                file.write(self.data_section)
            print(f"Data successfully written to {self.file_path}")
        except Exception as e:
            print(f"Failed to write to disk: {e}")
