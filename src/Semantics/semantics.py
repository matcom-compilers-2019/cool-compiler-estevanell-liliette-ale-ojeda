"""
AST workplace
"""
import Utils.visitor as visitor
import Semantics.scope as s
import Utils.Cool.ast as ast

#returns True if all classes in the hierarchy are define and the hierarchy does not contain cycles
def hierarchy_its_ok(scope, errors):
    result = True
    for k in scope.types:
        if k != "Object" and scope.get_type(scope.types[k].parent.name) is not None:
            scope.types[k].parent = scope.get_type(scope.types[k].parent.name)
            if scope.types[k].parent.name == "String" or scope.types[k].parent.name =="Int" or scope.types[k].parent.name =="Bool":
                # print(scope.types[k].parent.name)
                errors.append("Is an error to inherit from {0}".format(scope.types[k].parent.name))
                result = False
        elif k != "Object":
            errors.append("class {0} is not define".format(scope.types[k].parent.name))
            scope.types[k].parent = None
            result = False
    if not scope.get_type("Main"):
        errors.append("Program not contains a Main class")
        result = False
    elif scope.get_type("Main").parent.name != "Object":
        errors.append("Main class not must have heir")
        result = False
    for typ in scope.types:
        tmp = []
        current_type = scope.types[typ]
        while current_type.parent is not None:
            if tmp.__contains__(current_type.parent.name):
                errors.append("The class hierarchy contains cycles")
                return False
            tmp.append(current_type.parent.name)
            current_type = current_type.parent
    return result
def add_basic_types(scope):
    scope.create_type("Object")
    # scope.create_type("SELF_TYPE", "Object")
    scope.create_type("Int", "Object")
    scope.create_type("String", "Object")
    scope.create_type("Bool", "Object")
    scope.create_type("IO", "Object")
    scope.create_type("Void", "Object")

    scope.get_type("Object").define_method("abort", scope.get_type("Object"))
    scope.get_type("Object").define_method("type_name", scope.get_type("String"))
    scope.get_type("Object").define_method("copy", scope.get_type("Object"))
    scope.get_type("String").define_method("length", scope.get_type("Int"))
    scope.get_type("String").define_method("concat", scope.get_type("String"), [("x", scope.get_type("String"))])
    scope.get_type("String").define_method("substr", scope.get_type("String"), [("x",scope.get_type("Int")), ("y",scope.get_type("Int"))])
    scope.get_type("IO").define_method("out_string", scope.get_type("String"),[("x", scope.get_type("String"))])
    scope.get_type("IO").define_method("out_int", scope.get_type("Int"),[("x", scope.get_type("Int"))])
    scope.get_type("IO").define_method("in_string", scope.get_type("String"))
    scope.get_type("IO").define_method("in_int", scope.get_type("Int"))


class Semantics:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.scope = s.Scope()
        add_basic_types(self.scope)

    def check_semantics(self):
        type_collector = TypeCollectorVisitor()
        type_collector.visit(self.ast, self.scope, self.errors)
        if not hierarchy_its_ok(self.scope, self.errors) or len(self.errors) != 0:
            return False
        type_builder = TypeBuilderVisitor()
        type_builder.visit(self.ast, self.scope, self.errors)
        if not self.scope.types["Main"].get_method("main"):
            self.errors.append("Main class no contains a method main")
        elif len(self.scope.types["Main"].get_method("main").arguments) != 0:
            self.errors.append("method main not must have arguments")
        if len(self.errors) != 0:
            return False
        type_checker = TypeCheckerVisitor()
        type_checker.visit(self.ast, self.scope, self.errors)
        if len(self.errors) != 0:
            return False
        return True



class TypeCollectorVisitor:

    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

    @visitor.when(ast.Program)
    def visit(self, node, scope, errors):
        for class_def in node.classes:
            if not scope.get_type(class_def.name):
                self.visit(class_def,scope, errors)
            else:
                errors.append("class {0} alredy exists".format(class_def.name))

    @visitor.when(ast.Class)
    def visit(self, node, scope, errors):
        scope.create_type(node.name, node.parent)

class TypeBuilderVisitor:

    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

    @visitor.when(ast.Program)
    def visit(self, node, scope, errors):
        for class_def in node.classes:
            self.visit(class_def, scope, errors)

    @visitor.when(ast.Class)
    def visit(self, node, scope, errors):
        scope.current_type = scope.get_type(node.name)
        for feature_def in node.feature_list:
            self.visit(feature_def, scope, errors)

    @visitor.when(ast.ClassAttribute)
    def visit(self, node, scope, errors):
        attr_type = scope.get_type(node.f_type)
        if not attr_type:
            errors.append("Type {0} is not defined".format(node.f_type))
        if scope.current_type.get_attribute(node.name):
            errors.append("attribute {0} alredy exists".format(node.name))
        elif attr_type:
            scope.current_type.define_attribute(node.name, attr_type)
        node.variable = scope.current_type.define_variable(node.name, scope.get_type(node.f_type), True)
        
    @visitor.when(ast.ClassMethod)
    def visit(self, node, scope, errors):
        ok = True
        return_type = scope.get_type(node.f_type)
        if return_type is None:
            errors.append("Type {0} is not defined".format(node.f_type))
            ok = False
        for param in node.params:
            if not scope.get_type(param.p_type):
                errors.append("Type {0} is not defined".format(param.p_type))
                ok = False
        if not scope.current_type.methods.__contains__(node.name):
            method = scope.current_type.get_method(node.name)
            if ok and method:
                if method.return_type.name != return_type.name:
                    errors.append("method {0} alredy exists".format(method.name))
                    return
                if len(node.params) != len(method.arguments):
                    errors.append("method {0} alredy exists".format(method.name))
                    return
                for i in range(len(node.params)):
                    if method.arguments[i].type.name != node.params[i].p_type:
                        errors.append("method {0} alredy exists".format(method.name))
                        return
                if scope.current_type.conform(scope.get_type("IO")) and scope.get_type("IO").methods.__contains__(node.name):
                    errors.append("It is invalid to redefine the inherite methods of IO")
                    return
            if ok:
                args = [(node.params[i].name, scope.get_type(node.params[i].p_type)) for i in range(len(node.params))]
                scope.current_type.define_method(node.name, return_type, args)
        else:
            errors.append("method named {0} alredy exists".format(node.name))
        
class TypeCheckerVisitor:

    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

    @visitor.when(ast.Program)
    def visit(self, node, scope, errors):
        for class_def in node.classes:
            child_scope = scope.create_child_scope(True)
            var = child_scope.define_variable("self", scope.get_type(class_def.name))
            scope.get_type(class_def.name).variables["self"] = var
            class_def.variable = var
            child_scope.current_type = scope.get_type(class_def.name)
            self.visit(class_def, child_scope, errors)
            
    @visitor.when(ast.Class)
    def visit(self, node, scope, errors):
        for feature_def in node.feature_list:
            self.visit(feature_def, scope, errors)

    @visitor.when(ast.ClassAttribute)
    def visit(self, node, scope, errors):
        if node.initializer_expr:
            self.visit(node.initializer_expr, scope, errors)
            init_expr_type = node.initializer_expr.computed_type
            if init_expr_type:
                if not init_expr_type.conform(scope.get_type(node.f_type)):
                    errors.append("Type {0} not conform to type {1}".format(init_expr_type.name, node.f_type))
                    return

    @visitor.when(ast.ClassMethod)
    def visit(self, node, scope, errors):
        child_scope = scope.create_child_scope()
        node.variable = child_scope.get_variable("self")
        for arg in node.params:
            self.visit(arg, child_scope, errors)
            if not arg.variable:
                errors.append("The parameters not may have the same name")
                return
        self.visit(node.body, child_scope, errors)
        body_type = node.body.computed_type
        if body_type:
            if not body_type.conform(child_scope.get_type(node.f_type)):
                errors.append("Type {0} not conform to type {1}".format(body_type.name, node.f_type))
        #     node.computed_type = None
        # else:
        #     node.computed_type = scope.get_type(node.f_type)

    @visitor.when(ast.Object)
    def visit(self, node, scope, errors):
        var = scope.get_variable(node.name)
        if not var:
            var = scope.current_type.get_variable(node.name)
            if not var:
                errors.append("variable {0} is not define".format(node.name))
                node.computed_type = None
                return
        node.computed_type = var.type_var
        node.variable = var

    @visitor.when(ast.Self)
    def visit(self, node, scope, errors):
        node.variable = scope.get_variable("self")
        node.computed_type = node.variable.type_var

    @visitor.when(ast.Parameter)
    def visit(self, node, scope, errors):
        node.variable = scope.define_variable(node.name, scope.get_type(node.p_type))


    #########   Operations  #########
        
    @visitor.when(ast.OperationExpression)
    def visit(self, node, scope, errors):
        self.visit(node.left, scope, errors)
        self.visit(node.right, scope, errors)
        if node.left.computed_type and node.right.computed_type: 
            if node.left.computed_type.name != "Int" or node.right.computed_type.name != "Int":
                errors.append("The static types of the two sub-expressions of arithmetic operator must be Int")
                node.computed_type = None
            else:
                node.computed_type = node.left.computed_type
        else:
            node.computed_type = None

#---------------------------Expressions-------------------------------------#

    @visitor.when(ast.Assingment)
    def visit(self, node, scope, errors):
        self.visit(node.object_inst, scope, errors)
        v_type = node.object_inst.computed_type
        self.visit(node.expr, scope, errors)
        if v_type and node.expr.computed_type:
            if not node.expr.computed_type.conform(v_type):
                errors.append("Type {0} not conform with type {1}".format(node.expr.computed_type.name, v_type.name))
            else:
                node.computed_type = node.expr.computed_type
                return
        node.computed_type = None

    @visitor.when(ast.Block)
    def visit(self, node, scope, errors):
        b_type = None
        for expr in node.expr_block:
            self.visit(expr, scope, errors)
            b_type = expr.computed_type
        node.computed_type = b_type
        
    @visitor.when(ast.Let)
    def visit(self, node, scope, errors):
        child_scope = scope.create_child_scope()
        return_type = scope.get_type(node.return_type)
        if not return_type:
            errors.append("Type {0} not exists".format(node.return_type))
            node.computed_type = None
            return
        if node.init_expr:
            self.visit(node.init_expr, scope, errors)
            if node.init_expr.computed_type:
                if not node.init_expr.computed_type.conform(return_type):
                    errors.append("Type {0} not conform with type {1}".format(node.init_expr.computed_type.name, return_type.name))
                else:
                    node.variable = child_scope.define_variable(node.obj_inst, return_type)     
            else:
                node.computed_type = None
                return
        if node.nested_lets:
            for let in node.nested_lets:
                self.visit(let, child_scope, errors)
        current_scope = child_scope
        while len(current_scope.children) != 0:
            current_scope = current_scope.children[0]
        if node.body:
            self.visit(node.body, current_scope, errors)
            node.computed_type = node.body.computed_type

    @visitor.when(ast.New)
    def visit(self, node, scope, errors):
        new_object_type = scope.get_type(node.new_object_type)
        if not new_object_type:
            errors.append("Type {0} is not define".format(node.new_object_type))
        node.computed_type = new_object_type

    @visitor.when(ast.IsVoid)
    def visit(self, node, scope, errors):
        self.visit(node.expr, scope, errors)
        node.computed_type = scope.get_type("Bool")

    ########Constants########

    @visitor.when(ast.Integer)
    def visit(self, node, scope, errors):
        node.computed_type = scope.get_type("Int")

    @visitor.when(ast.Boolean)
    def visit(self, node, scope, errors):
        node.computed_type = scope.get_type("Bool")

    @visitor.when(ast.String)
    def visit(self, node, scope, errors):
        node.computed_type = scope.get_type("String")

    ################### Complements ##################

    @visitor.when(ast.IntegerComplement)
    def visit(self, node, scope, errors):
        self.visit(node.expr, scope, errors)
        if node.expr.computed_type:
            if node.expr.computed_type.name != "Int":
                errors.append("The expression must have static type Int")
                node.computed_type = None
            else:
                node.computed_type = scope.get_type("Int")
        else:
            node.computed_type = None

    @visitor.when(ast.BooleanComplement)
    def visit(self, node, scope, errors):
        self.visit(node.expr, scope, errors)
        if node.expr.computed_type:
            if node.expr.computed_type.name != "Bool":
                errors.append("The expression must have static type Bool")
                node.computed_type = None
            else:
                node.computed_type = scope.get_type("Bool")
        else:
            node.computed_type = None

    ################ Control Flow ###################

    @visitor.when(ast.If)
    def visit(self, node, scope, errors):
        self.visit(node.predicate, scope, errors)
        self.visit(node.then_body, scope, errors)
        self.visit(node.else_body, scope, errors)
        
        if node.then_body.computed_type and node.else_body.computed_type:
            node.computed_type = node.then_body.computed_type.least_type(node.else_body.computed_type)
        else:
            node.computed_type = None
        if node.predicate.computed_type:
            if node.predicate.computed_type.name != "Bool":
                errors.append("predicate's type must be Bool")
                node.computed_type = None
        else:
            node.computed_type = None
        
    @visitor.when(ast.WhileLoop)
    def visit(self, node, scope, errors):
        self.visit(node.predicate, scope, errors)
        self.visit(node.body, scope, errors)
        if node.predicate.computed_type:
            if node.predicate.computed_type.name != "Bool":
                errors.append("predicate's type must be Bool")
                node.computed_type = None
        else:
            node.computed_type = None
        node.computed_type = scope.get_type("Object")

    #########   Comparissons  #########
    @visitor.when(ast.Equal)
    def visit(self, node, scope, errors):
        self.visit(node.left, scope, errors)
        self.visit(node.right, scope, errors)
        if node.left.computed_type and node.right.computed_type:
            if node.left.computed_type.name != node.right.computed_type.name:
                errors.append("The static types of the two sub-expressions of comparissons must be same type")
                node.computed_type = None
            else:
                node.computed_type = scope.get_type("Bool")
        else:
            node.computed_type = None

    @visitor.when(ast.ComparissonExpression)
    def visit(self, node, scope, errors):
        self.visit(node.left, scope, errors)
        self.visit(node.right, scope, errors)
        if node.left.computed_type and node.right.computed_type: 
            if node.left.computed_type.name != "Int" or node.right.computed_type.name != "Int":
                errors.append("The static types of the two sub-expressions of comparissons must be Int")
                node.computed_type = None
            else:
                node.computed_type = scope.get_type("Bool")
        else:
            node.computed_type = None

    #---------------------------Methods Dispatchs--------------------------------#

    @visitor.when(ast.DynamicDispatch)
    def visit(self, node, scope, errors):
        self.visit(node.object_inst, scope, errors)
        obj_type = node.object_inst.computed_type
        if obj_type:  
            method = obj_type.get_method(node.method)
            if method:
                if len(method.arguments) == len(node.params):
                    for i in range(len(node.params)):
                        self.visit(node.params[i], scope, errors)
                        param_type = node.params[i].computed_type
                        if param_type:
                            if not param_type.conform(method.arguments[i].type):
                                errors.append("method {0} is not defined".format(node.method))
                                node.computed_type = None
                                return
                    node.computed_type = method.return_type
                    return 
            errors.append("method {0} is not defined".format(node.method))
        node.computed_type = None

    @visitor.when(ast.StaticDispatch)
    def visit(self, node, scope, errors):
        self.visit(node.object_inst, scope, errors)
        obj_type = scope.get_type(node.obj_type)
        if not node.object_inst.computed_type or not obj_type:
            node.computed_type = None
            if not obj_type:
                errors.append("class {0} is not define".format(obj_type))
            return
        if not node.object_inst.computed_type.conform(obj_type):
            errors.append("Type {0} not conform with type {1}".format(node.object_inst.computed_type.name, node.obj_type))
            node.computed_type = None
            return
        method = obj_type.get_method(node.method)
        if method:
            if len(method.arguments) == len(node.params):
                for i in range(len(node.params)):
                    self.visit(node.params[i], scope, errors)
                    param_type = node.params[i].computed_type
                    if param_type:
                        if not param_type.conform(method.arguments[i].type):
                            errors.append("method {0} is not define in class {1}".format(node.method,node.obj_type))
                            node.computed_type = None
                            return
                node.computed_type = method.return_type
                return
        errors.append("method {0} is not define in class {1}".format(node.method,node.obj_type))
        node.computed_type = None

#---------------------------Case---------------------------#

    @visitor.when(ast.Case)
    def visit(self, node, scope, errors):
        self.visit(node.expr,scope, errors)
        if not node.expr.computed_type:
            errors.append("Invalid Expression in Case")
        expr_types = []
        for action in node.actions:
            child_scope = scope.create_child_scope()
            r_type = scope.get_type(action.r_type)
            if not r_type:
                errors.append("class {0} is not define".format(action.r_type))
                node.computed_type = None
                return
            action.variable = child_scope.define_variable(action.r_object, r_type)
            self.visit(action.expr,child_scope, errors)
            expr_type = action.expr.computed_type
            if expr_type:
                expr_types.append(expr_type)
            else:
                node.computed_type = None
                return
        if len(expr_types) == 1:
            node.computed_type = expr_types[0]
            return
        least_type = expr_types[0].least_type(expr_types[1])
        for i in range(2,len(expr_types)):
            least_type = least_type.least_type(expr_types[i])
        node.computed_type = least_type
                

            

        






        

    
    