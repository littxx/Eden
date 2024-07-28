class IRNode:
    pass

class IRAssign(IRNode):
    def __init__(self, var, value):
        self.var = var
        self.value = value

class IRBinOp(IRNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IRVar(IRNode):
    def __init__(self, name):
        self.name = name

class IRNum(IRNode):
    def __init__(self, value):
        self.value = value

class IRIf(IRNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class IRWhile(IRNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IRFor(IRNode):
    def __init__(self, initial, condition, increment, body):
        self.initial = initial
        self.condition = condition
        self.increment = increment
        self.body = body

class IRFunc(IRNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class IRCall(IRNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

def generate_ir(ast):
    if isinstance(ast, list):
        return [generate_ir(node) for node in ast]
    elif isinstance(ast, Assign):
        return IRAssign(ast.name.name, generate_ir(ast.value))
    elif isinstance(ast, BinOp):
        return IRBinOp(ast.op, generate_ir(ast.left), generate_ir(ast.right))
    elif isinstance(ast, Num):
        return IRNum(ast.value)
    elif isinstance(ast, Var):
        return IRVar(ast.name)
    elif isinstance(ast, If):
        return IRIf(generate_ir(ast.condition), generate_ir(ast.then_branch), generate_ir(ast.else_branch))
    elif isinstance(ast, While):
        return IRWhile(generate_ir(ast.condition), generate_ir(ast.body))
    elif isinstance(ast, For):
        return IRFor(generate_ir(ast.initial), generate_ir(ast.condition), generate_ir(ast.increment), generate_ir(ast.body))
    elif isinstance(ast, Func):
        return IRFunc(ast.name, ast.params, generate_ir(ast.body))
    elif isinstance(ast, Call):
        return IRCall(ast.name, generate_ir(ast.args))
    else:
        raise TypeError(f"Desconhecido AST node {ast}")
