"""
Cool AST implementation
"""

class AST(object):
    """
    Base class for AST
    """
    def __init__(self):
        pass

    def __get_dict_printable(self):
        d = self.__dict__
        result = ""
        for att in d.keys():
            result += "%s -> %s\n" %(str(att),str(d[att]))
        return result

    def get_str(self, name):
        return name + "\n" + self.__get_dict_printable()

    def __str__(self):
        return self.get_str("AST")

    def __repr__(self):
        return self.__class__.__name__

class Object(AST): 
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.get_str("Object")

class Self(AST):
    def __init__(self):
        pass
    def __str__(self):
        return self.get_str("Self")

class SelfType(AST):
    def __init__(self):
        pass

class Program(AST):
    def __init__(self, classes):
        self.classes = classes
    
    def __repr__(self):
        return "Program"

class ClassList(AST):
    def __init__(self, classes):
        self.classes = classes
    
    def __repr__(self):
        return "ClassList"

class Parameter(AST):
    def __init__(self, name, p_type):
        self.name = name
        self.p_type = p_type
    
    def __str__(self):
        return self.get_str("Parameter")
#---------------------------Classes-----------------------------------------#

class Class(AST):
    def __init__(self, name, parent, feature_list):
        self.name = name
        self.parent = parent
        self.feature_list = feature_list
    
    def __repr__(self):
        return "class %s" %self.name

class ClassFeature(AST):
    def __init__(self,name, f_type):
        self.name = name
        self.f_type = f_type
    
    def __repr__(self):
        return "Class Feature %s" %self.name

class ClassMethod(ClassFeature):
    def __init__(self, name, params, return_type, body):
        super().__init__(name,return_type)
        self.params = params
        self.body = body
    
    def __str__(self):
        return self.get_str("ClassMethod")

class ClassAttribute(ClassFeature):
    def __init__(self, name, attribute_type, initializer_expr):
        super().__init__(name, attribute_type)
        self.name = name
        self.initializer_expr = initializer_expr
    
    def __str__(self):
        return self.get_str("ClassAtribute")

#---------------------------Expressions-------------------------------------#

class Expression(AST):
    def __init__(self):
        pass
    
    def __str__(self):
        return self.get_str("Expression")

class Assingment(Expression):  
    def __init__(self, object_inst, expr):
        self.object_inst = object_inst
        self.expr = expr
    
    def __str__(self):
        return self.get_str("Assigment")

class Block(Expression): 
    def __init__(self, expr_block):
        self.expr_block = expr_block
    
    def __str__(self):
        return self.get_str("Block")

class Let(Expression):
    def __init__(self, obj_inst, return_type, init_expr, body, nested_lets = None):
        self.obj_inst = obj_inst
        self.return_type = return_type
        self.init_expr = init_expr
        self.body = body
        self.nested_lets = nested_lets if nested_lets else []
     
    def __repr__(self):
        return "Let %s" %self.obj_inst

class New(Expression):
    def __init__(self, new_object_type):
        self.new_object_type = new_object_type
    
    def __str__(self):
        return self.get_str("New")

class IsVoid(Expression):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return self.get_str("IsVoid")

#########   Case  #########

class Case(Expression):
    def __init__(self, expr, actions):
        self.expr = expr
        self.actions = actions
    
    def __str__(self):
        return self.get_str("Case")

class Action(Expression):
    def __init__(self, r_object, r_type, expr):
        self.r_object = r_object
        self.r_type = r_type
        self.expr = expr
    
    def __str__(self):
        return self.get_str("Action")

#########   Operations  #########

class OperationExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return self.get_str("OperationExpression")

class Add(OperationExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("Add")

class Sub(OperationExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("Sub")

class Mul(OperationExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("Mul")

class Div(OperationExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("Div")

#########   Comparissons  #########

class ComparissonExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return self.get_str("ComparissonExpression")

class LessThan(ComparissonExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("LessThan")

class LessThanOrEqual(ComparissonExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("LessThanOrEqual")

class Equal(ComparissonExpression): 
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return self.get_str("Equal")

#########  Control Flow  #########

class ControlFlowExpression(Expression):
    def __init__(self, predicate):
        self.predicate = predicate
    
    def __str__(self):
        return self.get_str("ControlFlowExpression")

class If(ControlFlowExpression): 
    def __init__(self, predicate, then_body, else_body):
        super().__init__(predicate)
        self.then_body = then_body
        self.else_body = else_body
    
    def __str__(self):
        return self.get_str("If")

class WhileLoop(ControlFlowExpression): 
    def __init__(self, predicate, body):
        super().__init__(predicate)
        self.body = body
            
    def __str__(self):
        return self.get_str("WhileLoop")

#########   Complements  #########

class IntegerComplement(Expression):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return self.get_str("IntegerComplement")

class BooleanComplement(Expression):
    def __init__(self, expr):
        self.expr = expr
          
    def __str__(self):
        return self.get_str("BooleanComplement")

#---------------------------Constants---------------------------------------#

class Constant(Expression):
    def __init__(self,value):
        self.value = value
    
    def __str__(self):
        return self.get_str("Constant")

class Integer(Constant): 
    def __init__(self, value):
        super().__init__(value)
    
    def __str__(self):
        return self.get_str("Integer")

class Boolean(Constant): 
    def __init__(self, value):
        super().__init__(value)
    
    def __str__(self):
        return self.get_str("Boolean")

class String(Constant): 
    def __init__(self, value):
        super().__init__(value)
    
    def __str__(self):
        return self.get_str("String")

#---------------------------Methods Dispatchs--------------------------------#

class Dispatch(AST):
    def __init__(self, object_inst, method, params):
        self.object_inst = object_inst
        self.method = method
        self.params = params
    
    def __str__(self):
        return self.get_str("Dispatch")

class DynamicDispatch(Dispatch):  
    def __init__(self, object_inst, method, params):
        super().__init__(object_inst, method, params)
    
    def __str__(self):
        return self.get_str("DynamicDispatch")

class StaticDispatch(Dispatch):  
    def __init__(self, object_inst, obj_type, method, params):
        super().__init__(object_inst, method, params)
        self.obj_type = obj_type
    
    def __str__(self):
        return self.get_str("StaticDispatch")
