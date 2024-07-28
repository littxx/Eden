from collections import namedtuple

# AST Node Definitions
Assign = namedtuple('Assign', ['name', 'value'])
BinOp = namedtuple('BinOp', ['left', 'op', 'right'])
Num = namedtuple('Num', ['value'])
Var = namedtuple('Var', ['name'])
If = namedtuple('If', ['condition', 'then_branch', 'else_branch'])
While = namedtuple('While', ['condition', 'body'])
For = namedtuple('For', ['initial', 'condition', 'increment', 'body'])
Func = namedtuple('Func', ['name', 'params', 'body'])
Call = namedtuple('Call', ['name', 'args'])

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self):
        self.pos += 1

    def current_token(self):
        return self.tokens[self.pos]

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
        return statements

    def statement(self):
        token = self.current_token()
        if token[0] == 'LET':
            return self.assignment()
        elif token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'WHILE':
            return self.while_statement()
        elif token[0] == 'FOR':
            return self.for_statement()
        elif token[0] == 'FUNC':
            return self.func_statement()
        else:
            return self.expr()

    def assignment(self):
        self.consume()  # Consume 'let'
        var = self.variable()
        self.consume()  # Consume '='
        expr = self.expr()
        self.consume()  # Consume ';'
        return Assign(var, expr)

    def if_statement(self):
        self.consume()  # Consume 'if'
        self.consume()  # Consume '('
        condition = self.expr()
        self.consume()  # Consume ')'
        self.consume()  # Consume '{'
        then_branch = []
        while self.current_token()[0] != 'RBRACE':
            then_branch.append(self.statement())
        self.consume()  # Consume '}'
        else_branch = []
        if self.current_token()[0] == 'ELSE':
            self.consume()  # Consume 'else'
            self.consume()  # Consume '{'
            while self.current_token()[0] != 'RBRACE':
                else_branch.append(self.statement())
            self.consume()  # Consume '}'
        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume()  # Consume 'while'
        self.consume()  # Consume '('
        condition = self.expr()
        self.consume()  # Consume ')'
        self.consume()  # Consume '{'
        body = []
        while self.current_token()[0] != 'RBRACE':
            body.append(self.statement())
        self.consume()  # Consume '}'
        return While(condition, body)

    def for_statement(self):
        self.consume()  # Consume 'for'
        self.consume()  # Consume '('
        initial = self.statement()
        condition = self.expr()
        self.consume()  # Consume ';'
        increment = self.statement()
        self.consume()  # Consume ')'
        self.consume()  # Consume '{'
        body = []
        while self.current_token()[0] != 'RBRACE':
            body.append(self.statement())
        self.consume()  # Consume '}'
        return For(initial, condition, increment, body)

    def func_statement(self):
        self.consume()  # Consume 'function'
        name = self.current_token()[1]
        self.consume()  # Consume function name
        self.consume()  # Consume '('
        params = []
        if self.current_token()[0] != 'RPAREN':
            params.append(self.current_token()[1])
            self.consume()  # Consume param
            while self.current_token()[0] == 'COMMA':
                self.consume()  # Consume ','
                params.append(self.current_token()[1])
                self.consume()  # Consume param
        self.consume()  # Consume ')'
        self.consume()  # Consume '{'
        body = []
        while self.current_token()[0] != 'RBRACE':
            body.append(self.statement())
        self.consume()  # Consume '}'
        return Func(name, params, body)

    def variable(self):
        token = self.current_token()
        if token[0] == 'ID':
            self.consume()
            return Var(token[1])
        raise SyntaxError('Esperado identificador')

    def expr(self):
        left = self.term()
        while self.current_token()[0] in ('OP', 'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT'):
            op = self.current_token()[1]
            self.consume()
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.consume()
            return Num(token[1])
        elif token[0] == 'ID':
            return self.variable()
        elif token[0] == 'LPAREN':
            self.consume()  # Consume '('
            expr = self.expr()
            self.consume()  # Consume ')'
            return expr
        raise SyntaxError('Esperado número ou identificador')
