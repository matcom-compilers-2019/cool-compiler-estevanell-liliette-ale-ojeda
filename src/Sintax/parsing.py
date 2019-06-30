import ply.yacc as yacc
import sys
from Utils.Cool.ast import *
from Sintax.lexer import create_lexer

#-------------------------Parser----------------------------------#

class CoolParsX(object):
    def __init__(self):
        self.tokens = None
        self.lexer = None
        self.parser = None
        self.error_list = []

    #-----------------------Grammar Rules----------------------------#
    def p_program(self, p):
        """
        program : classes
        """
        p[0] =  Program(classes = p[1])

    def p_classes(self, p):
        """
        classes : classes class SEMICOLON
                | class SEMICOLON
        """
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_class(self, p):
        """
        class : CLASS TYPE LBRACE features_list_init RBRACE
        """
        p[0] =  Class(name = p[2], parent = "Object", feature_list = p[4])

    def p_class_inherits(self, p):
        """
        class : CLASS TYPE INHERITS TYPE LBRACE features_list_init RBRACE
        """
        p[0] =  Class(name = p[2], parent = p[4], feature_list = p[6])

    def p_feature_list_init(self, p):
        """
        features_list_init : features_list
                            | empty
        """
        p[0] = [] if p.slice[1].type == "empty" else p[1]

    def p_feature_list(self, p):
        """
        features_list : features_list feature SEMICOLON
                      | feature SEMICOLON
        """
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_feature_method(self, p):
        """
        feature : ID LPAREN params_list RPAREN COLON TYPE LBRACE expression RBRACE
        """
        p[0] =  ClassMethod(name=p[1], params=p[3], return_type=p[6], body=p[8])        

    def p_feature_method_no_params(self, p):
        """
        feature : ID LPAREN RPAREN COLON TYPE LBRACE expression RBRACE
        """
        p[0] =  ClassMethod(name=p[1], params = list(), return_type = p[5], body = p[7])        

    def p_feature_attribute_initialized(self, p):
        """
        feature : ID COLON TYPE ASSIGN expression
        """
        p[0] =  ClassAttribute(name = p[1], attribute_type = p[3], initializer_expr = p[5])

    def p_feature_attr(self, p):
        """
        feature : ID COLON TYPE
        """
        p[0] =  ClassAttribute(name=p[1], attribute_type=p[3], initializer_expr = None)        

    def p_params_list(self, p):
        """
        params_list : params_list COMMA params
                    | params
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_param(self, p):
        """
        params : ID COLON TYPE
        """
        p[0] =  Parameter(name=p[1], p_type=p[3])        

    def p_expression_object_identifier(self, p):
        """
        expression : ID
        """
        p[0] =  Object(name = p[1])

    # def p_expression_self_type(self, p):
    #     """
    #     expression : SELF_TYPE
    #     """
    #     p[0] =  SelfType()

    def p_expression_integer(self, p):
        """
        expression : INTEGER
        """
        p[0] =  Integer(value=p[1])        

    def p_expression_boolean(self, p):
        """
        expression : TRUE
        expression : FALSE

        """
        p[0] =  Boolean(value=p[1])        

    def p_expression_string(self, p):
        """
        expression : STRING
        """
        p[0] =  String(value=p[1])        

    def p_expr_self(self, p):
        """
        expression  : SELF
        """
        p[0] =  Self()

    def p_expr_block(self, p):
        """
        expression : LBRACE block RBRACE
        """
        p[0] =  Block(expr_block=p[2])

    # def p_block_init(self,p):
    #     """
    #     iblock : block
    #     """
    #     p[0] = Block(p[1])

    # def p_block_init_expr(self,p):
    #     """
    #     iblock : expression
    #     """
    #     p[0] = p[1]

    def p_block(self, p):
        """
        block : block expression SEMICOLON
              | expression SEMICOLON
        """
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_expr_assignment(self, p):
        """ 
        expression : ID ASSIGN expression
        """
        p[0] =  Assingment(object_inst =  Object(name=p[1]), expr = p[3])        

    def p_expr_dispatch(self, p):
        """
        expression : expression DOT ID LPAREN arguments_list_init RPAREN
        """
        p[0] =  DynamicDispatch(object_inst = p[1], method = p[3], params = p[5])

    def p_arguments_list_init(self, p):
        """
        arguments_list_init : arguments_list
                           | empty
        """
        p[0] = list() if p.slice[1].type == "empty" else p[1]

    def p_arguments_list(self, p):
        """
        arguments_list : arguments_list COMMA expression
                       | expression
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expr_static_dispatch(self, p):
        """
        expression : expression AT TYPE DOT ID LPAREN arguments_list_init RPAREN
        """
        p[0] =  StaticDispatch(object_inst=p[1], obj_type=p[3], method=p[5], params=p[7])

    def p_expr_self_dispatch(self, p):
        """
        expression : ID LPAREN arguments_list_init RPAREN
        """
        p[0] =  DynamicDispatch(object_inst =  Object("self"), method = p[1], params = p[3])

    def p_expr_math_operations(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULTIPLY expression
                   | expression DIVIDE expression
        """
        if p[2] == '+':
            p[0] =  Add(left=p[1], right=p[3])
        elif p[2] == '-':
            p[0] =  Sub(left=p[1], right=p[3])
        elif p[2] == '*':
            p[0] =  Mul(left=p[1], right=p[3])
        elif p[2] == '/':
            p[0] =  Div(left=p[1], right=p[3])

    def p_expr_math_comparisons(self, p):
        """
        expression : expression LT expression
                   | expression LTEQ expression
                   | expression EQ expression
        """ 
        if p[2] == '<':
            p[0] =  LessThan(left=p[1], right=p[3])
        elif p[2] == '<=':
            p[0] =  LessThanOrEqual(left=p[1], right=p[3])
        elif p[2] == '=':
            p[0] =  Equal(left=p[1], right=p[3])

    def p_expr_with_parenthesis(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_expr_if_conditional(self, p):
        """
        expression : IF expression THEN expression ELSE expression FI
        """
        p[0] =  If(predicate = p[2], then_body = p[4], else_body = p[6])

    def p_expr_while_loop(self, p):
        """ 
        expression : WHILE expression LOOP expression POOL
        """ 
        p[0] =  WhileLoop(predicate = p[2], body = p[4])

    def p_expr_let(self, p):
        """
        expression : let_expression
        """
        p[0] = p[1]

    def p_expr_let_heads(self, p): #new 1
        """
        let_expression_heads : let_expression_head_i COMMA let_expression_heads
                            | let_expression_head COMMA let_expression_heads
        """
        p[0] = [p[1]] + p[3]

    def p_expr_let_heads_end(self, p): #new 1
        """
        let_expression_heads : let_expression_head_i
                             | let_expression_head
        """
        p[0] = [p[1]]

    def p_expr_let_head_i(self, p): #new 1
        """
        let_expression_head_i : ID COLON TYPE ASSIGN expression
        """ 
        p[0] = Let(obj_inst = p[1], return_type = p[3], init_expr = p[5], body = None)

    def p_expr_let_head(self, p): #new 1
        """
        let_expression_head : ID COLON TYPE
        """
        p[0] = Let(obj_inst = p[1], return_type = p[3], init_expr = None, body = None)

    def p_expr_let_simple(self, p): #updated 1
        """
        let_expression : LET ID COLON TYPE COMMA let_expression_heads IN expression
                       | LET ID COLON TYPE IN expression
        """
        if p[5] == ",":
            p[0] =  Let(obj_inst = p[2], return_type = p[4], init_expr = None, body = p[8], nested_lets = p[6])
        else:
            p[0] = Let(obj_inst = p[2], return_type = p[4], init_expr = None, body = p[6])

    def p_expr_let_initialized(self, p): #updated
        """ 
        let_expression : LET ID COLON TYPE ASSIGN expression COMMA let_expression_heads IN expression
                       | LET ID COLON TYPE ASSIGN expression IN expression
        """
        if p[7] == ",":
            p[0] =  Let(obj_inst = p[2], return_type = p[4], init_expr = p[6], body = p[10], nested_lets = p[8])
        else:
            p[0] = Let(obj_inst = p[2], return_type = p[4], init_expr = p[6], body = p[8])

    def p_expr_case(self, p): 
        """
        expression : CASE expression OF actions ESAC
        """
        p[0] =  Case(expr=p[2], actions=p[4])

    def p_actions_list(self, p):
        """
        actions : actions action
                | action
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_action_expr(self, p):
        """
        action : ID COLON TYPE ARROW expression SEMICOLON
        """
        p[0] =  Action(r_object = p[1],r_type = p[3], expr = p[5])

    def p_expr_new(self, p):
        """
        expression : NEW TYPE
        """ 
        p[0] =  New(new_object_type = p[2])

    def p_expr_isvoid(self, p):
        """
        expression : ISVOID expression
        """
        p[0] =  IsVoid(p[2]) 

    def p_expr_integer_complement(self, p):
        """
        expression : INT_COMP expression
        """ 
        p[0] =  IntegerComplement(p[2])

    def p_expr_boolean_complement(self, p):
        """
        expression : NOT expression
        """
        p[0] =  BooleanComplement(p[2]) 

    def p_empty(self, p):
        """
        empty :
        """
        p[0] = None

    def p_error(self, p):
        """
        Error rule for Syntax Errors handling and reporting.
        """
        if p is None:
            print("Error! Unexpected end of input!")
        else:
            error = "Syntax error! Line: {}, position: {}, character: {}, type: {}".format(
                p.lineno, p.lexpos, p.value, p.type)
            self.error_list.append(error)
            self.parser.errok()

    def build(self, lexer = None):
        """
        if no lexer is provided a new one will be created
        """
        if not lexer:
            self.lexer = create_lexer()
        else:
            self.lexer = lexer
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module = self)

    def parse(self, program_source_code):
        if self.parser is None:
            raise ValueError("Parser was not build, try building it first with the build() method.")
        return self.parser.parse(program_source_code)