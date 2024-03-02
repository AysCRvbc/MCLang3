import mclang.syntax.PrcParser as prc
from mclang import parser
from mclang.namespace import Namespace


class Parser(prc.PrcParser):
    def __init__(self):
        self.imagePath = None

    def getName(self):
        return "image"

    def show(self, args: list, meta):
        pass

    def parse(self, block, meta, base=None, data=None):
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()
        varname, path = [x.strip() for x in block.split("=")]
        self.imagePath = eval(path)
        
        ns.setValue(varname, "image")
        ns.getValue(varname)["pointer"] = self

    def getImageData(self, sx, sy, block_size, image_path):
        pass