import sys
import Sintax.lexer as lex
import Sintax.parsing as psr
import Utils.settings as st
import Semantics.semantics as sem
from GeneratingCIL.CILgenerator import CilGenerator
from GeneratingMIPS.MIPSgenerator import MipsGenerator

class CoolCompilerX:
    def __init__(self, output_file = "Output/output.mips"):
        self.lexer = lex.Lexer()
        self.lexer.build()
        self.parser = psr.CoolParsX()
        self.parser.build(lexer = self.lexer)
        self.latest_parser_output = None
        self.cgen = None
        self.mgen = None
        self.sematic_analizer = None
        self.output_file = output_file

    def test_lexer(self, code = None):
        if not code:
            lex.run_test(self.lexer)

    def parse(self, code:str):
        output = self.parser.parse(code)
        if self.parser.error_list:
            print("Errors where detected while parsing:")
            for error in self.parser.error_list:
                print(error)
            raise Exception("Parsing Check Fail")
        self.latest_parser_output = output
        return self.latest_parser_output

    def run_semantics(self):
        if not self.latest_parser_output:
            raise Exception("No previous latest output found")
        self.sematic_analizer = sem.Semantics(self.latest_parser_output)
        self.sematic_analizer.check_semantics()
        if self.sematic_analizer.errors:
            print("semantics errors found:")
            for error in self.sematic_analizer.errors:
                print(error)
            raise Exception("Semantic Check Fail")

    def generate_cil(self):
        if not self.latest_parser_output:
            raise Exception("No previous latest output found")
        self.cgen = CilGenerator(self.latest_parser_output)
        program = self.cgen.gen(self.latest_parser_output)
        return program

    def generate_mips(self, program):
        self.mgen = MipsGenerator()
        self.mgen.visit(program)
        file_name = self.output_file
        fd = open(file_name,"w")
        for string in self.mgen.to_data:
            print(string, file = fd)
        for string in self.mgen.to_text:
            print(string, file = fd)
        fd.close()

    def run(self, code):
        self.parse(code)
        self.run_semantics()
        program = self.generate_cil()
        self.generate_mips(program)

def run_test(testing_directory = st.default_testing_data_dir):
    st.create_directory(f"{testing_directory}\Output")
    for dir_code in st.get_testing_data(testing_directory):
        print(f"\ncompiling {dir_code.name}")
        fd = open(dir_code,"r")
        code = fd.read()
        fd.close()

        #run compiler
        try:
            compiler = CoolCompilerX(f"{testing_directory}\Output\{dir_code.name[0:-2]}mips")
            compiler.run(code)
            print(f"Compilation successful \nGenerated file: {testing_directory}Output/{dir_code.name[0:-2]}mips\n")
        except Exception as e:
            print(f"Compilation Failed. error: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-t":
            testing_directory = None
            if len(sys.argv) >= 3:
                testing_directory = sys.argv[2]

            run_test(testing_directory) if testing_directory else run_test()
            exit()

        else:
            code_dir = sys.argv[1]
            output_name = None
            if len(sys.argv) >= 3:
                output_name = sys.argv[2]

    else:
        print("usage: python CoolCompilerX <cool-code> [output-file-name]")
        print("usage: python CoolCompilerX -t [testing-directory]")
        exit()
    
    #extract code from file
    fd = open(code_dir,"r")
    code = fd.read()
    fd.close()

    #run compiler
    compiler = CoolCompilerX(output_name) if output_name else CoolCompilerX()
    compiler.run(code)