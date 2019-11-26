from typing import NamedTuple, Sequence, Callable, Optional
import itertools
import string
import unicodedata


class Encoding(NamedTuple):
    text: str
    code: int


_encoding_table: Sequence[Encoding] = [
    *(
        Encoding(text=x, code=y)
        for x, y in itertools.chain(
            zip(string.ascii_uppercase, range(0x0, 0x1A)),
            zip(string.ascii_lowercase, range(0x1A, 0x34)),
            zip(string.digits, range(0x34, 0x3E)),
        )
    ),
    Encoding(text="!", code=0x3E),
    Encoding(text="?", code=0x3F),
    Encoding(text="-", code=0x40),
    Encoding(text=".", code=0x41),
    Encoding(text=",", code=0x42),
    Encoding(text=unicodedata.lookup("HORIZONTAL ELLIPSIS"), code=0x43),
    Encoding(text=unicodedata.lookup("RIGHTWARDS WHITE ARROW"), code=0x44),
    Encoding(text="(", code=0x45),
    Encoding(text=")", code=0x46),
    Encoding(text=unicodedata.lookup("ANKH"), code=0x47),
    Encoding(text=unicodedata.lookup("WATER WAVE"), code=0x48),
    Encoding(text=unicodedata.lookup("SNAKE"), code=0x49),
    # TODO: $4A: picture of Link's head in the kidnapper signs (left half)
    # TODO: $4B: picture of Link's head in the kidnapper signs (right half)
    Encoding(text=unicodedata.lookup("LEFT DOUBLE QUOTATION MARK"), code=0x4C),
    Encoding(text=unicodedata.lookup("UPWARDS ARROW"), code=0x4D),
    Encoding(text=unicodedata.lookup("DOWNWARDS ARROW"), code=0x4E),
    Encoding(text=unicodedata.lookup("LEFTWARDS ARROW"), code=0x4F),
    Encoding(text=unicodedata.lookup("RIGHTWARDS ARROW"), code=0x50),
    Encoding(text="'", code=0x51),
    # TODO: $52: heart piece upper left filled (just left side)
    # TODO: $53: heart piece empty (just right side)
    # TODO: $54: heart piece left filled (just left side)
    # TODO: $55: heart piece 3/4 filled (just left side)
    # TODO: $56: heart piece upper right filled (just right side)
    # TODO: $57: heart piece all filled (just left side)
    # TODO: $58: heart piece all filled (just right side),
    Encoding(text=" ", code=0x59),
    Encoding(text=unicodedata.lookup("LEFTWARDS WHITE ARROW"), code=0x5A),
    Encoding(text=unicodedata.lookup("CIRCLED LATIN CAPITAL LETTER A"), code=0x5B),
    Encoding(text=unicodedata.lookup("CIRCLED LATIN CAPITAL LETTER B"), code=0x5C),
    Encoding(text=unicodedata.lookup("CIRCLED LATIN CAPITAL LETTER X"), code=0x5D),
    Encoding(text=unicodedata.lookup("CIRCLED LATIN CAPITAL LETTER Y"), code=0x5E),
    # TODO: $5F: alternate "l" or "I"? (apparently not used)
    # TODO: $60: alternate "!" (apparently not used)
    # TODO: $61: upside down "!" (apparently not used)
    # TODO: $62 to $65: apparently tab characters or space characters? (apparently not used)
    # TODO: $66: strange red and white '.' (apparently not used)
]


def _ord(char: str) -> int:
    """
    Convert a character into the encoding byte.

    """
    for encoding in _encoding_table:
        if encoding.text == char:
            return encoding.code
    raise ValueError(f"Unable to encode {char!r}")


def _chr(ordinal: int) -> str:
    """
    Convert a encoded byte back into a character.

    """
    for encoding in _encoding_table:
        if encoding.code == ordinal:
            return encoding.text
    raise ValueError(f"Unable to decode {ordinal!r}")


def encode(s: str) -> bytes:
    """
    Encode a string into a series of bytes.

    """
    return bytes(map(_ord, s))


def decode(b: bytes, *, on_fail: Optional[Callable[[int], str]] = None) -> str:
    """
    Decode a string from a series of bytes.

    on_fail (if supplied) is called when a byte fails to decode. This can be
    used to generate a fallback character.

    """
    chars = []
    for x in b:
        try:
            char = _chr(x)
        except ValueError:
            if on_fail is None:
                raise
            else:
                char = on_fail(x)
        chars.append(char)
    return "".join(chars)
