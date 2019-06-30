import Utils.visitor as visit
import Utils.Cool.ast as ast
import Utils.CIL.ast as cil
import Semantics.scope as scope

class Function:
    """
    Function scope representation for CIL
    """
    def __init__(self, name = None, ctor = False):
        self.name = name if name else "f"
        self.internal_count = 0
        self.localvars = []
        self.instructions = []
        self.params_references = {}
        self.parameters = []
        self.vars_references = {}
        self.self_instance = None
        self.tempvar = None

    def __repr__(self):
        return f"Function {self.name}"
    declared = []
    declared_am = 0

    @staticmethod
    def reset_declared():
        Function.declared = []
    def build(self):
        return cil.FunctionNode(self.name, 
                                self.parameters, 
                                self.localvars, 
                                self.instructions)
    def build_internal_vname(self, vname):
        """
        Creates a new internal name for a new variable, assuring uniqueness
        """
        vname = f'{self.name}_{self.internal_count}_{vname}'
        self.internal_count +=1
        return vname
    def register(self):
        new_function = self.build()
        Function.declared.append(new_function)
        return new_function
    def register_type_atribute(self, attr):
        self.vars_references[attr.name] = attr
    def register_local(self, variable):
        local_node = variable
        if local_node in self.localvars or local_node in self.parameters:
            return variable
        self.localvars.append(local_node)
        return variable
    def register_arg(self, variable):
        param = variable
        self.parameters += [param]
        self.params_references[param.name] = param
        return param
    def register_instruction(self, instruction_type, *args):
        instruction = instruction_type(*args)
        self.instructions.append(instruction)
        return instruction
    def get_object_if_exist(self, name:str):
        if name in self.vars_references.keys():
            return self.vars_references[name]
        return None
    def register_label(self, label):
        self.instructions.append(label)

class Type:
    """
    Type scope representation for CIL
    """
    def __init__(self,name):
        self.name = name
        self.attributes = []
        self.functions = []
        self.pending = []
        self.attr_references = {}
        self.functions_index = {}
        self.constructor = None
        self.parent = None
    def __repr__(self):
        return f"Type {self.name}"
    declared = []

    @staticmethod
    def reset_declared():
        Type.declared = []
    def inherit(self, inherited_type):
        self.parent = inherited_type
        for func in inherited_type.type_functions:
            self.functions_index[func.name] = len(self.functions)
            self.functions.append(func)
    def build(self):
        new_type = cil.TypeNode(self.name,
                                self.attributes,
                                self.functions,
                                self.constructor,
                                self.parent)
        return new_type
    def start_constructor(self, self_var = None):
        self.constructor =  Function(f"ctor_{self.name}",ctor=True)
        if not self_var:
            arg = self.constructor.register_arg(scope.Variable("self", None, False))
        else:
            arg = self.constructor.register_arg(self_var)
        self.constructor.self_instance = arg
        return arg
    def close_constructor(self):
        self.constructor.register_instruction(cil.ReturnNode)
        self.constructor = self.constructor.register()
        return self.constructor
    def register(self):
        # attrs = [cil.AttributeNode(attr.name) for attr in self.attributes]
        # new_type = cil.TypeNode(self.name, self.attributes, self.functions, self.constructor)
        new_type = self.build()
        Type.declared.append(new_type)
        return new_type
    def register_attribute(self, attr):
        self.attributes += [cil.AttributeNode(attr)]
        value = len(self.attributes) - 1
        self.attr_references[attr.name] = value
        return value
    def register_function(self, name, func:cil.FunctionNode, ctor = False):
        """
        Register a function as a FunctionNode into self type as a TypeFunctionNode.\n
        >>> `params`\n
        `name`: name of the function in the type\n
        `func`: FunctionNode to register\n
        `ctor`: determines wether or not name will be modified (True equals no mod).
        """
        nfunc = cil.TypeFunctionNode(name, func)
        if name in self.functions_index.keys():
            self.functions[self.functions_index[name]] = nfunc
        else:
            self.functions_index[name] = len(self.functions)
            self.functions.append(nfunc)

class CilGenerator:
    def __init__(self,program:ast.Program):
        #references for types and functions
        # {type.name:type}
        # {function.name:[function]}
        self.types_references = {}
        self.function_references = {}
        self.all_functions_names_by_types = {}

        #initialize declared functions set
        Function.reset_declared() 
        self.cfunction = None

        #initialize declared types set
        Type.reset_declared() 
        self.ctype = None

        #initialize utils
        self.labels_count = 0
        self.attrs = {}
        self.special_attrs = {}
        self.program = program

        #initialize output sets
        self.dotdata = []
        self.dottype = Type.declared
        self.dotcode = Function.declared

        self.create_basics_types()
    def __repr__(self):
        return self.__class__.__name__

    #######################################################
    #          UTILS            ###########################
    #######################################################

    def call_constructor(self, instance, inst_type):
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.ParamNode, instance)
        self.cfunction.register_instruction(cil.VCallNode, var, inst_type.name, inst_type.constructor.name, True)
        return var
    def create_basics_types(self):
        """
        register basics types into dottype.\n
        created:\n
        `Object` type\n
        `Int` type\n
        `String` type\n
        `Bool` type\n
        `Void` type\n
        """
        #Void type definition
        self.ctype = Type("Void")
        self.ctype.start_constructor()
        self.ctype.close_constructor()
        void = self.register_type()
        #Ending Void type definition

        #Object type definition
        self.ctype = Type("Object")
        self.attrs["Object"] = []
        self.all_functions_names_by_types["Object"] = {}
        self.ctype.inherit(void)
        self.ctype.start_constructor()
        self.ctype.close_constructor()

        #function type_name(self)
        f_name = F"type_name_{Function.declared_am}"
        self.all_functions_names_by_types["Object"]["type_name"] = F"type_name_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.TypeNameNode, var, arg)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("type_name")

        #function copy(self)
        f_name = F"copy_{Function.declared_am}"
        self.all_functions_names_by_types["Object"]["copy"] = F"copy_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.CopyNode, var, arg)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("copy")

        #function abort(self)
        f_name = F"abort_{Function.declared_am}"
        self.all_functions_names_by_types["Object"]["abort"] = F"abort_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        self.cfunction.register_instruction(cil.AbortNode, arg)
        self.cfunction.register_instruction(cil.ReturnNode)
        self.register_function("abort")
        object_type = self.register_type()
        #Ending Object type definition

        #Int type definition
        self.ctype = Type("Int")
        self.ctype.inherit(object_type)
        val = self.ctype.register_attribute(scope.Variable("value", None, True))
        arg = self.ctype.start_constructor()
        self.cfunction = self.ctype.constructor
        self.cfunction.register_instruction(cil.SetAttribNode, arg, 0, 0)
        self.ctype.close_constructor()
        self.register_type()
        #Ending Int type definition

        #Bool type definition
        self.ctype = Type("Bool")
        self.ctype.inherit(object_type)
        self.ctype.register_attribute(scope.Variable("value", None, True))
        arg = self.ctype.start_constructor()
        self.cfunction = self.ctype.constructor
        self.cfunction.register_instruction(cil.SetAttribNode, arg, 0, 0)
        self.ctype.close_constructor()
        self.register_type()
        #Ending Bool type definition

        #String type definition
        self.ctype = Type("String")
        self.all_functions_names_by_types["String"] = {}
        self.ctype.inherit(object_type)
        self.ctype.register_attribute(scope.Variable("msg", None, True))
        self.ctype.attr_references["msg"] = 1
        arg = self.ctype.start_constructor()
        self.cfunction = self.ctype.constructor
        default = self.register_data("")
        self.cfunction.register_instruction(cil.LoadNode, arg, default)
        self.ctype.close_constructor()

        #function concat(self, string)
        f_name = F"concat_{Function.declared_am}"
        self.all_functions_names_by_types["String"]["concat"] = F"concat_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        arg_string = self.cfunction.register_arg(scope.Variable("x", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.ConcatNode, var, arg, arg_string)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("concat")

        #function substr(self, int, int)
        f_name = F"substr_{Function.declared_am}"
        self.all_functions_names_by_types["String"]["substr"] = F"substr_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        arg_int_1 = self.cfunction.register_arg(scope.Variable("i", None, False))
        arg_int_2 = self.cfunction.register_arg(scope.Variable("l", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.SubstringNode, var, arg, arg_int_1, arg_int_2)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("substr")

        #function lenght(self)
        f_name = F"length_{Function.declared_am}"
        self.all_functions_names_by_types["String"]["length"] = F"length_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.LengthNode, var, arg)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("length")
        self.register_type()
        #Ending String type definition

        #IO type definition
        self.ctype = Type("IO")
        self.all_functions_names_by_types["IO"] = {}
        self.ctype.inherit(object_type)
        self.attrs["IO"] = []
        self.ctype.start_constructor()
        self.cfunction = self.ctype.constructor
        self.ctype.close_constructor()

        #function out_string(self, string)
        f_name = F"out_string_{Function.declared_am}"
        self.all_functions_names_by_types["IO"]["out_string"] = F"out_string_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        arg_string = self.cfunction.register_arg(scope.Variable("x", None, False))
        self.cfunction.register_instruction(cil.OutStringNode, arg_string)
        self.cfunction.register_instruction(cil.ReturnNode, arg)
        self.register_function("out_string")

        #function out_int(self, int)
        f_name = F"out_int_{Function.declared_am}"
        self.all_functions_names_by_types["IO"]["out_int"] = F"out_int_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        arg_int = self.cfunction.register_arg(scope.Variable("x", None, False))
        self.cfunction.register_instruction(cil.OutIntNode, arg_int)
        self.cfunction.register_instruction(cil.ReturnNode, arg)
        self.register_function("out_int")

        #function in_string(self)
        f_name = F"in_string_{Function.declared_am}"
        self.all_functions_names_by_types["IO"]["in_string"] = F"in_string_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.InStringNode, var)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("in_string")

        #function in_int(self)
        f_name = F"in_int_{Function.declared_am}"
        self.all_functions_names_by_types["IO"]["in_int"] = F"in_int_{Function.declared_am}"
        Function.declared_am += 1 
        self.cfunction = Function(f_name)
        arg = self.cfunction.register_arg(scope.Variable("self", None, False))
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.InIntNode, var)
        self.cfunction.register_instruction(cil.ReturnNode, var)
        self.register_function("in_int")
        self.register_type()
        #Ending IO type definition
    def use_temp_variable(self):
        """
        Creates and register new temp local variable in 
        current function declaration.
        """
        return self.cfunction.register_local(scope.Variable("temp", None, False))
    def use_object(self, vname):
        """
        Returns a previously registered object or creates a new one.
        >>> `params`\n
        `vname`: vname for new `VariableInfo` instance.
        """
        if vname in self.cfunction.vars_references.keys():
            return self.cfunction.vars_references[vname]
        return self.cfunction.register_local(vname)
    def start_new_type(self,name):
        self.ctype = None
        self.ctype = Type(name)
        self.attrs[name] = []
    def start_new_function(self, name = None):
        self.cfunction = Function(name)
    def continue_function(self, function:Function):
        self.cfunction = function
    def register_data(self, value):
        """
        Register data variable in the dotdata.
        Names will be assigned this way: \n
        data_`<dotdata.index>` assuring name uniqueness.
        """
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    def register_base_type(self):
        ntype = self.ctype.build()
        self.types_references[self.ctype.name] = ntype
        return ntype
    def register_type(self):
        ntype = self.ctype.register()
        self.types_references[self.ctype.name] = ntype
        return ntype
    def register_function(self, name, ctor = False):
        func = self.cfunction.register()
        self.ctype.register_function(name, func, ctor)
        if name in self.function_references.keys():
            self.function_references[name].append(func)
        else:
            self.function_references[name] = [func]
    def register_attribute(self, t:Type, attribute:ast.ClassAttribute):
        # attr = t.register_attribute(attribute.name)
        if t.name in self.attrs.keys():
            self.attrs[t.name].append(attribute)
        else:
            self.attrs[t.name] = [attribute]
    def register_program(self):
        return cil.ProgramNode(self.dottype, self.dotdata, self.dotcode)
    def create_label(self):
        label = cil.LabelNode(f"label_{self.labels_count}")
        self.labels_count += 1
        return label

    #######################################################
    #  Auxiliar Code Generators ###########################
    #######################################################

    def gen_abort_call(self, var, instance):
        self_obj = self.cfunction.self_instance

        #get static type name
        static_type_name = instance.computed_type.name

        self.cfunction.register_instruction(cil.ParamNode, self_obj)
        self.cfunction.register_instruction(cil.VCallNode,var, static_type_name ,"abort")
        return var
    def gen_dynamic_call(self, instance, nparams, method_name):
        #register output variable and type variable
        var = self.use_temp_variable()

        #create error and end labels
        error_label = self.create_label()
        end_label = self.create_label()

        #generate object expression and get dynamic type
        obj_inst = self.gen(instance)
        obj_inst_dtype = self.use_temp_variable()
        self.cfunction.register_instruction(cil.TypeOfNode, obj_inst_dtype, obj_inst)

        #if dynamic type is void then raise error
        condition = self.use_temp_variable()
        self.cfunction.register_instruction(cil.IsTypeNode, condition, obj_inst_dtype, "Void")
        self.cfunction.register_instruction(cil.GotoIfNode, error_label, condition)

        #get static type name
        static_type_name = instance.computed_type.name

        #generate params expressions
        params = [self.gen(param) for param in nparams]
        params.reverse()

        #register params in inverse order
        if params:
            for param in params:
                self.cfunction.register_instruction(cil.ParamNode, param)

        #register param self
        self.cfunction.register_instruction(cil.ParamNode, obj_inst)

        #register virtual function call
        self.cfunction.register_instruction(cil.VCallNode, var, static_type_name, method_name)
        self.cfunction.register_instruction(cil.GotoNode, end_label)

        self.cfunction.register_label(error_label)
        self.gen_abort_call(var, instance)
        self.cfunction.register_instruction(cil.GotoNode, end_label)

        self.cfunction.register_label(end_label)
        return var
    def create_new_instance_gen(self, new_type):
        if new_type == "SELF_TYPE":
            new_obj_type = self.ctype
        else:
            new_obj_type = self.types_references[new_type]
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.AllocateNode, var, new_obj_type)
        self.call_constructor(var, new_obj_type)
        return var
    def gen_aritmetic_expression(self, node, node_type):
        left = self.gen(node.left)
        right = self.gen(node.right)
        result = self.use_temp_variable()
        self.cfunction.register_instruction(node_type, result, left, right)
        return result
    def gen_create_attr(self, node:ast.ClassAttribute):
        self.ctype.register_attribute(node.variable)

    #######################################################
    #          VISITOR          ###########################
    #######################################################

    @visit.on('node')
    def gen(self, node):
        pass

    @visit.when(ast.Program)
    def gen(self,node:ast.Program):
        for class_node in node.classes:
            blank_type = Type(class_node.name)
            blank_type.start_constructor(class_node.variable)
            self.all_functions_names_by_types[class_node.name] = {}
            for feature in class_node.feature_list:
                if isinstance(feature, ast.ClassMethod):
                    self.all_functions_names_by_types[class_node.name][feature.name] = F"{feature.name}_{Function.declared_am}"
                    Function.declared_am += 1

            self.types_references[class_node.name] = blank_type
            self.attrs[blank_type.name] = []
        for class_node in node.classes:
            self.gen(class_node)
        return self.register_program()
    
    @visit.when(ast.Class)
    def gen(self,node:ast.Class):
        #prepare features to be expandable
        inherited_features = []

        #check if already existing type
        for t in self.dottype:
            if node.name == t.name:
                return

        parent = None
        if node.parent and node.name != "Object":
            #priorize parent generation recursively
            #check if parent type is already generated
            parent_generated = False
            for t in self.dottype:
                if t.name == node.parent:
                    parent_generated = True
                    parent = t

            #if parent type is still not generated then generate it first
            if not parent_generated:
                for t in self.program.classes:
                    if t.name == node.parent:
                        self.gen(t)
                        parent = self.dottype[-1]

        #starts creation of new type node
        if node.name in self.types_references.keys():
            self.ctype = self.types_references[node.name]
        else:
            self.start_new_type(node.name)

        if parent:
            #expand features list with inherited attributes
            inherited_features = [attr for attr in self.attrs[parent.name]]
            self.ctype.inherit(parent)

        #prepare constructor for atributes
        features = inherited_features + node.feature_list
        functions = []
        #if no contructor was created then create one
        if not self.ctype.constructor:
            self.ctype.start_constructor()
        self.continue_function(self.ctype.constructor)

        for feature in features:
            if isinstance(feature,ast.ClassMethod):
                functions.append(feature)
                continue
            self.gen_create_attr(feature)
        
        for feature in features:
            if isinstance(feature,ast.ClassMethod):
                continue
            self.gen(feature)

        self.continue_function(self.ctype.constructor)
        #end constructor definition
        self.ctype.close_constructor()

        #end basic type definition with no functions declared
        #(this is made in order that class functions may create new instances
        # of this same class)
        self.register_base_type()

        #register function features
        for Function in functions:
            self.gen(Function)

        #end type definition
        self.register_type()

    @visit.when(ast.Object)
    def gen(self,node:ast.Object):
        if node.variable.attribute:
            var =  self.use_temp_variable()
            attr = node.variable
            atr = self.ctype.attr_references[node.name]
            self.cfunction.register_instruction(cil.GetAttribNode, var, self.cfunction.self_instance , atr)
            return var
        obj = self.cfunction.register_local(node.variable)
        return obj

    @visit.when(ast.Parameter)
    def gen(self,node:ast.Parameter):
        self.cfunction.register_arg(node.variable)

    @visit.when(ast.ClassMethod)
    def gen(self,node:ast.ClassMethod):
        self.start_new_function(self.all_functions_names_by_types[self.ctype.name][node.name])
        self.cfunction.register_arg(node.variable)
        self.cfunction.self_instance = node.variable
        for param in node.params:
            self.gen(param)
        result = 0
        result = self.gen(node.body)
        self.cfunction.register_instruction(cil.ReturnNode, result)
        self.register_function(node.name)

    @visit.when(ast.ClassAttribute)
    def gen(self,node:ast.ClassAttribute):
        #get final attribute value
        if node.initializer_expr:
            att_value = self.gen(node.initializer_expr)
        else:
            if node.f_type in ["Int", "String", "Object", "IO", "Bool"]:
                att_value = self.create_new_instance_gen(node.f_type)
            else: 
                att_value = self.create_new_instance_gen("Void")
        self_param = self.cfunction.self_instance
        attr = self.ctype.attr_references[node.variable.name]
        self.cfunction.register_instruction(cil.SetAttribNode, self_param, attr, att_value)
        #register attribute in type
        self.register_attribute(self.ctype, node)

    @visit.when(ast.Assingment)
    def gen(self,node:ast.Assingment):
        right = self.gen(node.expr)
        if node.object_inst.variable.attribute:
            tmp = self.use_temp_variable()
            atr = self.ctype.attr_references[node.object_inst.name]
            self.cfunction.register_instruction(cil.SetAttribNode, self.cfunction.self_instance , atr, right)
            self.cfunction.register_instruction(cil.GetAttribNode, tmp, self.cfunction.self_instance,  self.ctype.attr_references[node.object_inst.variable.name])
            return tmp
        else:
            obj = self.gen(node.object_inst)
            self.cfunction.register_instruction(cil.AssignNode, obj, right)
            return obj

    @visit.when(ast.Block)
    def gen(self,node:ast.Block):
        result = None
        for exp in node.expr_block:
            result = self.gen(exp)
        return result

    @visit.when(ast.Let)
    def gen(self,node:ast.Let):
        var = node.variable
        if node.init_expr:
            init = self.gen(node.init_expr)
            self.cfunction.register_instruction(cil.AssignNode,var,init)
        for nl in node.nested_lets:
            self.gen(nl)
        return self.gen(node.body)

    @visit.when(ast.New)
    def gen(self,node:ast.New):
        return self.create_new_instance_gen(node.new_object_type)

    @visit.when(ast.IsVoid)
    def gen(self,node:ast.IsVoid):
        expr_result = self.gen(node.expr)
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.IsTypeNode, var, expr_result, "Void")
        bool_result = self.create_new_instance_gen("Bool")
        self.cfunction.register_instruction(cil.SetAttribNode, bool_result, 0, var)
        return bool_result

    @visit.when(ast.Case)
    def gen(self,node:ast.Case):
        loop_label = self.create_label()
        end_label = self.create_label()
        error_label = self.create_label()

        #generate expression and get Type
        obj = self.gen(node.expr)
        obj_type = self.use_temp_variable()
        self.cfunction.register_instruction(cil.TypeOfNode, obj_type, obj)

        #create output variable
        result = self.use_temp_variable()

        #loop label
        self.cfunction.register_label(loop_label)

        #checking non void type
        condition = self.use_temp_variable()
        self.cfunction.register_instruction(cil.IsTypeNode, condition, obj_type, "Void")
        self.cfunction.register_instruction(cil.GotoIfNode, error_label, condition)

        for action in node.actions:
            act_label = self.create_label() #new label for action expression
            next_act_label = self.create_label() #new label for action expression

            #check if action type match object type
            condition = self.use_temp_variable()
            self.cfunction.register_instruction(cil.IsTypeNode, condition, obj_type, action.r_type)
            self.cfunction.register_instruction(cil.GotoIfNode, act_label, condition)

            #if not met condition then go to next action label
            self.cfunction.register_instruction(cil.GotoNode, next_act_label)
            self.cfunction.register_label(act_label)

            #bound action id to <expr0> result
            var = self.cfunction.register_local(action.variable)
            self.cfunction.register_instruction(cil.AssignNode, var, obj)

            #generate action expression
            expr_result = self.gen(action.expr)
            self.cfunction.register_instruction(cil.AssignNode, result, expr_result)
            self.cfunction.register_instruction(cil.GotoNode, end_label)

            #continue to next action label
            self.cfunction.register_label(next_act_label)

        #check for parent type case
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.ParentTypeNode, var, obj_type)
        self.cfunction.register_instruction(cil.AssignNode, obj_type, var)

        #jump to the loop start label
        self.cfunction.register_instruction(cil.GotoNode, loop_label)

        #runtime error if not viable branch
        self.cfunction.register_label(error_label)
        self.gen_abort_call(var, node.expr)

        #end of case
        self.cfunction.register_label(end_label)
        return result

    @visit.when(ast.Add)
    def gen(self,node:ast.Add):
        return self.gen_aritmetic_expression(node, cil.PlusNode)

    @visit.when(ast.Sub)
    def gen(self,node:ast.Sub):
        return self.gen_aritmetic_expression(node, cil.MinusNode)

    @visit.when(ast.Mul)
    def gen(self,node:ast.Mul):
        return self.gen_aritmetic_expression(node, cil.MultNode)

    @visit.when(ast.Div)
    def gen(self,node:ast.Div):
        return self.gen_aritmetic_expression(node, cil.DivNode)

    @visit.when(ast.LessThan)
    def gen(self,node:ast.LessThan):
        left = self.gen(node.left)
        right = self.gen(node.right)
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.LessThanNode, var, left, right)
        return var

    @visit.when(ast.LessThanOrEqual)
    def gen(self,node:ast.LessThanOrEqual):
        left = self.gen(node.left)
        right = self.gen(node.right)
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.LessThanOrEqualNode, var, left, right)
        return var

    @visit.when(ast.Equal)
    def gen(self,node:ast.Equal):
        left = self.gen(node.left)
        right = self.gen(node.right)
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.EqualNode, var, left, right)
        return var

    @visit.when(ast.If)
    def gen(self,node:ast.If):
        condition = self.gen(node.predicate)
        var = self.use_temp_variable()
        then_label = self.create_label()
        else_label = self.create_label()
        final_label = self.create_label()
        self.cfunction.register_instruction(cil.GotoIfNode,then_label, condition)
        self.cfunction.register_instruction(cil.GotoNode,else_label)

        #then instructions
        self.cfunction.register_label(then_label)
        then_result = self.gen(node.then_body)
        self.cfunction.register_instruction(cil.AssignNode, var, then_result)
        self.cfunction.register_instruction(cil.GotoNode,final_label)

        #else instructions
        self.cfunction.register_label(else_label)
        else_result = self.gen(node.else_body)
        self.cfunction.register_instruction(cil.AssignNode, var, else_result)

        #final label
        self.cfunction.register_label(final_label)
        return var

    @visit.when(ast.WhileLoop)
    def gen(self,node:ast.WhileLoop):
        loop_label = self.create_label()
        end_label = self.create_label()

        #check initial condition
        condition = self.gen(node.predicate)
        self.cfunction.register_instruction(cil.GotoIfNode, loop_label, condition)
        self.cfunction.register_instruction(cil.GotoNode, end_label)

        self.cfunction.register_label(loop_label)

        #generate while body
        self.gen(node.body)

        #check condition, if evaluates false then finish while else start again
        condition = self.gen(node.predicate)
        self.cfunction.register_instruction(cil.GotoIfNode, loop_label, condition)
        self.cfunction.register_label(end_label)
        result = self.create_new_instance_gen("Void")
        return result

    @visit.when(ast.IntegerComplement)
    def gen(self,node:ast.IntegerComplement):
        value = self.gen(node.expr)
        var = self.use_temp_variable()
        zero = self.create_new_instance_gen("Int")
        self.cfunction.register_instruction(cil.MinusNode, var, zero, value)
        return value

    @visit.when(ast.BooleanComplement)
    def gen(self,node:ast.BooleanComplement):
        #generate expression
        bool_instance = self.gen(node.expr)

        #create new instance of int to store vale 1
        one = self.create_new_instance_gen("Int")
        self.cfunction.register_instruction(cil.SetAttribNode, one, 0, 1)

        bool_value = self.create_new_instance_gen("Int")
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.GetAttribNode, var, bool_instance, 0)
        self.cfunction.register_instruction(cil.SetAttribNode, bool_value, 0, var)
        new_var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.MinusNode, new_var, one, bool_value)
        self.cfunction.register_instruction(cil.SetAttribNode, bool_instance, 0, new_var) 
        return bool_instance

    @visit.when(ast.Integer)
    def gen(self,node:ast.Integer):
        #create new instance of Int Type
        instance = self.create_new_instance_gen("Int")

        #set attribute value of instance with the literal value
        self.cfunction.register_instruction(cil.SetAttribNode, instance, 0, node.value)
        return instance

    @visit.when(ast.Boolean)
    def gen(self,node:ast.Boolean):
        #create new instance of Bool Type
        instance = self.create_new_instance_gen("Bool")

        #store real value of Bool
        if node.value == "TRUE":
            #set attribute value of instance with the literal value
            self.cfunction.register_instruction(cil.SetAttribNode, instance, 0, 1)
        return instance

    @visit.when(ast.String)
    def gen(self,node:ast.String):
        #create new instance of String Type
        # instance = self.create_new_instance_gen("String")

        #register string value
        data = self.register_data(node.value)

        #get the pointer to the data message and store it
        var = self.use_temp_variable()
        self.cfunction.register_instruction(cil.LoadNode, var, data)

        #set attribute msg of instance to point the given data
        # self.cfunction.register_instruction(cil.SetAttribNode, instance, 0, var)
        return var

    @visit.when(ast.DynamicDispatch)
    def gen(self,node:ast.DynamicDispatch):
        return self.gen_dynamic_call(node.object_inst, node.params, node.method)

    @visit.when(ast.StaticDispatch)
    def gen(self,node:ast.StaticDispatch):
        var = self.use_temp_variable()
        obj_inst = self.gen(node.object_inst)
        rtype = node.obj_type
        function = self.all_functions_names_by_types[rtype][node.method]

        #search for the actual function to call
        # for t_function in rtype.type_functions:
        #     if t_function.name == node.method:
        #         function = t_function.function

        #create error and end labels
        error_label = self.create_label()
        end_label = self.create_label()

        obj_inst_dtype = self.use_temp_variable()
        self.cfunction.register_instruction(cil.TypeOfNode, obj_inst_dtype, obj_inst)

        #if dynamic type is void then raise error
        condition = self.use_temp_variable()
        self.cfunction.register_instruction(cil.IsTypeNode, condition, obj_inst_dtype, "Void")
        self.cfunction.register_instruction(cil.GotoIfNode, error_label, condition)

        #generate params expressions
        params = [self.gen(param) for param in node.params]
        params.reverse()

        #register params in inverse order
        if params:
            for param in params:
                self.cfunction.register_instruction(cil.ParamNode, param)

        #register param self
        self.cfunction.register_instruction(cil.ParamNode, obj_inst)

        #register function call
        self.cfunction.register_instruction(cil.CallNode, var, function)
        self.cfunction.register_instruction(cil.GotoNode, end_label)

        self.cfunction.register_label(error_label)
        self.gen_abort_call(var,node.object_inst)

        self.cfunction.register_label(end_label)
        return var

    @visit.when(ast.Self)
    def gen(self,node:ast.Self):
        return node.variable