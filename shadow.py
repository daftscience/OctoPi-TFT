"""
Drop shadows with PIL.

Author: Kevin Schluff
License: Python license
"""
from PIL import Image, ImageFilter, ImageDraw
from global_variables import COLORS


def dropShadow(image, offset=(5, 5), background=0xffffff, shadow=0x444444,
               border=8, iterations=3):
    """
    Add a gaussian blur drop shadow to an image.

    image       - The image to overlay on top of the shadow.
    offset      - Offset of the shadow from the image as an (x,y) tuple.  Can be
                  positive or negative.
    background  - Background colour behind the image.
    shadow      - Shadow colour (darkness).
    border      - Width of the border around the image.  This must be wide
                  enough to account for the blurring of the shadow.
    iterations  - Number of times to apply the filter.  More iterations
                  produce a more blurred shadow, but increase processing time.
    """

    # Create the backdrop image -- a box in the background colour with a
    # shadow on it.
    totalWidth = image.size[0] + abs(offset[0]) + 2 * border
    totalHeight = image.size[1] + abs(offset[1]) + 2 * border
    back = Image.new(image.mode, (totalWidth, totalHeight), background)

    # Place the shadow, taking into account the offset from the image
    shadowLeft = border + max(offset[0], 0)
    shadowTop = border + max(offset[1], 0)
    back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0],
                        shadowTop + image.size[1]])

    # Apply the filter to blur the edges of the shadow.  Since a small kernel
    # is used, the filter must be applied repeatedly to get a decent blur.
    n = 0
    while n < iterations:
        back = back.filter(ImageFilter.BLUR)
        n += 1

    # Paste the input image onto the shadow backdrop
    imageLeft = border - min(offset[0], 0)
    imageTop = border - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))

    return back


class rounded_rectangle():

    def __init__(self, size, radius, fill):
        self.size = size
        self.fill = fill
        self.radius = radius
        self.image = self.round_rectangle()
        self.image.show()

    def round_corner(self):
            """Draw a round corner"""
            corner = Image.new('RGBA', (self.radius, self.radius), (0, 0, 0, 0))
            draw = ImageDraw.Draw(corner)
            draw.pieslice((0, 0, self.radius * 2, self.radius * 2), 180, 270, fill=self.fill)
            return corner

    def round_rectangle(self):
            """Draw a rounded rectangle"""
            rectangle = Image.new('RGBA', self.size, self.fill)
            width, height = self.size
            corner = self.round_corner()
            rectangle.paste(corner, (0, 0))
            # Rotate the corner and paste it
            rectangle.paste(corner.rotate(90), (0, height - self.radius))
            rectangle.paste(
                corner.rotate(180), (width - self.radius, height - self.radius))
            rectangle.paste(corner.rotate(270), (width - self.radius, 0))
            return rectangle




    def add_corners(self):
        circle = Image.new('L', (self.radius * 2, self.radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, self.radius * 2, self.radius * 2), fill=255)
        alpha = Image.new('L', im.size, "white")
        w, h = im.size
        alpha.paste(circle.crop((0, 0, self.radius, self.radius)), (0, 0))
        alpha.paste(circle.crop((0, self.radius, self.radius, self.radius * 2)), (0, h - self.radius))
        alpha.paste(circle.crop((self.radius, 0, self.radius * 2, self.radius)), (w - self.radius, 0))
        # alpha.paste(circle.crop((self.radius, self.radius, self.radius * 2, self.radius * 2)), (w - self.radius, h - self.radius))
        im.putalpha(alpha)
        return im




if __name__ == "__main__":
    import sys

    image = Image.open('pic.png')
    # image.thumbnail((200, 200), Image.ANTIALIAS)
    shadow  = rounded_rectangle((310, 60), 12, COLORS['PURPLE'])

    shadow.image.show()
    # dropShadow(image).show()
    dropShadow(
        shadow.image,
        background=0xeeeeee,
        shadow=0x444444,
        offset=(
            0,
            5))
