BASIC_VARIABLES = {
    "True": {"type": "const", "value": 1},
    "False": {"type": "const", "value": 0},
    "None": {"type": "const", "value": -1},
}

for key, val in BASIC_VARIABLES.items():
    val["ignore"] = True


class Namespace:
    def __init__(self, global_name, sub_name="", variables: dict = None, functions: dict = None):
        self.prefix = global_name
        self.global_name = global_name
        self.sub_name = sub_name
        if sub_name:
            self.prefix += f"_{sub_name}"
        if variables is None:
            self.variables = BASIC_VARIABLES.copy()
        else:
            self.variables = variables.copy()
        if functions is None:
            self.functions = {}
        else:
            self.functions = functions

    def getValue(self, name):
        if name not in self.variables:
            print(name)
            raise ValueError("Invalid variable name")
        return self.variables[name]

    def setValue(self, name, val_type):
        self.variables[name] = {"type": val_type, "value": f"{self.prefix}_{name}"}
        return self.variables[name]

    def setLocal(self, name):
        self.variables[name]["value"] = f"{self.prefix}_{name}"
        return self.variables[name]

    def setFunction(self, name, sub_process=""):
        prefix = f"{self.global_name}"
        if sub_process:
            prefix += f"_{sub_process}"
        self.functions[name] = f'{prefix}_{name.replace(".", "_")}'

    def getFunction(self, name):
        if name not in self.functions:
            raise ValueError("Function does not exists")
        return self.functions[name]

    def copy(self, sub_name):
        new_namespace = Namespace(self.prefix, sub_name=sub_name, variables=self.variables,
                                  functions=self.functions)
        return new_namespace
