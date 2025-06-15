import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
from data import colors, rectangles
from src.decoders import raw_decoder, raw_plus_decoder, hex_decoder, string_mini_decoder, string_decoder

print("""Select decoder:
0 - raw_decoder
1 - raw_plus_decoder
2 - hex_decoder
3 - string_mini_decoder
4 - string_decoder""")
decoder_choice = int(input("Enter choice: "))
match decoder_choice:
    case 0:
        show_image = raw_decoder.show_image
    case 1:
        show_image = raw_plus_decoder.show_image
    case 2:
        show_image = hex_decoder.show_image
    case 3:
        show_image = string_mini_decoder.show_image
    case 4:
        show_image = string_decoder.show_image
    case _:
        print("Invalid choice")
        sys.exit(1)



t1 = time.monotonic()
show_image(colors, rectangles)
print("Time taken:", time.monotonic() - t1)
