BASIC_VARIABLES = {
    "True": 1,
    "False": 0
}


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

    def setValue(self, name):
        self.variables[name] = f"{self.prefix}{name}"
        return self.variables[name]

    def setLocal(self, name):
        self.variables[name] = f"{self.prefix}{name}"
        return self.variables[name]

    def setFunction(self, name, sub_process=""):
        prefix = f"{self.global_name}_"
        if sub_process:
            prefix += f"{sub_process}_"
        self.functions[name] = f"{prefix}{name}"

    def getFunction(self, name):
        if name not in self.functions:
            raise ValueError("Function does not exists")
        return self.functions[name]

    def copy(self, sub_name):
        new_namespace = Namespace(self.global_name, sub_name=sub_name, variables=self.variables,
                                  functions=self.functions)
        return new_namespace
