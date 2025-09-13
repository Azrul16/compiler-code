"""
Tag Constants Implementation

Single-character tokens use ASCII values, while multi-character
tokens use values above 255 to avoid conflicts.
"""

class Tag:
    # Single-character tokens use ASCII values
    # Multi-character tokens
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259
    # Relational operators
    LE = 260  # <=
    GE = 261  # >=
    EQ = 262  # ==
    NE = 263  # !=

if __name__ == "__main__":
    print("Tag Constants:")
    print("=" * 50)
    print(f"NUM: {Tag.NUM}")
    print(f"ID: {Tag.ID}")
    print(f"TRUE: {Tag.TRUE}")
    print(f"FALSE: {Tag.FALSE}")
    print(f"LE: {Tag.LE}")
    print(f"Plus ASCII: {ord('+')}")
    print(f"Minus ASCII: {ord('-')}")