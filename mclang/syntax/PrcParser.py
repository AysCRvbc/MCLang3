levels = {}


class PrcParser:
    def process(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        process = nmeta.process
        if nmeta.namespace:
            if process not in levels:
                levels[process] = 0
            levels[process] += 1
            nmeta.level = list(levels).index(process)
            nmeta.index = levels[process]

        res = self.parse(block, meta, base=base, data=data)
        nmeta.prevBlock = self
        return res

    def parse(self, block, meta, base=None, data=None):
        pass

    def getName(self):
        raise Exception
