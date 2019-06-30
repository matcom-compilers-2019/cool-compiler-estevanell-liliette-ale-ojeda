"""
CIL AST implementation
"""

class CILNode:
    """Base class for  ast CILNode"""
    pass
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return self.__class__.__name__

class ProgramNode(CILNode):
    def __init__(self, types_section, data_section, code_section):
        self.types_section = types_section
        self.data_section = data_section
        self.code_section = code_section

#------------------------------ TYPES ------------------------------------------#
class ParentTypeNode(CILNode):
    def __init__(self, dest, type_obj):
        self.dest = dest
        self.type_obj = type_obj
    def __repr__(self):
        return f"{self.dest} = Parent({self.type_obj})"

class TypeNode(CILNode):
    def __init__(self, name, attributes, type_functions, constructor, parent):
        self.name = name
        self.attributes = attributes
        self.type_functions = type_functions
        self.constructor = constructor
        self.parent = parent
    def __repr__(self):
        return f"Type {self.name}"

class AttributeNode(CILNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"attribute {self.name}"

class TypeFunctionNode(CILNode):
    def __init__(self, name, function):
            self.name = name
            self.function = function
    def __repr__(self):
        return f"function {self.name}:{self.function.name}"

class DataNode(CILNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f'{self.name} = "{self.value}"'

class StringNode(CILNode):
    def __init__(self, value, data):
        self.value = value
        self.data = data

class IntegerNode(CILNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Integer {self.value}"

class FunctionNode(CILNode):
    def __init__(self, name, params, localvars, instructions):
        self.name = name
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
    def __repr__(self):
        return "Function %s" %self.name

class ParamNode(CILNode):
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return f"Param {self.obj}"

class LocalNode(CILNode):
    def __init__(self, variable):
        self.variable = variable
    def __repr__(self):
        return "LOCAL %s" %self.variable

#------------------------------ INSTRUCTIONS ------------------------------------------#

class InstructionNode(CILNode):
    def __init__(self, dest, first_op, second_op ):
        self.dest = dest
        self.first_op = first_op
        self.second_op = second_op
    def __str__(self):
        return self.__repr__()

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        super().__init__(dest, source, None)
    def __repr__(self):
        return f"{str(self.dest)} = {str(self.first_op)}"

############## ARITHMETIC INSTRUCTIONS Nodes ##################

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class PlusNode(ArithmeticNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)
    def __repr__(self):
        return f"{str(self.dest)} = {str(self.first_op)} + {str(self.second_op)}"

class MinusNode(ArithmeticNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)
    def __repr__(self):
        return f"{str(self.dest)} = {str(self.first_op)} - {str(self.second_op)}"

class MultNode(ArithmeticNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)
    def __repr__(self):
        return f"{str(self.dest)} = {str(self.first_op)} * {str(self.second_op)}"

class DivNode(ArithmeticNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)
    def __repr__(self):
        return f"{str(self.dest)} = {str(self.first_op)} / {str(self.second_op)}"

############## ATTRIBUTES INSTRUCTIONS Nodes ##################

class GetAttribNode(InstructionNode):
    def __init__(self, dest, instance, attribute):
        super().__init__(dest, instance, attribute)
    def __repr__(self):
        return f"{self.dest} = GetAtribute {self.first_op} {self.second_op}"

class SetAttribNode(InstructionNode):
    def __init__(self, instance, attribute, value):
        super().__init__(instance, attribute, value)
    def __repr__(self):
        return f"SetAtribute {self.dest} {self.first_op} {self.second_op}"

############## CHAIN INSTRUCTIONS Nodes ##################

class GetIndexNode(InstructionNode):
    def __init__(self, dest, indexable_obj, index):
        super().__init__(dest, indexable_obj, index)

class SetIndexNode(InstructionNode):
    def __init__(self, indexable_obj, index, value):
        super().__init__(indexable_obj, index, value)

############## FUNCTION INSTRUCTION Nodes ##################

class AllocateNode(InstructionNode):
    def __init__(self, dest, obj_type):
        super().__init__(dest, obj_type, None)
    def __repr__(self):
        return f"{self.dest} = ALLOC {self.first_op}"

class ArrayNode(InstructionNode):
    def __init__(self, dest, Length):
        super().__init__(dest, Length, None)

class TypeOfNode(InstructionNode):
    def __init__(self, dest, obj):
        super().__init__(dest, obj, None)
    def __repr__(self):
        return f"{self.dest} = TypeOf {self.first_op}"

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"LABEL {self.name}"

class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label
    def __repr__(self):
        return f"GOTO {self.label}"

class GotoIfNode(InstructionNode):
    def __init__(self, label, condition):
        self.label = label
        self.condition = condition
    def __repr__(self):
        return f"IF {self.condition} GOTO {self.label}"

class CallNode(InstructionNode):
    def __init__(self, dest, function):
        super().__init__(dest, function, None)

class VCallNode(InstructionNode):
    def __init__(self, dest, obj_type, function, ctor = False):
        self.dest = dest
        self.obj_type = obj_type
        self.function = function
        self.ctor = ctor
    def __repr__(self):
        return f"{self.dest} = VCALL {self.obj_type} {self.function}"

class ArgNode(InstructionNode):
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
    def __repr__(self):
        return f"argument {self.name}"

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value
    def __repr__(self):
        return f"RETURN {self.value}"
#-------------------------- BASIC TYPES Nodes ----------------------------------

############## STRING ##################

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class LengthNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj
    def __repr__(self):
        return f"{self.dest} = length({self.obj})"

class ConcatNode(InstructionNode):
    def __init__(self, dest, string1, string2):
        self.dest = dest
        self.string1 = string1
        self.string2 = string2
    def __repr__(self):
        return f"{self.dest} = concat({self.string1},{self.string2})"

class PrefixNode(InstructionNode):
    def __init__(self, dest, msg1, msg2):
        self.dest = dest
        self.msg1 = msg1
        self.msg2 = msg2
    
class SubstringNode(InstructionNode):
    def __init__(self, dest, msg, init, end):
        self.dest = dest
        self.msg = msg
        self.init = init
        self.end = end
    def __repr__(self):
        return f"{self.dest} = substr({self.init},{self.end})"

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class EqualStringNode(InstructionNode):
    def __init__(self, dest, string1, string2):
        self.dest = dest
        self.string1 = string1
        self.string2 = string2

############## Object ##################

class IsTypeNode(CILNode):
    def __init__(self, dest, type_obj, type_name):
        self.dest = dest
        self.type_obj = type_obj
        self.type_name = type_name
    def __repr__(self):
        return f"{self.dest} = IsType({self.type_obj},{self.type_name})"

class TypeNameNode(CILNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj
    def __repr__(self):
        return f"{self.dest} = type_name({self.obj})"

class CopyNode(CILNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj
    def __repr__(self):
        return f"{self.dest} = copy({self.obj})"

class AbortNode(CILNode):
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return f"{self.obj}.abort({self.error_message})"

############## IO ##################

class OutStringNode(CILNode):
    def __init__(self, source):
        self.source = source

class InStringNode(CILNode):
    def __init__(self, dest):
        self.dest = dest

class OutIntNode(CILNode):
    def __init__(self, source):
        self.source = source

class InIntNode(CILNode):
    def __init__(self, dest):
        self.dest = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

############## IO ##################

class IsVoidNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj
    def __repr__(self):
        return f"{self.dest} = IsVoid({self.obj})"

############## Comparisson Nodes ##################

class LessThanNode(InstructionNode):
    def __init__(self, dest, first, second):
        super().__init__(dest, first, second)
    def __repr__(self):
        return f"{self.dest} = {self.first_op} < {self.second_op}"

class LessThanOrEqualNode(InstructionNode):
    def __init__(self, dest, first, second):
        super().__init__(dest, first, second)
    def __repr__(self):
        return f"{self.dest} = {self.first_op} <= {self.second_op}"

class EqualNode(InstructionNode):
    def __init__(self, dest, first, second):
        super().__init__(dest, first, second)
    def __repr__(self):
        return f"{self.dest} = {self.first_op} = {self.second_op}"