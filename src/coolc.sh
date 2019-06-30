# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE = $1
OUTPUT_FILE = ${INPUT_FILE:0: -2}mips


# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool-Compiler-X v1.2"   # Recuerde cambiar estas
echo "Copyright (c) 2019: Ernesto L. Estevanell, Liliette Chiu, Alejandro Ojeda"    # líneas a los valores correctos

# Llamar al compilador
python CoolCompilerX $1 $2
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

