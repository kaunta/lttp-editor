assert __name__ == "__main__"

import argparse
import pathlib

import lttp.text

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
rom = bytearray(pathlib.Path(args.input).read_bytes())
rom[940904:940924] = lttp.text.encode("LO, praise of the   ")
rom[940925:940947] = lttp.text.encode("prowess of people-    ")
rom[940948:940965] = lttp.text.encode("kings, of spear- ")
rom[940968:940991] = lttp.text.encode("armed Danes, in days   ")
pathlib.Path(args.output).write_bytes(rom)
