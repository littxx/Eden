def generate_assembly(ir):
    assembly = []
    if isinstance(ir, list):
        for node in ir:
            assembly.extend(generate_assembly(node).split('\n'))
    elif isinstance(ir, IRAssign):
        assembly.append(f"mov dword [{ir.var}], {generate_assembly(ir.value)}")
    elif isinstance(ir, IRBinOp):
        left = generate_assembly(ir.left)
        right = generate_assembly(ir.right)
        if ir.op == '+':
            assembly.append(f"mov eax, {left}")
            assembly.append(f"add eax, {right}")
        elif ir.op == '-':
            assembly.append(f"mov eax, {left}")
            assembly.append(f"sub eax, {right}")
        elif ir.op == '*':
            assembly.append(f"mov eax, {left}")
            assembly.append(f"imul eax, {right}")
        elif ir.op == '/':
            assembly.append(f"mov eax, {left}")
            assembly.append(f"mov ebx, {right}")
            assembly.append(f"cdq")
            assembly.append(f"idiv ebx")
        elif ir.op in ('==', '!=', '<', '<=', '>', '>='):
            assembly.append(f"mov eax, {left}")
            assembly.append(f"cmp eax, {right}")
            if ir.op == '==':
                assembly.append(f"sete al")
            elif ir.op == '!=':
                assembly.append(f"setne al")
            elif ir.op == '<':
                assembly.append(f"setl al")
            elif ir.op == '<=':
                assembly.append(f"setle al")
            elif ir.op == '>':
                assembly.append(f"setg al")
            elif ir.op == '>=':
                assembly.append(f"setge al")
            assembly.append(f"movzx eax, al")
        assembly.append(f"mov [{left}], eax")
    elif isinstance(ir, IRNum):
        return str(ir.value)
    elif isinstance(ir, IRVar):
        return f"dword [{ir.name}]"
    elif isinstance(ir, IRIf):
        condition = generate_assembly(ir.condition)
        then_branch = generate_assembly(ir.then_branch)
        else_branch = generate_assembly(ir.else_branch)
        assembly.append(f"cmp {condition}, 0")
        assembly.append(f"je else_branch")
        assembly.extend(then_branch.split('\n'))
        assembly.append(f"jmp end_if")
        assembly.append(f"else_branch:")
        assembly.extend(else_branch.split('\n'))
        assembly.append(f"end_if:")
    elif isinstance(ir, IRWhile):
        condition = generate_assembly(ir.condition)
        body = generate_assembly(ir.body)
        assembly.append(f"start_while:")
        assembly.append(f"cmp {condition}, 0")
        assembly.append(f"je end_while")
        assembly.extend(body.split('\n'))
        assembly.append(f"jmp start_while")
        assembly.append(f"end_while:")
    elif isinstance(ir, IRFor):
        initial = generate_assembly(ir.initial)
        condition = generate_assembly(ir.condition)
        increment = generate_assembly(ir.increment)
        body = generate_assembly(ir.body)
        assembly.extend(initial.split('\n'))
        assembly.append(f"start_for:")
        assembly.append(f"cmp {condition}, 0")
        assembly.append(f"je end_for")
        assembly.extend(body.split('\n'))
        assembly.extend(increment.split('\n'))
        assembly.append(f"jmp start_for")
        assembly.append(f"end_for:")
    elif isinstance(ir, IRFunc):
        assembly.append(f"{ir.name}:")
        for param in ir.params:
            assembly.append(f"push {param}")
        body = generate_assembly(ir.body)
        assembly.extend(body.split('\n'))
        assembly.append(f"ret")
    elif isinstance(ir, IRCall):
        for arg in reversed(ir.args):
            assembly.append(f"push {generate_assembly(arg)}")
        assembly.append(f"call {ir.name}")
    else:
        raise TypeError(f"Desconhecido IR node {ir}")
    return '\n'.join(assembly)
