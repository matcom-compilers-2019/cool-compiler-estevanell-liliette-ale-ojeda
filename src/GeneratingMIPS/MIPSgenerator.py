import Utils.visitor as visitor
import Semantics.scope
from Utils.CIL.ast import *

class Type:
    def __init__(self, tag, name, parent):
        self.tag = tag
        self.name = name
        self.attr = {}
        self.functs = {}
        self.imp_functs = {}
        self.parent = parent

class MipsGenerator:

    def __init__(self):
        self.to_data = []
        self.to_text = []
        self.types = {}
        # self.tag_to_type = []
        self.lcounter = 0

        self.cargs = []
        self.clocals = []
    
    ########################################################
    ###################### UTILS ###########################  
    ########################################################

    def write_to_data(self, instruction):
        self.to_data.append(instruction)

    def write_to_text(self, instruction):
        self.to_text.append(instruction)

    def my_push(self, reg):
        self.write_to_text(f"# PUSHING {reg}")
        self.write_to_text(f"sw {reg} 0($sp)")
        self.write_to_text(f"addiu $sp $sp -4")
    
    def create_integer(self, reg_value): # registro en que esta el value,
        offset = self.types["Int"].tag * 8
        self.write_to_text(f"# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE")
        self.write_to_text(f"lw $a0 {offset}($s6)")    
        self.write_to_text(f"jal obj_copy")
        self.write_to_text(f"sw {reg_value} 12($a0)")
    
    def create_bool(self, reg_value):# registro en que esta el value,
        offset = self.types["Bool"].tag * 8
        self.write_to_text(f"# CREATE A NEW BOOL PROTOYPE IN HEAP AND STORE ITS VALUE")
        self.write_to_text(f"lw $a0 {offset}($s6)")    
        self.write_to_text(f"jal obj_copy")
        self.write_to_text(f"sw {reg_value} 12($a0)")

    # UTILIZA LOS REG a1, t6, t7 y a0 los 3 primeros no se respetan, en a0 se retorna la pos del str 
    def create_str(self, r_length):
        self.write_to_text(f"# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE")
        self.write_to_text(f"addi $t5 {r_length} 1") # Sumo 1 pal $0                
        self.create_integer(r_length)# En a0 tengo la ref la int length
        self.write_to_text(f"move $a1 $a0") # DEJO EL INICIO DEL PROT CREADO EN a1
        self.write_to_text(f"li $a0 0")
        self.write_to_text(f"addi $t5 $t5 16")                
        self.write_to_text(f"add $a0 $a0 $t5")
        self.write_to_text(f"jal mem_alloc")# Reservo size exacto
        tg = self.types["String"].tag
        self.write_to_text(f"li $t6 {tg}")# lleno el class_tag (solo para cumplir con el prot)
        self.write_to_text(f"sw $t6 ($a0)")
        self.write_to_text(f"sw $t5 4($a0)")# lleno el size
        self.write_to_text(f"sw $a1 12($a0)")# ref al integer Length
        self.write_to_text(f"lw $t6 {tg*8}($s6)")
        self.write_to_text(f"lw $t7 8($t6)")
        self.write_to_text(f"sw $t7 8($a0)")# ref a la tmv
        self.write_to_text(f"move $t0 {r_length}")# DEJO EL LENGTH EN t0

    def crt_str_cmp(self, s):
        self.write_to_text(f"# CMP CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE")
        size = len(s) + 17
        if size % 4 != 0:
            size += (4 - (size % 4))
        str_tg = self.types["String"].tag

        self.write_to_text(f"li $a0 {size}")# cargo el size
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $a1 $a0")# save ref to new space
        self.write_to_text(f"li $t7 {str_tg}")
        self.write_to_text(f"sw $t7 ($a1)")# pongo el tag
        self.write_to_text(f"li $t7 {size}")
        self.write_to_text(f"sw $t7 4($a1)")#pogo el size
        self.write_to_text(f"lw $t7 {str_tg*8}($s6)")
        self.write_to_text(f"lw $t7 8($t7)")# tengo en t7 la ref a la tmv
        self.write_to_text(f"sw $t7 8($a1)")# pongo la ref a la  tmv

        self.write_to_text(f"li $t7 {len(s)}") # pongo en t7 el len pa crear el int Length
        self.create_integer(f"$t7")# tengo en a0 la ref al integer

        self.write_to_text(f"sw $a0 12($a1)")# guardo el inr length en el str
        
        pos = 16
        for char in s:
            self.write_to_text(f"li $t7 {ord(char)}")
            self.write_to_text(f"sb $t7 {pos}($a1)")#copio char a char
            pos+=1
        self.write_to_text(f"li $t7 0")# endline
        self.write_to_text(f"sb $t7 {pos}($a1)")
        self.write_to_text(f"move $a0 $a1")#dejo en str en a0
        


        


    ########################################################
    #################### GENERATED CODE ####################  
    ########################################################



    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode) 
    def visit(self, node : ProgramNode):
        # TYPES
        self.to_data.append(".data")
        self.to_text.append(".text")

        self.to_text.append("main:")
        self.write_to_text(f"move $s7 $gp")
        self.write_to_text(f"addi $s7 $s7 30000")

        self.write_to_data(f"_abort: .asciiz \"Program Aborted\"")
        self.write_to_data(f"_zero: .asciiz \"0 Division Error\"")
        self.write_to_data(f"_substr: .asciiz \"Substr Length Error\"")
        self.write_to_data(f"_mem: .asciiz \"Memory Error\"")
        self.write_to_data(f"")

        self.write_to_text(f"# SAVE A REFERENCE TO ALL THE PROTOTYPES IN $s6")
        self.write_to_text(f"li $a0 {8 * len(node.types_section)}")# REVISAR SI PONER EL STR
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $s6 $a0")
        self.write_to_text(f"")

        self.write_to_text(f"# SAVE A REFERENCE TO ALL THE TYPES-NAMES IN $s5")
        self.write_to_text(f"li $a0 {4 * len(node.types_section)}")# REVISAR SI NECESITO CAMBIAR POR OBJ STR
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $s5 $a0")
        self.write_to_text(f"")

        self.write_to_text(f"# SAVE A REFERENCE TO ALL THE PARENTS PROTOTYPES IN $s4")
        self.write_to_text(f"li $a0 {4 * len(node.types_section)}")# REVISAR SI NECESITO CAMBIAR POR OBJ STR
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $s4 $a0")
        self.write_to_text(f"")

        tx = 0
        self.write_to_text(f"# VISITING ALL THE TYPES NODES")
        for t in node.types_section:
            self.visit(t, tx)
            tx += 1
        
        tg = self.types["Main"].tag * 8
        tgctr = self.types["Main"].tag * 8 + 4
        off = self.types["Main"].functs["main"]

        self.write_to_text(f"#empieza esta pinga")
        self.write_to_text(f"lw $a0 {tg}($s6)")

        self.write_to_text(f"jal obj_copy")
        self.write_to_text(f"move $a2 $a0")
        
        self.my_push("$a0")
        self.my_push("$fp")
        
        self.write_to_text(f"lw $t0 {tgctr}($s6)")
        self.write_to_text(f"jalr $t0")

        self.write_to_text(f"addi $sp $sp -8")

        self.write_to_text(f"lw $t0 {tg}($s6)")
        self.write_to_text(f"lw $t0 8($t0)")
        self.write_to_text(f"lw $t0 {off}($t0)")
        
        self.write_to_text(f"jalr $t0")

        self.write_to_text(f"lw $a0 12($a0)")

        self.write_to_text(f"b _end_main")
        self.write_to_text(f"# END MAIN")

        self.write_to_data(f"# VISITING ALL THE DATA NODES")
        for d in node.data_section:
            self.visit(d)

        # self.main()

        self.write_to_text(f"# VISITING ALL THE FUNCTIONS NODES")        
        for f in node.code_section:
            self.visit(f)

        self.write_to_text(f"# CREATING SOME UTIL FUNCTIONS")
        self.utils_functs()
        self.write_to_text(f"_end_main:")

        
    @visitor.when(TypeNode) 
    def visit(self, node : TypeNode, tag):
        self.types[f"{node.name}"] = Type(tag, f"{node.name}", node.parent)### REVISAAAAAAAAAAAAARRRRRRRRR NOMBREEEEEEEEE
        # self.tag_to_type[tag] = f"{node.name}" 
        offset = 0
        for attr in node.attributes:
            self.types[f"{node.name}"].attr[f"{attr.name}"] = offset
            offset += 4
        
        self.write_to_text(f"#{node.name}")
        self.write_to_text(f"li $a0 {4*len(node.attributes)+12} #reservo mem para {node.name}")# Para reservar mem para el prot
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $t0 $a0")# Muevo a t0 porque a0 sera utilizado por fill_vmt
        self.write_to_text(f"li $t1 {tag}")
        self.write_to_text(f"sw $t1 ($t0)")# Pongo el tag
        self.write_to_text(f"li $t1 {4*len(node.attributes)+12}")
        self.write_to_text(f"sw $t1 4($t0) # guardo el size")# Pongo el size
        self.write_to_text(f"")
        
        # Creo la tabla de metodos virtuales
        self.write_to_text(f"# CREATING VIRTUAL TABLE METHOD")
        offset = 0
        self.write_to_text(f"li $a0 {4*len(node.type_functions)}")
        self.write_to_text(f"jal mem_alloc")# Reservo mem para las direcciones de las funciones  
        self.write_to_text(f"")
        for f in node.type_functions:
            self.types[f"{node.name}"].functs[f"{f.name}"] = offset
            self.types[f"{node.name}"].imp_functs[f"{f.function}"] = offset
            self.visit(f,offset)
            offset += 4
        self.write_to_text(f"")

        self.write_to_text(f"sw $a0 8($t0)")
        self.write_to_text(f"sw $t0 {8*tag}($s6)")# Pongo la direccion de la tabla
        self.write_to_text(f"")
        self.write_to_text(f"la $t0 {node.constructor.name}")#REVISAR
        self.write_to_text(f"sw $t0 {8*tag + 4}($s6)")# Pongo la direccion del init en la pos 8*tag + 4
        self.write_to_text(f"")
        self.write_to_data(f"_{node.name}: .asciiz \"{node.name}\"")# setear los typename (data)
        self.write_to_text(f"la $t0 _{node.name}")
        self.write_to_text(f"sw $t0 {4*tag}($s5)")
        self.write_to_text(f"")

        if node.name != "Void":
            k = 8*self.types[(self.types[f"{node.name}"].parent.name)].tag
        else:
            k = 0
        self.write_to_text(f"lw $t0 {k}($s6)") # pon en a0 el prot de mi parent
        self.write_to_text(f"sw $t0 {4*tag}($s4)")# Pongo la direccion de la tabla de parents
        self.write_to_text(f"")
        

    # @visitor.when(AttributeNode) 
    # def visit(self, node : AttributeNode):
    #     pass
    
    @visitor.when(TypeFunctionNode) 
    def visit(self, node : TypeFunctionNode, offset):
        self.write_to_text(f"# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE")
        self.write_to_text(f"la $t1 {node.function.name}")# Cargo la direccion
        self.write_to_text(f"sw $t1 {offset}($a0)")# Pongo en su offset
        self.write_to_text(f"")

    @visitor.when(DataNode) 
    def visit(self, node : DataNode):
        self.write_to_data(f"{node.name}: .asciiz \"{node.value}\"")

    @visitor.when(FunctionNode) 
    def visit(self, node : FunctionNode):
        self.cargs = node.params
        self.clocals = node.localvars

        self.write_to_text(f"{node.name}:")
        self.my_push(f"$ra")# Save ra
        self.write_to_text(f"")
        self.write_to_text(f"move $fp $sp")# Save fp  
        self.write_to_text(f"")

        self.write_to_text(f"addi $sp $sp {-4*len(node.localvars)}")# Svae space for locals
        for inst in node.instructions:
            self.visit(inst)
        
        z = len(self.clocals) + len(self.cargs)
        self.write_to_text(f"lw $ra 4($fp)")# Cargo ra
        self.write_to_text(f"lw $fp 8($fp)")# Cargo fp
        self.write_to_text(f"addi $sp $sp {4*z + 8}")# Limpio la pila       
        self.write_to_text(f"jr $ra")        
        self.write_to_text(f"")
        

    @visitor.when(ParamNode) 
    def visit(self, node : ParamNode):
        o1 = (self.cargs.index(node.obj) + 3) * 4 if node.obj in self.cargs else self.clocals.index(node.obj) * -4
        self.write_to_text(f"lw $t0 {o1}($fp)")
        self.write_to_text(f"")
        self.my_push("$t0")        
        self.write_to_text(f"")
    
    # @visitor.when(LocalNode)
    # def visit(self, node : LocalNode):
    #     pass
    
    # @visitor.when(InstructionNode)
    # def visit(self, node : InstructionNode):
    #     pass
    
    @visitor.when(AssignNode)
    def visit(self, node : AssignNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# ASSIGN NODE")
        self.write_to_text(f"lw $t0 {o1}($fp)")
        self.write_to_text(f"sw $t0 {d}($fp)")
        self.write_to_text(f"")
        
    # @visitor.when(ArithmeticNode)
    # def visit(self, node : ArithmeticNode):
    #     pass

    # @visitor.when(IntegerNode)
    # def visit(self, node : IntegerNode):
    #     self.write_to_text(f"li $a0 {node.value}")# MAAAAL
    #     self.write_to_text(f"")

    @visitor.when(PlusNode)
    def visit(self, node : PlusNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        self.write_to_text(f"# PLUS NODE")        
        self.write_to_text(f"lw $t1 {o1}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")

        self.write_to_text(f"lw $t2 {o2}($fp)")
        self.write_to_text(f"lw $t2 12($t2)")

        self.write_to_text(f"add $t1 $t1 $t2")

        self.write_to_text(f"")
        self.create_integer("$t1")       
        self.write_to_text(f"")
        
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")


    @visitor.when(MinusNode)
    def visit(self, node : MinusNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        self.write_to_text(f"# Minus NODE")        
        self.write_to_text(f"lw $t1 {o1}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")

        self.write_to_text(f"lw $t2 {o2}($fp)")
        self.write_to_text(f"lw $t2 12($t2)")

        self.write_to_text(f"sub $t1 $t1 $t2")

        self.write_to_text(f"")
        self.create_integer("$t1")       
        self.write_to_text(f"")
        
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    
    @visitor.when(MultNode)
    def visit(self, node : MultNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        self.write_to_text(f"# MULT NODE")
        
        self.write_to_text(f"lw $t1 {o1}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")

        self.write_to_text(f"lw $t2 {o2}($fp)")
        self.write_to_text(f"lw $t2 12($t2)")

        self.write_to_text(f"mul $t1 $t1 $t2")

        self.write_to_text(f"")
        self.create_integer("$t1")       
        self.write_to_text(f"")
        
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    
    @visitor.when(DivNode)
    def visit(self, node : DivNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        self.write_to_text(f"# DIV NODE")
        self.write_to_text(f"lw $t1 {o1}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")

        self.write_to_text(f"lw $t2 {o2}($fp)")
        self.write_to_text(f"lw $t2 12($t2)")

        self.write_to_text(f"div $t1 $t1 $t2")

        self.write_to_text(f"")
        self.create_integer("$t1")       
        self.write_to_text(f"")
        
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    
    @visitor.when(GetAttribNode)
    def visit(self, node : GetAttribNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4        
        # o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4        
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4        
        self.write_to_text(f"# GET-ATTR X = T.Y (SAVES IN X THE ATTR OF OFFSET Y OF T)")# 

        self.write_to_text(f"lw $t0 {o1}($fp)")# EN (T0) tengo el tag
        self.write_to_text(f"addi $t0 $t0 {node.second_op*4 + 12}")# EN (T0) tengo el tag
        self.write_to_text(f"lw $t0 ($t0)")# 
        
        
        # self.write_to_text(f"lw $t1 {o2}($fp)")# EN (T1) tengo el int con el offset del attr
        # self.write_to_text(f"lw $t1 12($t1)")# EN (T1) tengo el valor del offset del attr
        # self.write_to_text(f"sll $t1 $t1 2")# t1 *= 4 pa apuntar al attr
        # self.write_to_text(f"addi $t1 $t1 12")# t1 += 12 pa tener todo lo q hay q deplazarse a artir del inicio del prot
        # self.write_to_text(f"add $t0 $t0 $t1")# a0 apunta al attr
        # self.write_to_text(f"")
        
        self.write_to_text(f"sw $t0 {d}($fp)")# guardo lo que esta en a0 en el destino
        self.write_to_text(f"")

    
    @visitor.when(SetAttribNode)
    def visit(self, node : SetAttribNode):
        instnce = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4        
        self.write_to_text(f"# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)")# 

        self.write_to_text(f"lw $t1 {instnce}($fp)")# EN (T1) tengo la primera pos de la instancia
        self.write_to_text(f"addi $t1 $t1 {12 + node.first_op*4}")# EN (T0) tengo lo q hay q sumar quedarme en el attr desde la instancia
        # self.write_to_text(f"add $t1 $t1 $t0")# EN (T1) estoy parado en el attr  
        self.write_to_text(f"")

        if isinstance(node.second_op, int):
            # self.write_to_text(f"lw $t2 ($t1)")# cargo el attr (Solo puede ser bool o int)
            self.write_to_text(f"li $t0 {node.second_op}")# guardo el value
            # self.write_to_text(f"addi $t2 $t2 12")# me muevo al value attr
            self.write_to_text(f"sw $t0 ($t1)")# guardo el value en el attr
                        
        else:
            value = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4        
            self.write_to_text(f"lw $t2 {value}($fp)")# guardo la ref al value
            self.write_to_text(f"sw $t2 ($t1)")# guardo el value en el attr
            self.write_to_text(f"")
    
    # @visitor.when(GetIndexNode)
    # def visit(self, node : GetIndexNode):
    #     # tomamos la referencia del indexable, luego solo es buscar el offset i y dejarlo que haya ahi en a0
    #     pass
    
    # @visitor.when(SetIndexNode)
    # def visit(self, node : SetIndexNode):
    #     # igual que arriba, pero cambiamos la referencia por x
    #     pass
    
    @visitor.when(AllocateNode)
    def visit(self, node : AllocateNode):
        t = self.types[node.first_op.name].tag
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# ALLOCATE TYPE (MAKES A COPY OF THE TYPE PROTOTYPE)")

        self.write_to_text(f"lw $a0 {8*t}($s6)")
        self.write_to_text(f"jal obj_copy")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")
        
    
    # @visitor.when(ArrayNode)
    # def visit(self, node : ArrayNode):
    #     # reservar en el heap y espacios?????? que tipo tiene el array?????
    #     pass
    
    @visitor.when(TypeOfNode)
    def visit(self, node : TypeOfNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4        
        self.write_to_text(f"lw $t0 {o1}($fp)")# cargo la instancia
        self.write_to_text(f"lw $t0 ($t0)")# me quedo con el tag
        self.write_to_text(f"")
        self.write_to_text(f"sll $t0 $t0 3")# mult * 8 
        self.write_to_text(f"move $t1 $s6")# cargo el prottable
        self.write_to_text(f"add $t0 $t0 $t1")# me paro en el que quiero
        self.write_to_text(f"lw $t0 ($t0)")
        self.write_to_text(f"")
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $t0 {d}($fp)")
        self.write_to_text(f"")
    
    @visitor.when(LabelNode)
    def visit(self, node : LabelNode):
        self.write_to_text(f"{node.name}:")
        self.write_to_text(f"")

    @visitor.when(GotoNode)
    def visit(self, node : GotoNode):
        self.write_to_text(f"# GOTO")
        self.write_to_text(f"b {node.label.name}")
        self.write_to_text(f"")
    
    @visitor.when(GotoIfNode)
    def visit(self, node : GotoIfNode):
        ocond = (self.cargs.index(node.condition) + 3) * 4 if node.condition in self.cargs else self.clocals.index(node.condition) * -4
        self.write_to_text(f"# IF X(BOOL) GOTO DIR({node.label.name})")
        self.write_to_text(f"lw $t0 {ocond}($fp)")
        self.write_to_text(f"lw $t0 12($t0)")
        self.write_to_text(f"bnez $t0 {node.label.name}")
        self.write_to_text(f"")
    
    @visitor.when(CallNode)
    def visit(self, node : CallNode):
        self.write_to_text(f"# STATIC CALL")
        self.write_to_text(f"")
        self.my_push("$fp")# salvo el fp
        self.write_to_text(f"")
        self.write_to_text(f"jal {node.first_op}") # entro a la funcion
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"sw $a0 {d}($fp)") # el retorno de la funcion esta en a0
        self.write_to_text(f"")

    @visitor.when(VCallNode)
    def visit(self, node : VCallNode):
        tg = self.types[node.obj_type].tag
        self.write_to_text(f"# DYNAMIC CALL")
        self.write_to_text(f"lw $v0 4($sp)")
        self.my_push("$fp")# salvo el fp
        if node.ctor:
            self.write_to_text(f"lw $t0 {8*tg + 4}($s6)")
            self.write_to_text(f"jalr $t0")# salto a la direccion que indica el registro
            d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
            self.write_to_text(f"sw $a0 {d}($fp)")# el retoro esta en a0
            self.write_to_text(f"")
        else:
            offset = self.types[node.obj_type].functs[node.function]

            self.write_to_text(f"lw $v0 8($v0)")
            self.write_to_text(f"lw $v0 {offset}($v0)")

            # self.write_to_text(f"lw $t0 {8*tg}($s6)") # cargo el prot
            # self.write_to_text(f"lw $t0 8($t0)")# voy a la tmv
            # self.write_to_text(f"lw $t0 {offset}($t0)")# cargo el metodo pedido
            self.write_to_text(f"jalr $v0")# salto a la direccion que indica el registro
            d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
            self.write_to_text(f"sw $a0 {d}($fp)")# el retoro esta en a0
            self.write_to_text(f"")

    
    # @visitor.when(ArgNode)
    # def visit(self, node : ArgNode):
    #     pass
    
    @visitor.when(ReturnNode)
    def visit(self, node : ReturnNode):
        if node.value:
            offset = (self.cargs.index(node.value) + 3) * 4 if node.value in self.cargs else self.clocals.index(node.value) * -4
            self.write_to_text(f"# SAVES IN $a0 THE RETURN VALUE")
            self.write_to_text(f"lw $a0 {offset}($fp)")
            self.write_to_text(f"")
    
    @visitor.when(LoadNode)
    def visit(self, node : LoadNode):
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.crt_str_cmp(node.msg.value)
        
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    
    @visitor.when(LengthNode)
    def visit(self, node : LengthNode):
        o1 = (self.cargs.index(node.obj) + 3) * 4 if node.obj in self.cargs else self.clocals.index(node.obj) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4    
        self.write_to_text(f"# GIVES A STRING LENGTH (A REF TO INT)")
        self.write_to_text(f"lw $a0 {o1}($fp)")
        self.write_to_text(f"lw $a0 12($t0)") #cargo la ref a int
        self.write_to_text(f"")

        self.write_to_text(f"sw $a0 {d}($fp)")# guardo la ref al int
        self.write_to_text(f"")
        
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode):
        o1 = (self.cargs.index(node.string1) + 3) * 4 if node.string1 in self.cargs else self.clocals.index(node.string1) * -4
        o2 = (self.cargs.index(node.string2) + 3) * 4 if node.string2 in self.cargs else self.clocals.index(node.string2) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4        
        self.write_to_text(f"# CONCAT => STR1 + STR2")

        self.write_to_text(f"lw $v0 {o1}($fp)")
        self.write_to_text(f"lw $v1 {o2}($fp)")# almaceno en v0 y v1 str1 y str2
        self.write_to_text(f"jal str_concat")# almaceno en v0 y v1 str1 y str2
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")


    # @visitor.when(PrefixNode)
    # def visit(self, node : PrefixNode):
    #     pass
    
    @visitor.when(SubstringNode)
    def visit(self, node : SubstringNode):
        o1 = (self.cargs.index(node.msg) + 3) * 4 if node.msg in self.cargs else self.clocals.index(node.msg) * -4
        o2 = (self.cargs.index(node.init) + 3) * 4 if node.init in self.cargs else self.clocals.index(node.init) * -4
        o3 = (self.cargs.index(node.end) + 3) * 4 if node.end in self.cargs else self.clocals.index(node.end) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4    
        self.write_to_text(f"# SUBSTR => CREATES A NEW STRING FROM POS I AND WITH LENGTH X FROM A STRING")

        self.write_to_text(f"lw $v0 {o1}($fp)")# meto el msg en v0
        self.write_to_text(f"lw $t0 {o2}($fp)")# meto el init en t0
        self.write_to_text(f"lw $t1 {o3}($fp)")# meto el len en t1
        self.write_to_text(f"jal str_substr")# 
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")
        
    
    # @visitor.when(ToStrNode)
    # def visit(self, node : ToStrNode):
    #     pass
    
    @visitor.when(EqualStringNode)
    def visit(self, node : EqualStringNode):
        o1 = (self.cargs.index(node.string1) + 3) * 4 if node.string1 in self.cargs else self.clocals.index(node.string1) * -4
        o2 = (self.cargs.index(node.string2) + 3) * 4 if node.string2 in self.cargs else self.clocals.index(node.string2) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# CHECKS IF 2 STRINGS ARE EQUALS (LENGTH FIRST THEN CHAR BY CHAR IF NECESSARY)")
        self.write_to_text(f"lw $v0 {o1}($fp)")# meto el str1 en v0
        self.write_to_text(f"lw $v1 {o2}($fp)")# meto el str2 en v1
        self.write_to_text(f"jal str_eq")#
        self.write_to_text(f"sw $a0 {d}($fp)")# guardo en dest lo q hay en a0 q es un bool de si son iguales
        self.write_to_text(f"")

    @visitor.when(OutStringNode)
    def visit(self, node : OutStringNode):
        o1 = (self.cargs.index(node.source) + 3) * 4 if node.source in self.cargs else self.clocals.index(node.source) * -4
        self.write_to_text(f"# PRINTS A STRING IN CONSOLE")
        self.write_to_text(f"lw $a0 {o1}($fp)")
        self.write_to_text(f"addi $a0 $a0 16")
        self.write_to_text(f"li $v0 4")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")

    @visitor.when(InStringNode)
    def visit(self, node : InStringNode):
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# READS A STRING FROM CONSOLE AND CREATES A STRING OBJECT TO SAVE IT")

        self.write_to_text(f"li $a0 1024")
        self.write_to_text(f"li $a1 1024")# hagoo el buffer lo max posible
        self.write_to_text(f"li $v0 8")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")

        self.write_to_text(f"move $t1 $a0")# guardo el 1er pos del str leido
        self.write_to_text(f"jal len")# salgo con len+2 en t0
        self.write_to_text(f"addi $t0 $t0 -2")
        self.write_to_text(f"")
        self.create_str("$t0")# crea el string con el len leido
        self.write_to_text(f"")

        self.write_to_text(f"move $a1 $a0")# gaurdo la primera pos del str creado
        self.write_to_text(f"addi $a0 $a0 16")
        self.write_to_text(f"")

        self.write_to_text(f"in_str{self.lcounter}:")
        self.write_to_text(f"lb $v0 ($t1)")
        self.write_to_text(f"sb $v0 ($a0)")
        self.write_to_text(f"addi $t1 $t1 1")
        self.write_to_text(f"addi $a0 $a0 1")
        self.write_to_text(f"addi $t0 $t0 -1")
        self.write_to_text(f"bnez $t0 in_str{self.lcounter}")
        self.lcounter += 1
        self.write_to_text(f"")
        self.write_to_text(f"sw $a1 {d}($fp)")
        self.write_to_text(f"")
        


    @visitor.when(OutIntNode)
    def visit(self, node : OutIntNode):
        o1 = (self.cargs.index(node.source) + 3) * 4 if node.source in self.cargs else self.clocals.index(node.source) * -4
        self.write_to_text(f"# PRINTS AN INT")

        self.write_to_text(f"lw $a0 {o1}($fp)")
        self.write_to_text(f"lw $a0 12($a0)")
        self.write_to_text(f"li $v0 1")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")


    @visitor.when(InIntNode)
    def visit(self, node : InIntNode):
        o1 = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# READS AN INT AND SAVE IT IN AN INT OBJECT")
        
        self.write_to_text(f"li $v0 5")
        self.write_to_text(f"syscall")
        self.write_to_text(f"move $t0 $a0")
        self.write_to_text(f"")
        self.create_integer(f"$v0")
        self.write_to_text(f"")
        self.write_to_text(f"sw $a0 {o1}($fp)")
        self.write_to_text(f"")

    # @visitor.when(ReadNode)
    # def visit(self, node : ReadNode):
    #     pass
    
    # @visitor.when(PrintNode)
    # def visit(self, node : PrintNode):
    #     pass
    
    @visitor.when(LessThanNode)
    def visit(self, node : LessThanNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4  
        self.write_to_text(f"# < COMPARES 2 INT OBJECTS")

        self.write_to_text(f"lw $t0 {o1}($fp)")
        self.write_to_text(f"lw $t0 12($t0)")
        self.write_to_text(f"lw $t1 {o2}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")# ENS esnte putno estan guardados los valores de los int
        self.write_to_text(f"slt $t2 $t0 $t1")# pone en t2 1 si t0 < t1, 0 eoc
        self.write_to_text(f"")
        self.create_bool("$t2")
        self.write_to_text(f"")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    @visitor.when(LessThanOrEqualNode)
    def visit(self, node : LessThanOrEqualNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# <= COMPARES 2 INT OBJECTS")

        self.write_to_text(f"lw $t0 {o1}($fp)")
        self.write_to_text(f"lw $t0 12($t0)")
        self.write_to_text(f"lw $t1 {o2}($fp)")
        self.write_to_text(f"lw $t1 12($t1)")
        self.write_to_text(f"sle $t2 $t0 $t1")
        self.write_to_text(f"")
        self.create_bool("$t2")
        self.write_to_text(f"")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")
    
    @visitor.when(EqualNode)
    def visit(self, node : EqualNode):
        o1 = (self.cargs.index(node.first_op) + 3) * 4 if node.first_op in self.cargs else self.clocals.index(node.first_op) * -4
        o2 = (self.cargs.index(node.second_op) + 3) * 4 if node.second_op in self.cargs else self.clocals.index(node.second_op) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4     
        self.write_to_text(f"# COMPARES 2 OBJECTS")

        self.write_to_text(f"lw $t0 {o1}($fp)")
        self.write_to_text(f"lw $t1 {o2}($fp)")
        self.write_to_text(f"seq $t2 $t0 $t1")
        self.write_to_text(f"")
        self.create_bool("$t2")
        self.write_to_text(f"")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")
    
    @visitor.when(TypeNameNode)
    def visit(self, node : TypeNameNode):
        o1 = (self.cargs.index(node.obj) + 3) * 4 if node.obj in self.cargs else self.clocals.index(node.obj) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4   
        self.write_to_text(f"# CREATES A STRING WITH THE TYPE NAME")

        self.write_to_text(f"lw $a0 {o1}($fp)")
        self.write_to_text(f"lw $t7 ($a0)")
        self.write_to_text(f"sll $t7 $t7 2") # t0 *= 4 pa poder moverme en la tabla
        self.write_to_text(f"move $t6 $s5")# Me pAro e el primero tyoename
        self.write_to_text(f"add $t6 $t6 $t7") #Me muevo al de mi tipo
        self.write_to_text(f"lw $a0 ($t6)") #Me muevo al de mi tipo
        self.write_to_text(f"move $a2 $a0")        

        self.write_to_text(f"jal len")# pongo el len+1 en t0
        self.write_to_text(f"")
        self.write_to_text("addi $t7 $t0 16")# creo el str de len en t0
        self.write_to_text(f"li $t6 4")
        self.write_to_text(f"rem $t5 $t7 $t6")
        self.write_to_text(f"sub $t6 $t6 $t5")
        self.write_to_text(f"add $t7 $t7 $t6")# tengo el size mult de 4 en t7
        self.write_to_text(f"move $a0 $t7")

        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $a1 $a0")
        str_tg = self.types["String"].tag
        
        self.write_to_text(f"li $t6 {str_tg}")
        self.write_to_text(f"sw $t6 ($a1)")# pongo el tag
        self.write_to_text(f"sw $t7 4($a1)")#pogo el size
        self.write_to_text(f"lw $t7 {str_tg*8}($s6)")
        self.write_to_text(f"lw $t7 8($t7)")# tengo en t7 la ref a la tmv
        self.write_to_text(f"sw $t7 8($a1)")# pongo la ref a la  tmv
        self.write_to_text(f"addi $t0 $t0 -1")# tengo el len en t0
        self.create_integer(f"$t0")
        self.write_to_text(f"sw $a0 12($a1)")# guardo el int len


        self.write_to_text(f"move $a0 $a1")
        self.write_to_text(f"addi $a1 $a1 16")
        self.write_to_text(f"")

        self.write_to_text(f"type_name{self.lcounter}:")
        self.write_to_text(f"lb $v0 ($a2)")
        self.write_to_text(f"sb $v0 ($a1)")
        self.write_to_text(f"addi $a1 $a1 1")
        self.write_to_text(f"addi $a2 $a2 1")
        self.write_to_text(f"addi $t0 $t0 -1")
        self.write_to_text(f"bnez $t0 type_name{self.lcounter}")
        self.lcounter += 1
        self.write_to_text(f"")
        self.write_to_text(f"li $t7 0")
        self.write_to_text(f"sb $t7 ($a1)")        

        
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

           

    @visitor.when(CopyNode)
    def visit(self, node : CopyNode):
        o1 = (self.cargs.index(node.obj) + 3) * 4 if node.obj in self.cargs else self.clocals.index(node.obj) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"# COPIES AN OBJECT")

        self.write_to_text(f"lw $a0 {o1}($fp)")# en a0 el tag del prototipo
        self.write_to_text(f"sll $t0 $a0 3")#  a0 *= 8 pa pararme en el prot
        self.write_to_text(f"lw $t1 ($s6)")# Me pAro e el primero prot
        self.write_to_text(f"add $t1 $t1 $t0") #Me muevo al de mi tipo
        self.write_to_text(f"move $a0 $t1") #lo pongo en a0
        
        self.write_to_text(f"jal obj_copy")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")


    @visitor.when(AbortNode)
    def visit(self, node : AbortNode):
        self.write_to_text(f"# ABORT")

        self.write_to_text(f"la $a0 _abort")
        
        self.write_to_text(f"li $v0 4")
        self.write_to_text(f"syscall")
        self.write_to_text(f"li $v0 10")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")
    
    @visitor.when(ParentTypeNode)
    def visit(self, node : ParentTypeNode):
        self.write_to_text(f"# PARENT TYPE")
    #dest typeobj(result de typeof)
        o1 = (self.cargs.index(node.type_obj) + 3) * 4 if node.type_obj in self.cargs else self.clocals.index(node.type_obj) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        self.write_to_text(f"lw $a0 {o1}($fp)")
        self.write_to_text(f"jal get_parent_prot")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    @visitor.when(IsTypeNode)
    def visit(self, node : IsTypeNode):
        self.write_to_text(f"# IS TYPE")
    #dest, typeobj(result de typeof), typename
        o1 = (self.cargs.index(node.type_obj) + 3) * 4 if node.type_obj in self.cargs else self.clocals.index(node.type_obj) * -4
        d = (self.cargs.index(node.dest) + 3) * 4 if node.dest in self.cargs else self.clocals.index(node.dest) * -4
        tg = self.types[node.type_name].tag
        self.write_to_text(f"li $t0 {tg}")
        self.write_to_text(f"lw $t1 {o1}($fp)")
        self.write_to_text(f"lw $t1 ($t1)")
        self.write_to_text(f"seq $t2 $t1 $t0")
        self.create_bool("$t2")
        self.write_to_text(f"sw $a0 {d}($fp)")
        self.write_to_text(f"")

    ######################################################################################################################################
    ######################################################################################################################################
    ######################################################################################################################################
    ######################################################################################################################################


    # OBJECT
    # Hace una copia del prot que esta en a0 y deja esa ref en a0
    def object_copy(self):# OK
        self.write_to_text(f"# DECLARATION OF THE OBEJCT.COPY AUX BODY")
        self.write_to_text(f"obj_copy:")
        self.write_to_text(f"lw $s1 4($a0)")# cojo el size
        self.write_to_text(f"")

        self.write_to_text(f"add $gp $gp $s1")# Reservar mem para el obj
        # self.write_to_text(f"blt $s7 $gp mem_error")
        self.write_to_text(f"sub $s0 $gp $s1")
        self.write_to_text(f"")

        # self.write_to_text(f"add $t0 $t0 $a0")# find limit of copy ???????
        self.write_to_text(f"move $s2 $s0")# save src
        self.write_to_text(f"")

        self.write_to_text(f"cpy_loop: #loop pa copiar el obj")
        self.write_to_text(f"lw $s3 0($a0)")
        self.write_to_text(f"sw $s3 0($s2)")# copy
        self.write_to_text(f"")

        self.write_to_text(f"addiu $a0 $a0 4")
        self.write_to_text(f"addiu $s2 $s2 4")# update
        self.write_to_text(f"addi $s1 $s1 -4")#
        self.write_to_text(f"")

        self.write_to_text(f"bnez $s1 cpy_loop")
        self.write_to_text(f"")

        self.write_to_text(f"move $a0 $s0")# dejo en a0 el objeto copiado
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")

    
    # STRING
    # Se pasan 2 string en v0 v1 y se retorna en a1
    def str_concat(self):
        self.write_to_text(f"# DECLARATION OF THE STRING.CONCAT AUX BODY")

        self.write_to_text(f"str_concat:")
        self.write_to_text(f"move $t2 $ra")
        self.write_to_text(f"")
        
        self.write_to_text(f"lw $t6 12($v0)")# Pongo en t6 el campo int de str1
        self.write_to_text(f"lw $t6 12($t6)")# Pongo en t6 el valor del int cargado en la instr anterior
        self.write_to_text(f"lw $t7 12($v1)")
        self.write_to_text(f"lw $t7 12($t7)")
        self.write_to_text(f"")

        self.write_to_text(f"add $a0 $t6 $t7")
        self.write_to_text(f"addi $a0 $a0 17")# TENGO EL SIZE en a0
        self.write_to_text(f"li $t5 4")
        self.write_to_text(f"rem $t4 $a0 $t5")# cojo el resto
        self.write_to_text(f"sub $t5 $t5 $t4")# se lo resto a 4 pa completar
        self.write_to_text(f"add $a0 $a0 $t5")# en a0 hay un size mult de 4
        
        self.write_to_text(f"move $t4 $a0")# guardo en t4 el size

        self.write_to_text(f"jal mem_alloc")# Tengo en a0 el inicio de al mem pal nuevo str
        self.write_to_text(f"move $a1 $a0")
        self.write_to_text(f"move $a3 $a0")
        
        self.write_to_text(f"lw $t5 ($v0)")# cargo el str tag
        self.write_to_text(f"sw $t5 ($a1)")# guardo el str tag
        self.write_to_text(f"sw $t4 4($a1)")# guardo el size
        self.write_to_text(f"lw $t5 8($v0)")# cargo la tmv
        self.write_to_text(f"sw $t5 8($a1)")# la guardo

        self.write_to_text(f"add $t5 $t6 $t7")# guardo el len
        self.create_integer(f"$t5")# tengo en a0 la ref al int del len
        self.write_to_text(f"sw $a0 12($a1)")# guardo el int len

        self.write_to_text(f"move $a0 $a1")
        
        self.write_to_text(f"addi $a1 $a1 16")# me paro en la primera posicion del str (luego de los ca,pos del prot)
        self.write_to_text(f"addi $v0 $v0 16")# me paro en la primera posicion del str (luego de los ca,pos del prot)
        self.write_to_text(f"addi $v1 $v1 16")# me paro en la primera posicion del str (luego de los ca,pos del prot)
                

        self.write_to_text(f"strcat_loop:")# Copiar str 1 en a1 (a0 apunta al inicio de a1)
        self.write_to_text(f"lb $t5 ($v0)")
        self.write_to_text(f"sb $t5 ($a1)")
        self.write_to_text(f"addi $a1 $a1 1")
        self.write_to_text(f"addi $v0 $v0 1")
        self.write_to_text(f"addi $t6 $t6 -1")
        self.write_to_text(f"bnez $t6 strcat_loop")
        self.write_to_text(f"")

        self.write_to_text(f"strcat_loop2:")# Copiar str 2 en a0 por donde se quedo
        self.write_to_text(f"lb $t5 ($v1)")
        self.write_to_text(f"sb $t5 ($a1)")
        self.write_to_text(f"addi $v1 $v1 1")
        self.write_to_text(f"addi $a1 $a1 1")
        self.write_to_text(f"addi $t7 $t7 -1")
        self.write_to_text(f"bnez $t7 strcat_loop2")
        self.write_to_text(f"")
        # ya se copiaron los 2 str, falta poner el 0
        self.write_to_text(f"li $t5 0")
        self.write_to_text(f"sb $t5 ($a1)")        
        self.write_to_text(f"move $ra $t2")        
        # self.write_to_text(f"move $a0 $a3")        

        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")

    # TENGO EN V0 el self que es el str, en T0 la pos inicial, en T1 el len a copiar y retono en A0
    def str_substr(self):
        self.write_to_text(f"# DECLARATION OF THE STRING.SUBSTR AUX BODY")

        self.write_to_text(f"str_substr:")
        self.write_to_text(f"move $t7 $ra")
        
        self.write_to_text(f"lw $t0 12($t0)")#  pos inicial
        self.write_to_text(f"lw $t1 12($t1)")# Guardo el valor del len
        self.write_to_text(f"")

        self.write_to_text(f"add $t3 $t0 $t1")# pos + len = t3 <- ultima pos del substr
        self.write_to_text(f"lw $t4 12($v0)")#
        self.write_to_text(f"lw $t4 12($t4)")# Guardo el valor del len del str
        self.write_to_text(f"bge $t3 $t4 substr_error")#
        self.write_to_text(f"")

        self.write_to_text(f"addi $a0 $t1 17")
        self.write_to_text(f"li $t5 4")
        self.write_to_text(f"rem $t4 $a0 $t5")
        self.write_to_text(f"sub $t5 $t5 $t4")
        self.write_to_text(f"add $a0 $a0 $t5")# dejo en a0 un size mult de 4

        self.write_to_text(f"move $t4 $a0")
        self.write_to_text(f"jal mem_alloc")
        self.write_to_text(f"move $a1 $a0")# guardo la ref a la mem reservada

        self.write_to_text(f"lw $t5 ($v0)")
        self.write_to_text(f"sw $t5 ($a1)")
        self.write_to_text(f"sw $t4 4($a1)")
        self.write_to_text(f"lw $t5 8($v0)")
        self.write_to_text(f"sw $t5 8($a1)")# armo el prot

        self.create_integer(f"$t1")
        self.write_to_text(f"sw $a0 12($a1)")#
        
        self.write_to_text(f"move $a0 $a1")

        self.write_to_text(f"addi $t0 $t0 16")
        self.write_to_text(f"add $v0 $v0 $t0")
        self.write_to_text(f"addi $a1 $a1 16")
        

        self.write_to_text(f"substr_loop:")#
        self.write_to_text(f"lb $t5 ($v0)")
        self.write_to_text(f"sb $t5 ($a1)")
        self.write_to_text(f"addi $v0 $v0 1")
        self.write_to_text(f"addi $a1 $a1 1")
        self.write_to_text(f"addi $t1 $t1 -1")
        self.write_to_text(f"bnez $t1 substr_loop")
        self.write_to_text(f"")

        self.write_to_text(f"li $t5 0")
        self.write_to_text(f"sb $t5 ($a1)")        
        self.write_to_text(f"move $ra $t7")        

        self.write_to_text(f"jr $ra")
        

    # Voy a tener en el v0 el str 1, en el v1 el str 2,  ret el bool en a0
    def str_eq(self):
        self.write_to_text(f"# DECLARATION OF THE STRING.EQUALS AUX BODY")

        self.write_to_text(f"str_eq:")
        self.write_to_text(f"")
        
        self.write_to_text(f"lw $t6 12($v0)")# Pongo en t6 el campo int de str1
        self.write_to_text(f"lw $t6 12($t6)")# Pongo en t6 el valor del int cargado en la instr anterior
        self.write_to_text(f"lw $t7 12($v1)")
        self.write_to_text(f"lw $t7 12($t7)")
        self.write_to_text(f"")

        self.write_to_text(f"bne $t7 $t6 str_eq_false") # Comp que los len son iguales
        self.write_to_text(f"beqz $t7 str_eq_true") # si son iguales y miden 0 son iguales
        self.write_to_text(f"")
        
        self.write_to_text(f"addi $v0 $v0 16")
        self.write_to_text(f"addi $v1 $v1 16")
        self.write_to_text(f"move $t5 $t7")
        self.write_to_text(f"")

        self.write_to_text(f"str_eq_loop:")
        self.write_to_text(f"lb $t7 ($v0)")
        self.write_to_text(f"lb $t6 ($v1)")
        self.write_to_text(f"bne $t7 $t6 str_eq_false")
        self.write_to_text(f"addi $v0 $v0 1")
        self.write_to_text(f"addi $v1 $v1 1")
        self.write_to_text(f"addi $t5 $t5 -1")
        self.write_to_text(f"bnez $t5 str_eq_loop")
        self.write_to_text(f"")

        self.write_to_text(f"str_eq_true:")
        self.write_to_text(f"li $t6 1")
        self.create_bool("$t6")
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")

        self.write_to_text(f"str_eq_false:")
        self.write_to_text(f"li $t6 0")
        self.create_bool("$t6")
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")


# RECIBE EN A0 EL STR Y DEVUELVE EN T0 el len+1($0) (EN caso del Read es +2 por el \n de pinga ese)
    def length(self):
        self.write_to_text(f"# DECLARATION OF THE LEN AUX BODY")
        
        self.write_to_text(f"len:")
        self.write_to_text(f"li $t0 0")
        self.write_to_text(f"len_loop:")
        self.write_to_text(f"lb $t7 ($a0)")
        self.write_to_text(f"addi $t0 $t0 1")
        self.write_to_text(f"addi $a0 $a0 1")
        self.write_to_text(f"bne $t7 $0 len_loop")
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")

    # Input espacio a reservar en $a0
# Output direccion de memoria reservada en $a0
    def mem_alloc(self):# OK
        self.write_to_text(f"# DECLARATION OF THE MEM-ALLOC BODY")

        self.write_to_text(f"mem_alloc:")
        self.write_to_text(f"add $gp $gp $a0")
        self.write_to_text(f"blt $gp $s7 mem_alloc_end")# si se pasa del limite de memoria error
        self.write_to_text(f"j mem_error")
        self.write_to_text(f"mem_alloc_end:")
        self.write_to_text(f"sub $a0 $gp $a0")    
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")

# en a0 tengo el la instancia
    def get_parent_prot(self):
        self.write_to_text(f"# GET PARENT PROTOTYPE") #
        self.write_to_text(f"get_parent_prot:")
        self.write_to_text(f"lw $t0 ($a0)")
        self.write_to_text(f"sll $t0 $t0 2")# mult por 4 pa tener el offset
        self.write_to_text(f"lw $t0 ($s4)")
        self.write_to_text(f"move $a0 $t0")
        self.write_to_text(f"jr $ra")
        self.write_to_text(f"")



# RUNTIME ERROR FUNCT
    #DIV POR 0
    def zero_error(self):
        self.write_to_text(f"# DECLARATION OF THE ZERO-DIV RE BODY")

        self.write_to_text(f"zero_error:")
        self.write_to_text(f"la $a0 _zero")
        self.write_to_text(f"")

        self.write_to_text(f"li $v0 4")
        self.write_to_text(f"syscall")
        self.write_to_text(f"li $v0 10")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")

    def substr_error(self):
        self.write_to_text(f"# DECLARATION OF THE SUBSTR-IND.OUT.OF.RANGE RE BODY")

        self.write_to_text(f"substr_error:")
        self.write_to_text(f"la $a0 _substr")
        self.write_to_text(f"")
        
        self.write_to_text(f"li $v0 4")
        self.write_to_text(f"syscall")
        self.write_to_text(f"li $v0 10")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")
    
    def mem_error(self):
        self.write_to_text(f"# DECLARATION OF THE MEMORY-OVERFLOW RE BODY")
        self.write_to_text(f"mem_error:")
        self.write_to_text(f"la $a0 _mem")
        self.write_to_text(f"")
        
        self.write_to_text(f"li $v0 4")
        self.write_to_text(f"syscall")
        self.write_to_text(f"li $v0 10")
        self.write_to_text(f"syscall")
        self.write_to_text(f"")


    def utils_functs(self):
        self.mem_alloc()
        self.get_parent_prot()
        self.object_copy()
        self.str_eq()
        self.str_concat()
        self.str_substr()
        self.length()
        self.zero_error()
        self.mem_error()
        self.substr_error()