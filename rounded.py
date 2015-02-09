from PIL import Image, ImageDraw, ImageFilter
from global_variables import SHADING_QUALITY, CORNER_QUALITY


class rounded_rect():

    def __init__(self, og_size, radius, fill, quality, shadow=False):
        self.quality = quality
        self.og_size = og_size
        self.radius = radius * self.quality
        self.fill = fill
        # to get better quality corners we will scale the
        # image up then shink it back down
        self.size = (
            self.og_size[0] *
            self.quality,
            self.og_size[1] *
            self.quality)
        self.width, self.height = self.size
        if shadow:
            self.image = self.round_rectangle()
        else:
            self.image = makeShadow(
                image=self.rounded_rectangle(),
                iterations=5,
                border=SHADING_QUALITY,
                ofset=(0, 6),
                backgroundColour=0xffffff,
                shadowColour=0x000000)

    def round_corner(self):
        """Draw a round corner"""
        corner = Image.new('RGBA', (self.radius, self.radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice(
            (0,
             0,
             self.radius *
             2,
             self.radius *
             2),
            180,
            270,
            fill=self.fill)
        corner.convert('RGBA')
        # corner.show()
        return corner

    def round_rectangle(self):
        """Draw a rounded rectangle"""

        rectangle = Image.new('RGBA', self.size)
        # ImageDraw.Draw.rectangle(size, (0,0,0,0))

        origCorner = self.round_corner()
        corner = origCorner
        rectangle.paste(corner, (0, 0))
        corner = origCorner.rotate(90)
        rectangle.paste(corner, (0, self.height - self.radius))
        corner = origCorner.rotate(180)
        rectangle.paste(
            corner,
            (self.width -
             self.radius,
             self.height -
             self.radius))
        corner = origCorner.rotate(270)
        rectangle.paste(corner, (self.width - self.radius, 0))

        dr = ImageDraw.Draw(rectangle)
        dl = ImageDraw.Draw(rectangle)
        dr.rectangle(
            ((self.width - self.radius, 0), ((self.radius), (self.height))), fill=self.fill)
        dl.rectangle(
            ((0, self.radius), ((self.width), (self.height - self.radius))), fill=self.fill)

        rectangle = rectangle.resize(self.og_size, resample=Image.LANCZOS)
        return rectangle

    def makeShadow(self,
                   image,
                   iterations,
                   border,
                   offset,
                   backgroundColour,
                   shadowColour):
        # image: base image to give a drop shadow
        # iterations: number of times to apply the blur filter to the shadow
        # border: border to give the image to leave space for the shadow
        # offset: offset of the shadow as [x,y]
        # backgroundCOlour: colour of the background
        # shadowColour: colour of the drop shadow

        # Calculate the size of the shadow's image
        fullWidth = image.size[0] + abs(offset[0]) + 2 * border
        fullHeight = image.size[1] + abs(offset[1]) + 2 * border

    # Create the shadow's image. Match the parent image's mode.
        shadow = Image.new(
            image.mode, (fullWidth, fullHeight), backgroundColour)

    # Place the shadow, with the required offset
    # if <0, push the rest of the image right
        shadowLeft = border + max(offset[0], 0)
    # if <0, push the rest of the image down
        shadowTop = border + max(offset[1], 0)
    # Paste in the constant colour
        shadow.paste(shadowColour,
                     [shadowLeft, shadowTop,
                      shadowLeft + image.size[0],
                      shadowTop + image.size[1]])

    # Apply the BLUR filter repeatedly
        for i in range(iterations):
            shadow = shadow.filter(ImageFilter.BLUR)

    # Paste the original image on top of the shadow
    # if the shadow offset was <0, push right
        imgLeft = border - min(offset[0], 0)
    # if the shadow offset was <0, push down
        imgTop = border - min(offset[1], 0)
        shadow.paste(image, (imgLeft, imgTop))

        return shadow

if __name__ == "__main__":
    from global_variables import COLORS
    img = rounded_rect((310, 60), 10, COLORS['PURPLE'], 10, shadow=True)
    print img.image.size
    img.image.show()
    print img.image.mode
    # print newIMG.verify()
    img.image.save('zzz.png')
