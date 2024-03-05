import mclang.syntax.PrcParser as prc
from mclang import parser as pr
from mclang.namespace import Namespace

class Parser(prc.PrcParser):
    def __init__(self):
        self.name = None

    def getName(self):
        return "template"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()

        ns.setValue(block, "code_template")
        ns.getValue(block)['pointer'] = self
        ns.getValue(block)['value'] = data
        self.name = block

    def insert(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()
        parser: pr.CodeParser = meta["PARSER"]
        prc_list = parser.parse_prcs(ns.getValue(self.name)['value'])

        return prc_list