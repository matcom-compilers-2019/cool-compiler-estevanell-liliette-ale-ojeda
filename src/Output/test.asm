.data
_abort: .asciiz "Program Aborted"
_zero: .asciiz "0 Division Error"
_substr: .asciiz "Substr Length Error"
_mem: .asciiz "Memory Error"

_Void: .asciiz "Void"
_Object: .asciiz "Object"
_Int: .asciiz "Int"
_Bool: .asciiz "Bool"
_String: .asciiz "String"
_IO: .asciiz "IO"
_Main: .asciiz "Main"
# VISITING ALL THE DATA NODES
data_0: .asciiz ""
.text
main:
move $s7 $gp
addi $s7 $s7 50000
# SAVE A REFERENCE TO ALL THE PROTOTYPES IN $s6
li $a0 56
jal mem_alloc
move $s6 $a0

# SAVE A REFERENCE TO ALL THE TYPES-NAMES IN $s5
li $a0 28
jal mem_alloc
move $s5 $a0

# SAVE A REFERENCE TO ALL THE PARENTS PROTOTYPES IN $s4
li $a0 28
jal mem_alloc
move $s4 $a0

# VISITING ALL THE TYPES NODES
#Void
li $a0 12
jal mem_alloc
move $t0 $a0
li $t1 0
sw $t1 ($t0)
li $t1 12
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 0
jal mem_alloc


sw $a0 8($t0)
sw $t0 0($s6)

la $t0 ctor_Void
sw $t0 4($s6)

la $t0 _Void
sw $t0 0($s5)

lw $t0 0($s6)
sw $t0 0($s4)

#Object
li $a0 12
jal mem_alloc
move $t0 $a0
li $t1 1
sw $t1 ($t0)
li $t1 12
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 12
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)


sw $a0 8($t0)
sw $t0 8($s6)

la $t0 ctor_Object
sw $t0 12($s6)

la $t0 _Object
sw $t0 4($s5)

lw $t0 0($s6)
sw $t0 4($s4)

#Int
li $a0 16
jal mem_alloc
move $t0 $a0
li $t1 2
sw $t1 ($t0)
li $t1 16
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 12
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)


sw $a0 8($t0)
sw $t0 16($s6)

la $t0 ctor_Int
sw $t0 20($s6)

la $t0 _Int
sw $t0 8($s5)

lw $t0 8($s6)
sw $t0 8($s4)

#Bool
li $a0 16
jal mem_alloc
move $t0 $a0
li $t1 3
sw $t1 ($t0)
li $t1 16
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 12
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)


sw $a0 8($t0)
sw $t0 24($s6)

la $t0 ctor_Bool
sw $t0 28($s6)

la $t0 _Bool
sw $t0 12($s5)

lw $t0 8($s6)
sw $t0 12($s4)

#String
li $a0 16
jal mem_alloc
move $t0 $a0
li $t1 4
sw $t1 ($t0)
li $t1 16
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 24
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 concat_3
sw $t1 16($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 substr_4
sw $t1 20($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 length_5
sw $t1 24($a0)


sw $a0 8($t0)
sw $t0 32($s6)

la $t0 ctor_String
sw $t0 36($s6)

la $t0 _String
sw $t0 16($s5)

lw $t0 8($s6)
sw $t0 16($s4)

#IO
li $a0 12
jal mem_alloc
move $t0 $a0
li $t1 5
sw $t1 ($t0)
li $t1 12
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 28
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 out_string_6
sw $t1 16($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 out_int_7
sw $t1 20($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 in_string_8
sw $t1 24($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 in_int_9
sw $t1 28($a0)


sw $a0 8($t0)
sw $t0 40($s6)

la $t0 ctor_IO
sw $t0 44($s6)

la $t0 _IO
sw $t0 20($s5)

lw $t0 8($s6)
sw $t0 20($s4)

#Main
li $a0 16
jal mem_alloc
move $t0 $a0
li $t1 6
sw $t1 ($t0)
li $t1 16
sw $t1 4($t0)

# CREATING VIRTUAL TABLE METHOD
li $a0 20
jal mem_alloc

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 type_name_0
sw $t1 4($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 copy_1
sw $t1 8($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 abort_2
sw $t1 12($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 sum_10
sw $t1 16($a0)

# SAVING THE OFFSET OF EVERY FUNCTION IN THE TYPE
la $t1 main_11
sw $t1 20($a0)


sw $a0 8($t0)
sw $t0 48($s6)

la $t0 ctor_Main
sw $t0 52($s6)

la $t0 _Main
sw $t0 24($s5)

lw $t0 8($s6)
sw $t0 24($s4)

jal obj_copy
move $a2 $a0
# PUSHING $a0
sw $a0 0($sp)
addiu $sp $sp -4
# PUSHING $fp
sw $fp 0($sp)
addiu $sp $sp -4
la $t0 52($s6)
jalr $t0
addi $sp $sp -8
lw $t0 48($s6)
lw $t0 8($t0)
la $t0 20($t0)
jalr $t0
b _end_main
# END MAIN
# VISITING ALL THE FUNCTIONS NODES
ctor_Void:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

ctor_Object:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

type_name_0:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# CREATES A STRING WITH THE TYPE NAME
lw $a0 12($fp)
lw $t0 ($a0)
sll $t0 $t0 2
lw $t1 ($s5)
add $t1 $t1 $t0
la $a0 ($t1)
move $a1 $a0
jal len

# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE
addi $t5 $t0 1
# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t0 12($a0)
move $a1 $a0
li $a0 0
addi $t5 $t5 16
add $a0 $a0 $t5
jal mem_alloc
li $t6 4
sw $t6 ($a0)
sw $t5 4($a0)
sw $a1 12($a0)
lw $t6 32($s6)
lw $t7 8($t6)
sw $t7 8($a0)
move $t0 $t0

move $t1 $a0
addi $a0 $a0 16

type_name0:
lb $v0 ($a1)
sb $v0 ($a0)
addi $a1 $a1 1
addi $a0 $a0 1
addi $t0 $t0 -1
bnez $t0 in_str0

sw $t1 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

copy_1:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# COPIES AN OBJECT
lw $a0 12($fp)
sll $t0 $a0 3
lw $t1 ($s6)
add $t1 $t1 $t0
move $a0 $t1
jal obj_copy
sw $a0 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

abort_2:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# ABORT
la $a0 _abort
li $v0 4
syscall
li $v0 10
syscall

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

ctor_Int:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 12($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 ($t1)
li $t0 0
addi $t2 $t2 12
sw $t0 ($t2)
lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

ctor_Bool:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 12($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 ($t1)
li $t0 0
addi $t2 $t2 12
sw $t0 ($t2)
lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

ctor_String:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# LOADS A MSG TO A DESTINATION
li $t0 0

# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE
addi $t5 $t0 1
# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t0 12($a0)
move $a1 $a0
li $a0 0
addi $t5 $t5 16
add $a0 $a0 $t5
jal mem_alloc
li $t6 4
sw $t6 ($a0)
sw $t5 4($a0)
sw $a1 12($a0)
lw $t6 32($s6)
lw $t7 8($t6)
sw $t7 8($a0)
move $t0 $t0

addi $a0 $a0 16
la $a1 data_0
li $t0 0

str_load1:
lb $t1 ($a1)
sb $t1 ($a0)
addi $a1 $a1 1
addi $a0 $a0 1
addi $t0 $t0 -1
bnez $t0 str_load1

sw $a0 12($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

concat_3:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# CONCAT => STR1 + STR2
lw $v0 12($fp)
lw $v1 16($fp)
jal str_concat
sw $a0 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 20
jr $ra

substr_4:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# SUBSTR => CREATES A NEW STRING FROM POS I AND WITH LENGTH X FROM A STRING
lw $v0 12($fp)
lw $t0 16($fp)
lw $t1 20($fp)
jal str_substr
sw $a0 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 24
jr $ra

length_5:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# GIVES A STRING LENGTH (A REF TO INT)
lw $a0 12($fp)
lw $a0 12($t0)

sw $a0 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

ctor_IO:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 12
jr $ra

out_string_6:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# PRINTS A STRING IN CONSOLE
lw $a0 16($fp)
addi $a0 $a0 16
li $v0 4
syscall

# SAVES IN $a0 THE RETURN VALUE
lw $a0 12($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

out_int_7:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp 0
# PRINTS AN INT
lw $a0 16($fp)
lw $a0 12($a0)
li $v0 1
syscall

# SAVES IN $a0 THE RETURN VALUE
lw $a0 12($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

in_string_8:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# READS A STRING FROM CONSOLE AND CREATES A STRING OBJECT TO SAVE IT
li $a0 1024
li $a1 1024
li $v0 8
syscall

move $t1 $a0
jal len
addi $t0 $t0 -2

# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE
addi $t5 $t0 1
# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t0 12($a0)
move $a1 $a0
li $a0 0
addi $t5 $t5 16
add $a0 $a0 $t5
jal mem_alloc
li $t6 4
sw $t6 ($a0)
sw $t5 4($a0)
sw $a1 12($a0)
lw $t6 32($s6)
lw $t7 8($t6)
sw $t7 8($a0)
move $t0 $t0

move $a1 $a0
addi $a0 $a0 16

in_str2:
lb $v0 ($t1)
sb $v0 ($a0)
addi $t1 $t1 1
addi $a0 $a0 1
addi $t0 $t0 -1
bnez $t0 in_str2

sw $a1 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

in_int_9:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -4
# READS AN INT AND SAVE IT IN AN INT OBJECT
li $v0 5
syscall
move $t0 $a0

# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t0 12($a0)

sw $a0 0($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 0($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 16
jr $ra

ctor_Main:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -8
# ALLOCATE TYPE (MAKES A COPY OF THE TYPE PROTOTYPE)
lw $a0 16($s6)
jal obj_copy
sw $a0 0($fp)

lw $t0 0($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
la $t0 20($s6)
jalr $t0
sw $a0 -4($fp)

# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 12($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 0($fp)
sw $t2 ($t1)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 20
jr $ra

sum_10:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -16
# ALLOCATE TYPE (MAKES A COPY OF THE TYPE PROTOTYPE)
lw $a0 16($s6)
jal obj_copy
sw $a0 0($fp)

lw $t0 0($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
la $t0 20($s6)
jalr $t0
sw $a0 -4($fp)

# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 0($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 ($t1)
li $t0 1
addi $t2 $t2 12
sw $t0 ($t2)
# PLUS NODE
lw $t1 20($fp)
lw $t1 12($t1)
lw $t2 0($fp)
lw $t2 12($t2)
add $t1 $t1 $t2

# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw t1 12($a0)

sw $a0 -8($fp)

# PLUS NODE
lw $t1 16($fp)
lw $t1 12($t1)
lw $t2 -8($fp)
lw $t2 12($t2)
add $t1 $t1 $t2

# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw t1 12($a0)

sw $a0 -12($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 -12($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 36
jr $ra

main_11:
# PUSHING $ra
sw $ra 0($sp)
addiu $sp $sp -4

move $fp $sp

addi $sp $sp -32
lw $t0 12($fp)
lw $t0 ($t0)

sll $t0 $t0 2
lw $t1 ($s6)
add $t0 $t0 $t1

sw $t0 -4($fp)

# IS TYPE
li $t0 0
lw $t1 -4($fp)
seq $t2 $t1 $t0
# CREATE A NEW BOOL PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 24($s6)
jal obj_copy
sw $t2 12($a0)
sw $a0 -8($fp)

# IF X(BOOL) GOTO DIR(label_0)
lw $t0 -8($fp)
lw $t0 12($t0)
bnez $t0 label_0

# ALLOCATE TYPE (MAKES A COPY OF THE TYPE PROTOTYPE)
lw $a0 16($s6)
jal obj_copy
sw $a0 -12($fp)

lw $t0 -12($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
la $t0 20($s6)
jalr $t0
sw $a0 -16($fp)

# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 -12($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 ($t1)
li $t0 1
addi $t2 $t2 12
sw $t0 ($t2)
# ALLOCATE TYPE (MAKES A COPY OF THE TYPE PROTOTYPE)
lw $a0 16($s6)
jal obj_copy
sw $a0 -20($fp)

lw $t0 -20($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
la $t0 20($s6)
jalr $t0
sw $a0 -24($fp)

# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 -20($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 ($t1)
li $t0 11
addi $t2 $t2 12
sw $t0 ($t2)
lw $t0 -20($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $t0 -12($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $t0 12($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
lw $v0 8($v0)
lw $v0 16($v0)
jalr $v0
sw $a0 0($fp)

# GOTO
b label_1

label_0:

lw $t0 12($fp)

# PUSHING $t0
sw $t0 0($sp)
addiu $sp $sp -4

lw $v0 4($sp)
# DYNAMIC CALL
lw $v0 8($v0)
lw $v0 12($v0)
jalr $v0
sw $a0 0($fp)

# GOTO
b label_1

label_1:

# SET-ATTR A.Y = X (STORES X AS THE ATTR OF OFFSET Y OF INSTANCE A)
lw $t1 12($fp)
li $t0 12
add $t1 $t1 $t0

lw $t2 0($fp)
sw $t2 ($t1)

# GET-ATTR X = T.Y (SAVES IN X THE ATTR OF OFFSET Y OF T)
lw $t0 12($fp)
addi $t0 $t0 12
sw $t0 -28($fp)

# SAVES IN $a0 THE RETURN VALUE
lw $a0 -28($fp)

lw $ra 4($fp)
lw $fp 8($fp)
addi $sp $sp 44
jr $ra

# CREATING SOME UTIL FUNCTIONS
# DECLARATION OF THE MEM-ALLOC BODY
mem_alloc:
add $gp $gp $a0
blt $gp $s7 mem_alloc_end
j mem_error
mem_alloc_end:
sub $a0 $gp $a0
jr $ra

# GET PARENT PROTOTYPE
get_parent_prot:
lw $t0 ($a0)
sll $t0 $t0 2
lw $t0 ($s4)
move $a0 $t0
jr $ra

# DECLARATION OF THE OBEJCT.COPY AUX BODY
obj_copy:
lw $t0 4($a0)

add $gp $gp $t0
blt $s7 $gp mem_error
sub $a1 $gp $t0

add $t0 $t0 $a0
move $t1 $a1

cpy_loop:
lw $v0 0($a0)
sw $v0 0($t1)

addiu $a0 $a0 4
addiu $t1 $t1 4

bne $a0 $t0 cpy_loop

move $a0 $a1
jr $ra

# DECLARATION OF THE STRING.EQUALS AUX BODY
str_eq:

lw $t0 12($v0)
lw $t0 12($t0)
lw $t1 12($v1)
lw $t1 12($t1)

bne $t1 $t2 str_eq_false
beqz $t1 str_eq_true

addi $v0 $v0 16
addi $v1 $v1 16
move $t2 $t1

str_eq_loop:
lb $t1 ($v0)
lb $t2 ($v1)
bne $t1 $t2 str_eq_false
addi $v0 $v0 1
addi $v1 $v1 1
addi $t0 $t0 -1
bnez $t0 str_eq_loop

str_eq_true:
li $t0 1
# CREATE A NEW BOOL PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 24($s6)
jal obj_copy
sw $t0 12($a0)
jr $ra

str_eq_false:
li $t0 0
# CREATE A NEW BOOL PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 24($s6)
jal obj_copy
sw $t0 12($a0)
jr $ra

# DECLARATION OF THE STRING.CONCAT AUX BODY
str_concat:

lw $t0 12($v0)
lw $t0 12($t0)
lw $t1 12($v1)
lw $t1 12($t1)

add $t2 $t0 $t1

# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE
addi $t5 $t2 1
# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t2 12($a0)
move $a1 $a0
li $a0 0
addi $t5 $t5 16
add $a0 $a0 $t5
jal mem_alloc
li $t6 4
sw $t6 ($a0)
sw $t5 4($a0)
sw $a1 12($a0)
lw $t6 32($s6)
lw $t7 8($t6)
sw $t7 8($a0)
move $t0 $t2

move $a1 $a0

addi $a0 $a0 16
addi $v0 $v0 16
addi $v1 $v1 16

lw $t0 12($v0)
lw $t0 12($t0)

strcat_loop2:
lb $t1 ($v0)
sb $t1 ($a1)
addi $a1 $a1 1
addi $v0 $v0 1
addi $t0 $t0 -1
bnez $t0 strcat_loop2

addiu $a0 $a0 -1

lw $t0 12($v0)
lw $t0 12($t0)

strcat_loop3:
lb $t1 ($v1)
sb $t1 ($a1)
addi $v1 $v1 1
addi $a1 $a1 1
addi $t0 $t0 -1
bnez $t0 strcat_loop3

jr $ra

# DECLARATION OF THE STRING.SUBSTR AUX BODY
str_substr:

lw $t0 12($t0)
lw $t1 12($t1)

add $t3 $t1 $t2
lw $t4 12($v0)
lw $t4 12($t4)
bge $t3 $t4 substr_error

# CREATE A NEW STRING PROTOYPE IN HEAP AND STORE ITS VALUE
addi $t5 $t1 1
# CREATE A NEW INT PROTOYPE IN HEAP AND STORE ITS VALUE
lw $a0 16($s6)
jal obj_copy
sw $t1 12($a0)
move $a1 $a0
li $a0 0
addi $t5 $t5 16
add $a0 $a0 $t5
jal mem_alloc
li $t6 4
sw $t6 ($a0)
sw $t5 4($a0)
sw $a1 12($a0)
lw $t6 32($s6)
lw $t7 8($t6)
sw $t7 8($a0)
move $t0 $t1

move $a1 $a0
addi $v0 $v0 16
addi $a1 $a1 16
add $v0 $v0 $t0

substr_loop:
lb $t2 ($v0)
sb $t2 ($a1)
addi $v0 $v0 1
addi $a1 $a1 1
addi $t1 $t1 -1
bnez $t1 substr_loop

sw $0 ($a1)
jr $ra

# DECLARATION OF THE LEN AUX BODY
len:
li $t0 0
len_loop:
lb $t1 ($a0)
addi $t0 $t0 1
addi $a0 $a0 1
bne $t1 $0 len_loop
jr $ra

# DECLARATION OF THE ZERO-DIV RE BODY
zero_error:
la $a0 _zero

li $v0 4
syscall
li $v0 10
syscall

# DECLARATION OF THE MEMORY-OVERFLOW RE BODY
mem_error:
la $a0 _mem

li $v0 4
syscall
li $v0 10
syscall

# DECLARATION OF THE SUBSTR-IND.OUT.OF.RANGE RE BODY
substr_error:
la $a0 _substr

li $v0 4
syscall
li $v0 10
syscall

_end_main:
