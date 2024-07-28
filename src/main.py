import subprocess
from lexer import tokenize
from parser import Parser
from ir import generate_ir
from codegen import generate_assembly

def compile_eden(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    ir = generate_ir(ast)
    assembly = generate_assembly(ir)
    return assembly

def main():
    # Leitura do arquivo Eden e compilação
    with open('../examples/index.eden', 'r') as file:
        eden_code = file.read()

    assembly_code = compile_eden(eden_code)

    with open('program.asm', 'w') as file:
        file.write(assembly_code)

    print("Código de montagem gerado com sucesso.")

    # Montagem com NASM
    result = subprocess.run(['nasm', '-f', 'elf64', 'program.asm', '-o', 'program.o'])
    if result.returncode != 0:
        print("Erro na montagem do código.")
        return

    # Linkagem com ld
    result = subprocess.run(['ld', 'program.o', '-o', 'program'])
    if result.returncode != 0:
        print("Erro na linkagem do código.")
        return

    print("Programa compilado e executável gerado com sucesso.")

if __name__ == '__main__':
    main()
