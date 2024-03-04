import mclang.syntax.PrcParser as prc
from mclang import parser
from mclang.namespace import Namespace
from PIL import Image


def getImageData(sx, sy, block_size, image_path):
    with Image.open(image_path) as img:
        img = img.resize((int(sx / block_size), int(sy / block_size)))
        img = img.convert("RGBA")

        data = []

        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))

                if len(pixel) == 4 and pixel[3] == 0:
                    continue

                scaled_x = x * (sx / img.width)
                scaled_y = y * (sy / img.height)

                scaled_x = round(scaled_x, 5)
                scaled_y = 1 - round(scaled_y, 5)

                scaled_x -= sx / 2
                scaled_y += sy / 2

                rgb = [round(c / 255.0, 5) for c in pixel[:3]]

                data.append((scaled_x, scaled_y, rgb))

        return data


class Parser(prc.PrcParser):
    def __init__(self):
        self.imagePath = None

    def getName(self):
        return "image"

    def show(self, args: list, meta):
        cmds = []
        sx = float(args[0])
        sy = float(args[1])
        size = float(args[2])
        psize = float(args[3])
        selector = "@a"
        if len(args) > 4:
            selector = args[4]
        data = getImageData(sx, sy, psize, self.imagePath)
        for dat in data:
            cmds.append(
                f"particle minecraft:dust {dat[2][0]} {dat[2][1]} {dat[2][2]} {size} ^{dat[0]} ^{dat[1]} ^ 0 0 0 0 1 force {selector}")
        res = []
        for cmd in cmds:
            res.append({
                "type": "command",
                "value": cmd
            })
        return res

    def parse(self, block, meta, base=None, data=None):
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()
        varname, path = [x.strip() for x in block.split("=")]
        self.imagePath = eval(path)

        ns.setValue(varname, "image")
        ns.getValue(varname)["pointer"] = self
