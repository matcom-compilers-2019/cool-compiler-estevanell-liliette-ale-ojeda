import os
cwd = os.getcwd()

# DIRECTORIES
## lexer
default_lexer_testing_data_dir = 'Utils/Testing/'
default_testing_data_dir = 'Utils/Testing/'
default_lexer_directory = "Sintax/"
default_parser_directory = "Sintax/"
default_output_mips_dir = "Output/"

def get_output_mips_name(code_name, path = ""):
    if not path:
        op = default_output_mips_dir
    else:
        op = path
    return "%s/%s/%s" %(cwd,op,str(code_name))

def get_lexer_testing_data(path = default_testing_data_dir):
    """
    Scan a directory (no recursive scan) looking for cool programs source code for lexer testing \n
    :param path: specifies the direcori to be scan, if not specified just scan default directory \n
    :return: DirEntry objects list, this objects can be opened for data adquisition
    """
    try:
        dir_obj = os.scandir(path)
        testing_data = []
        for obj in dir_obj:
            if obj.is_file() and obj.name.endswith(".cl"):
                testing_data.append(obj)
        return testing_data
    except Exception as e:
        raise e

def get_testing_data(path = default_lexer_testing_data_dir):
    """
    Scan a directory (recursive scan) looking for cool programs source code for lexer testing. \n
    `param path` specifies the directory to be scan, if not specified just scan default directory \n
    `return` DirEntry objects list, this objects can be opened for data adquisition
    """
    try:
        dir_obj = os.scandir(path)
        testing_data = []
        for obj in dir_obj:
            if obj.is_file() and obj.name.endswith(".cl"):
                testing_data.append(obj)
            elif not obj.is_file():
                r_testing_data = get_testing_data(f"{path}\{obj.name}")
                testing_data += r_testing_data
        return testing_data
    except Exception as e:
        raise e

def create_directory(path):
    try: #lexer directory
        os.makedirs(f"{path}")
    except:
        pass

##template for scaffolding if required
def default_scaffolding():
    try: #lexer directory
        os.makedirs("%s/%s" %(cwd,default_lexer_directory))
    except:
        pass
    try: #parser directory
        os.makedirs("%s/%s" %(cwd,default_parser_directory))
    except:
        pass
    try: #output directory
        os.makedirs("%s/%s" %(cwd,default_output_mips_dir))
    except:
        pass

