"""
You are tasked with building a parser for a simplified, protobuf-like message definition 
language from a given text file or string. The input contains definitions for one or more 
message structures, where each definition begins with the keyword Message followed by a name 
(e.g., Message Vehicle). Each subsequent line within a message block defines a field with its 
type and name (e.g., string name). Your parser must handle the primitive data types int (4 bytes),
 float (4 bytes), and string (256 bytes). After parsing the entire input, your program should 
 expose an interface to query the parsed information. Specifically, you need to implement functions to: 
 1) calculate the total memory size of a given message name by summing the sizes of its fields 
 (e.g., get_size('Vehicle')), 2) return the size of a primitive type (e.g., get_size('int')), and 
 3) retrieve the data type of a specific field within a given message (e.g., get_type('Vehicle', 'name') 
 should return 'string').

"""

class ProtoParser:
    PRIMITIVE_SIZES = {
        "int": 4,
        "float": 4,
        "string": 256
    }

    def __init__(self, text):
        self.messages = {}
        self.parse(text)

    def parse(self, text):
        current = None
        for line in text.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("Message"):
                _, name = line.split()
                self.messages[name] = {}
                current = name
            else:
                if current is None:
                    raise ValueError("Field defined outside a Message block.")
                type_, field = line.split()
                self.messages[current][field] = type_

    def get_size(self, name):
        # primitive type
        if name in self.PRIMITIVE_SIZES:
            return self.PRIMITIVE_SIZES[name]

        # user-defined message
        if name not in self.messages:
            raise ValueError(f"Unknown type or message: {name}")

        total = 0
        for field, type_ in self.messages[name].items():
            total += self.get_size(type_)
        return total

    def get_type(self, message_name, field_name):
        # Person, name
        if message_name not in self.messages:
            raise ValueError(f"No such message: {message_name}")
        fields = self.messages[message_name]
        if field_name not in fields:
            raise ValueError(f"No such field: {field_name}")
        return fields[field_name]
