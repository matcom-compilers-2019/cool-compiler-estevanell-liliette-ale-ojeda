
class Type:
    def __init__(self, name, parent = None, attributes = None, methods = None):
        self.name = name
        self.parent = parent
        self.attributes = {} if not attributes else attributes
        self.methods = {} if not methods else methods
        self.variables = {}

    def define_variable(self, name, type_var, attr = False):
        if not self.variables.__contains__(name):
            new_variable = Variable(name, type_var, attr)
            self.variables[name] = new_variable
            return new_variable
        return None

    def get_variable(self, name_var):
        if self.variables.__contains__(name_var):
            return self.variables[name_var]
        tmp = self
        while tmp.parent:
            if tmp.parent.variables.__contains__(name_var):
                return tmp.parent.variables[name_var]
            tmp = tmp.parent
        # if tmp.current_type.attributes.__contains__(name_var):
        #     return tmp.current_type.attributes[name_var].type
        return None

    def get_attribute(self, name):
        if self.attributes.__contains__(name):
            return self.attributes[name]
        parent = self
        while parent:
            if parent.attributes.__contains__(name):
                return parent.attributes[name]
            parent = parent.parent
        return None

    def get_method(self, name):
        if self.methods.__contains__(name):
            return self.methods[name]
        parent = self
        while parent:
            if parent.methods.__contains__(name):
                return parent.methods[name]
            parent = parent.parent
        return None

    def define_attribute(self, name, type):
        if not self.attributes.__contains__(name):
            new_attr = Attribute(name, type)
            self.attributes[name] = new_attr
            return True
        return False

    def define_method(self, name, return_type, arguments = None):
        arguments = [] if not arguments else arguments
        if not self.methods.__contains__(name):
            args = [Attribute(arguments[i][0],arguments[i][1]) for i in range(len(arguments))]
            new_method = Method(name, return_type, args)
            self.methods[name] = new_method
            return True
        return False

    def conform(self, other_type):
        if not other_type:
            return False
        parent = self
        while parent:
            if parent.name == other_type.name:
                return True
            parent = parent.parent
        return False

    def least_type(self, other_type):
        if not other_type:
            return False
        parent = self
        while parent:
            if other_type.conform(parent):
                return parent
            parent = parent.parent
        return None


class Attribute:
    def __init__(self, name, attr_type):
        self.name = name
        self.type = attr_type

class Method:
    def __init__(self, name, return_type, arguments = None):
        self.name = name
        self.return_type = return_type
        self.arguments = [] if not arguments else arguments

class Variable:
    am = 0
    def __init__(self, name, type_var, attribute):
        self.name = name
        self.type_var = type_var
        self.attribute = attribute
        self.am = Variable.am
        Variable.am += 1
    def __repr__(self):
        return f"{self.name}_{self.am} "

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.types = {}
        self.current_type = None
        self.variables = {}
        self.children = []

    def get_type(self, type_name):
        if self.types.__contains__(type_name):
            return self.types[type_name]
        parent = self
        while parent:
            if parent.types.__contains__(type_name):
                return parent.types[type_name]
            parent = parent.parent
        return None

    def get_variable(self, name_var):
        if self.variables.__contains__(name_var):
            return self.variables[name_var]
        tmp = self
        while tmp.parent:
            if tmp.parent.variables.__contains__(name_var):
                return tmp.parent.variables[name_var]
            tmp = tmp.parent
        # if tmp.current_type.attributes.__contains__(name_var):
        #     return tmp.current_type.attributes[name_var].type
        return None

    def create_child_scope(self, first=False):
        child_scope = Scope(parent = self)
        if not first:
        # child_scope.define_variable("self", self.current_type)
            child_scope.current_type = self.current_type
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, name, type_var, attr = False):
        if not self.variables.__contains__(name):
            new_variable = Variable(name, type_var, attr)
            self.variables[name] = new_variable
            return new_variable
        return None

    def create_type(self, name, parent_name= "", attributes = None, methods = None):
        parent = Type(parent_name)
        new_type = Type(name, parent, attributes, methods)
        self.types[name] = new_type
        return new_type

