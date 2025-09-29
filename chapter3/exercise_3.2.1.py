# Exercise 3.2.1:
# Simulate input buffering using two buffers (buffer pairs).
# Each buffer has a fixed size. The scanner reads characters sequentially.
# When one buffer is exhausted, the other is filled with the next chunk of input.

class BufferPair:
    def __init__(self, text, buffer_size=8):
        self.text = text
        self.buffer_size = buffer_size
        self.pointer = 0
        self.buffers = ["", ""]  # two buffers
        self.active = 0          # active buffer index
        self.load_buffer(0)
        self.load_buffer(1)

    def load_buffer(self, index):
        start = self.pointer
        end = min(self.pointer + self.buffer_size, len(self.text))
        self.buffers[index] = self.text[start:end]
        self.pointer = end

    def get_chars(self):
        while self.buffers[0] or self.buffers[1]:
            buf = self.buffers[self.active]
            for c in buf:
                yield c
            # Switch buffer when current is exhausted
            self.active = 1 - self.active
            self.load_buffer(self.active)
            if not self.buffers[self.active]:
                break

# Example text input
text = "This is a sample string for buffer pair simulation."

bp = BufferPair(text, buffer_size=10)

print("Reading characters with buffer pairs:")
for ch in bp.get_chars():
    print(ch, end="|")
