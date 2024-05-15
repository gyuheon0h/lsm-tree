import struct 

class SSTableWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.offset_table = {}
        self.data_section = bytearray()
        self.offset = 0

    def add_entry(self, key, value):
        # Serialize the value into bytes
        value_bytes = struct.pack('d' * len(value), *value)
        # Update the offset table with the current offset
        self.offset_table[key] = self.offset
        # Append the serialized value to the data section
        self.data_section.extend(value_bytes)
        # Update the offset for the next entry
        self.offset += len(value_bytes)

    def write_to_disk(self):
        with open(self.file_path, 'wb') as file:
            # First, write the offset table
            # Format: key (int) and offset (int) for each entry
            for key, offset in self.offset_table.items():
                file.write(struct.pack('ii', key, offset))
            # Write a separator between the offset table and data section
            file.write(b'\n')
            # Finally, write the data section
            file.write(self.data_section)

sstable = SSTableWriter('sstable_file.sst')
sstable.add_entry(1, (123.456, 789.012))
sstable.add_entry(2, (234.567, 890.123))
sstable.write_to_disk()