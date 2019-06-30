import Sintax.lexer as lex
import Sintax.parsing as psr
import Utils.settings as st
import Semantics.semantics as sem
from GeneratingCIL.CILgenerator import CilGenerator
from GeneratingMIPS.MIPSgenerator import MipsGenerator

class CoolCompilerX:
    def __init__(self):
        self.lexer = lex.Lexer()
        self.lexer.build()
        self.parser = psr.CoolParsX()
        self.parser.build(lexer = self.lexer)
        self.latest_parser_output = None
        self.cgen = None
        self.mgen = None
        self.sematic_analizer = None

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
        file_name = st.get_output_mips_name("test.asm")
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
        print("Ya")

testing_code = """
class Main{
    x:Int <- sum(1,11);
    sum(p1:Int,p2:Int):Int{p1 + p2 + 1};
    main(): Int{
        {
        x;
        }
    };
};

"""

# fd = open("test.cl")
# testing_code = fd.read()
# fd.close()

a = CoolCompilerX()
# a.test_lexer()
a.run(testing_code)