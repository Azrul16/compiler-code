# Exercise 3.2.2:
# Simulate input buffering with sentinels.
# A sentinel (special EOF marker) is placed at the end of the buffer to simplify scanning.

class SentinelBuffer:
    def __init__(self, text, buffer_size=8):
        self.text = text + "$"  # Use '$' as sentinel marker (end of input)
        self.buffer_size = buffer_size
        self.index = 0
        self.buffer = ""

    def load_buffer(self):
        if self.index < len(self.text):
            end = min(self.index + self.buffer_size - 1, len(self.text))
            self.buffer = self.text[self.index:end]
            self.buffer += "$"  # place sentinel at end of buffer
            self.index = end
        else:
            self.buffer = "$"

    def get_chars(self):
        self.load_buffer()
        while True:
            for c in self.buffer:
                if c == "$":   # sentinel reached
                    if self.index >= len(self.text):  # real end of input
                        return
                    else:
                        self.load_buffer()
                        break
                yield c

# Example input
text = "Lexical analyzer buffer simulation using sentinel."

sb = SentinelBuffer(text, buffer_size=12)

print("Reading characters with sentinel buffer:")
for ch in sb.get_chars():
    print(ch, end="|")
