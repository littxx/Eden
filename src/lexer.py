import re

# Lexer
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('LET',      r'\blet\b'),
    ('IF',       r'\bif\b'),
    ('ELSE',     r'\belse\b'),
    ('WHILE',    r'\bwhile\b'),
    ('FOR',      r'\bfor\b'),
    ('FUNC',     r'\bfunction\b'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('OP',       r'[+\-*/]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('COMMA',    r','),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('EQ',       r'=='),
    ('NEQ',      r'!='),
    ('LE',       r'<='),
    ('GE',       r'>='),
    ('LT',       r'<'),
    ('GT',       r'>'),
    ('MISMATCH', r'.'),
]
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP' or kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value} inesperado')
        tokens.append((kind, value))
    return tokens
