#!/usr/bin/python3
from PIL import Image
import argparse, sys


# parse command line arguments
parser = argparse.ArgumentParser(description="make a 'invisible' image")
parser.add_argument("infile", metavar="INPUT_FILE", type=str, default="img.png",
                    help="input file, image")
parser.add_argument("outfile", metavar="OUTPUT_FILE", type=str, default="out.png",
                    help="output file, image")
parser.add_argument("-c", "--color", type=tuple, default=(54, 57, 63, 255),
                    help="custom color to be used as background, type: tuple, (R, G, B, A)")
parser.add_argument("-i", "--invert", action="store_true",
                    help="whether to invert or not")
args = parser.parse_args()

if args.invert:
    fgcolor = args.color
    bgcolor = args.color[:3] + (0,)
else:
    bgcolor = args.color
    fgcolor = args.color[:3] + (0,)
# open input image
try:
    img = Image.open(args.infile)
except FileNotFoundError: # while checking for errors
    print(f"File {args.infile} does not exist")
    sys.exit(1)
# except PIL.UnidentifiedImageError:
#     print("File could not be identified")
#     sys.exit(1)
# convert image to 1-bit, then to RGBA format (for alpha channel)
img = img.convert("L").convert("RGBA")

# then iterate over the whole image...
for y in range(img.height):
    for x in range(img.width):
        # ...and set any pixel that is darker than 127 to bgcolor, else fgcolor
        px = img.getpixel((x, y))
        if sum(px[:3]) / 3 < 127:
            img.putpixel((x, y), fgcolor)
        else:
            img.putpixel((x, y), bgcolor)

# finally save the resulting image
try:
    img.save(args.outfile)
except ValueError: # while checking for errors
    print(f"Error saving image (as {args.outfile}): Output format could not be detected")
    sys.exit(1)
except IOError:
    print("Write error")
    sys.exit(1)
