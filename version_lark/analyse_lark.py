from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re
import os
import shutil
import subprocess
import tempfile

# ------------------------------
# 1. Code source MiniPython
# ------------------------------
code_source = """
int x;
x=0;
while (x <3){
    if (x ==1) {
        print(x);
    }
    x = x + 1;
}
"""

# ------------------------------
# 2. Analyse lexicale
# ------------------------------
token_specification = [
    ('INT', r'int'), ('FLOAT', r'float'), ('BOOL', r'bool'),
    ('STRING', r'string'), ('PRINT', r'print'), ('WHILE', r'while'),
    ('IF', r'if'), ('ELSE', r'else'), ('FOR', r'for'),
    ('TRUE', r'true'), ('FALSE', r'false'),

    ('EQEQ', r'=='), ('NEQ', r'!='), ('LTE', r'<='), ('GTE', r'>='),
    ('LT', r'<'), ('GT', r'>'),
    ('AND', r'&&'), ('OR', r'\|\|'), ('NOT', r'!'),

    ('PLUS', r'\+'), ('MINUS', r'-'),
    ('STAR', r'\*'), ('SLASH', r'/'),
    ('EQUAL', r'='),

    ('LPAR', r'\('), ('RPAR', r'\)'),
    ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),

    ('FLOATNUM', r'\d+\.\d+'),
    ('NUMBER', r'\d+'),
    ('STRINGLIT', r'"[^"]*"'),
    ('ID', r'[A-Za-z_]\w*'),

    ('SKIP', r'[ \t\n]+')
]

regex = '|'.join(f'(?P<{n}>{p})' for n, p in token_specification)
tokens = [(m.lastgroup, m.group()) for m in re.finditer(regex, code_source) if m.lastgroup != 'SKIP']

print("\n=== Phase lexicale ===")
for t in tokens:
    print(t)

# ------------------------------
# 3. Analyse syntaxique & AST
# ------------------------------

symbol_table = {}

###########
# EXPRESSIONS
###########

def parse_expr(tokens, start_idx): return parse_or(tokens, start_idx)

def parse_or(tokens, i):
    left, i = parse_and(tokens, i)
    while i < len(tokens) and tokens[i][0] == 'OR':
        i += 1
        right, i = parse_and(tokens, i)
        left = ('Expr: ||', [left, right])
    return left, i

def parse_and(tokens, i):
    left, i = parse_equality(tokens, i)
    while i < len(tokens) and tokens[i][0] == 'AND':
        i += 1
        right, i = parse_equality(tokens, i)
        left = ('Expr: &&', [left, right])
    return left, i

def parse_equality(tokens, i):
    left, i = parse_comparison(tokens, i)
    while i < len(tokens) and tokens[i][0] in ('EQEQ', 'NEQ'):
        op = '==' if tokens[i][0] == 'EQEQ' else '!='
        i += 1
        right, i = parse_comparison(tokens, i)
        left = (f'Expr: {op}', [left, right])
    return left, i

def parse_comparison(tokens, i):
    left, i = parse_additive(tokens, i)
    while i < len(tokens) and tokens[i][0] in ('LT','GT','LTE','GTE'):
        op_map = {'LT':'<','GT':'>','LTE':'<=','GTE':'>='}
        op = op_map[tokens[i][0]]
        i += 1
        right, i = parse_additive(tokens, i)
        left = (f'Expr: {op}', [left, right])
    return left, i

def parse_additive(tokens, i):
    left, i = parse_multiplicative(tokens, i)
    while i < len(tokens) and tokens[i][0] in ('PLUS', 'MINUS'):
        op = '+' if tokens[i][0]=='PLUS' else '-'
        i += 1
        right, i = parse_multiplicative(tokens, i)
        left = (f'Expr: {op}', [left, right])
    return left, i

def parse_multiplicative(tokens, i):
    left, i = parse_unary(tokens, i)
    while i < len(tokens) and tokens[i][0] in ('STAR','SLASH'):
        op = '*' if tokens[i][0]=='STAR' else '/'
        i += 1
        right, i = parse_unary(tokens, i)
        left = (f'Expr: {op}', [left, right])
    return left, i

def parse_unary(tokens, i):
    if tokens[i][0] in ('MINUS','NOT'):
        op = '-' if tokens[i][0]=='MINUS' else '!'
        i += 1
        expr, i = parse_unary(tokens, i)
        return (f'Expr: unary{op}', [expr]), i
    return parse_primary(tokens, i)

def parse_primary(tokens, i):
    tok,val = tokens[i]
    if tok == 'LPAR':
        expr, j = parse_expr(tokens, i+1)
        return expr, j+1
    if tok == 'NUMBER': return ('Const: '+val), i+1
    if tok == 'ID': return ('Var: '+val), i+1
    return None, i

###########
# STATEMENTS
###########
def parse_statement(tokens, i):
    if tokens[i][0]=='INT':
        i+=1
        varname=tokens[i][1]
        symbol_table[varname]='int'
        i+=1  # name
        i+=1  # ;
        return ('Decl', [f'Var: {varname} (type=int)']), i
    
    if tokens[i][0]=='ID':
        var=tokens[i][1]
        i+=2 # var '='
        expr,i=parse_expr(tokens,i)
        i+=1 # ;
        return ('Assign',[f'Var: {var}',expr]),i

    if tokens[i][0]=='PRINT':
        i+=2 # print (
        expr,i=parse_expr(tokens,i)
        i+=2 # ) ;
        return ('Print',[expr]),i

    if tokens[i][0]=='WHILE':
        i+=2
        cond,i=parse_expr(tokens,i)
        i+=1
        body,i=parse_block(tokens,i)
        return ('While',[cond,('Block',body)]),i

    if tokens[i][0]=='IF':
        i+=2
        cond,i=parse_expr(tokens,i)
        i+=1
        then_body,i=parse_block(tokens,i)
        else_body=[]
        return ('If',[cond,('Block',then_body),('Block',else_body)]),i

    return None,i

def parse_block(tokens,i):
    i+=1
    body=[]
    while tokens[i][0] != 'RBRACE':
        stmt,i=parse_statement(tokens,i)
        body.append(stmt)
    return body,i+1

# Parse global
ast=[]
i=0
while i<len(tokens):
    stmt,i=parse_statement(tokens,i)
    ast.append(stmt)

print("\n=== AST syntaxique brut ===")
for x in ast: print(x)

# ------------------------------
# 4. Analyse sémantique
# ------------------------------
ast_semantic = ast

print("\n=== AST après analyse sémantique ===")
for x in ast_semantic: print(x)

# ------------------------------
# 5. Génération TAC
# ------------------------------
class TACGenerator:
    def __init__(self):
        self.code=[]
        self.temp_id=0
        self.label_id=0
    
    def new_temp(self):
        self.temp_id+=1
        return f"t{self.temp_id}"
    
    def new_label(self):
        self.label_id+=1
        return f"L{self.label_id}"
    
    def emit(self, line):
        self.code.append(line)

    def gen_expr(self, expr):
        if isinstance(expr,str):
            if expr.startswith("Const:"):
                return expr.split(": ")[1]
            if expr.startswith("Var:"):
                v=expr.split(": ")[1]
                t=self.new_temp()
                self.emit(f"LOAD {t}, {v}")
                return t

        if isinstance(expr,tuple):
            op=expr[0].split(": ")[1]
            left=self.gen_expr(expr[1][0])
            right=self.gen_expr(expr[1][1])
            t=self.new_temp()
            opmap={'+':'ADD','-':'SUB','*':'MUL','/':'DIV','<':'LT','>':'GT','<=':'LTE','>=':'GTE','==':'EQ','!=':'NEQ'}
            op=opmap[op]
            self.emit(f"{op} {t}, {left}, {right}")
            return t
        
        return "0"

    def gen_stmt(self, stmt):
        if stmt[0]=='Decl':
            v=stmt[1][0].split()[1]
            self.emit(f"DECLARE int {v}")
        
        elif stmt[0]=='Assign':
            v=stmt[1][0].split(": ")[1]
            r=self.gen_expr(stmt[1][1])
            self.emit(f"STORE {v}, {r}")
        
        elif stmt[0]=='Print':
            r=self.gen_expr(stmt[1][0])
            self.emit(f"PRINT {r}")
        
        elif stmt[0]=='While':
            L1=self.new_label()
            L2=self.new_label()
            cond=stmt[1][0]
            self.emit(f"LABEL {L1}")
            rc=self.gen_expr(cond)
            self.emit(f"JZ {rc}, {L2}")
            for s in stmt[1][1][1]:
                self.gen_stmt(s)
            self.emit(f"JMP {L1}")
            self.emit(f"LABEL {L2}")

    def generate(self, ast):
        for s in ast:
            self.gen_stmt(s)
        return self.code

tac=TACGenerator().generate(ast_semantic)

print("\n=== CODE INTERMÉDIAIRE (TAC) ===")
for x in tac: print(x)

# ------------------------------
# 6. Visualisation AST
# ------------------------------

def build_anytree(node, parent=None):
    n=Node(node[0], parent=parent)
    for c in node[1]:
        if isinstance(c,tuple):
            build_anytree(c,n)
        elif isinstance(c,list):
            cn=Node("Block", parent=n)
            for x in c:
                build_anytree(x,cn)
        else:
            Node(str(c), parent=n)
    return n

root = build_anytree(("Program", ast_semantic))

print("\n=== AST visuel console ===")
for pre,_,n in RenderTree(root):
    print(pre+n.name)

# Fix: generate DOT into local folder (NO TEMP FILES)
dot_path = os.path.join(os.getcwd(),"ast.dot")
png_path = os.path.join(os.getcwd(),"ast.png")

try:
    DotExporter(root).to_dotfile(dot_path)
    subprocess.run(["dot","-Tpng",dot_path,"-o",png_path], check=True)
    print(f"\n✔ Image PNG générée : {png_path}")
except Exception as e:
    print("\nGraphviz non disponible :", e)

# ------------------------------
# 7. Exécution MiniPython
# ------------------------------

def eval_expr(expr, env):
    if isinstance(expr,str):
        if expr.startswith("Const:"):
            return int(expr.split(": ")[1])
        if expr.startswith("Var:"):
            return env[expr.split(": ")[1]]

    if isinstance(expr,tuple):
        op=expr[0].split(": ")[1]
        left=eval_expr(expr[1][0],env)
        right=eval_expr(expr[1][1],env)
        ops={'+':left+right,'-':left-right,'*':left*right,'/':left/right,
             '<':left<right,'>':left>right,'<=':left<=right,'>=':left>=right,
             '==':left==right,'!=':left!=right}
        return ops[op]

def exec_stmt(stmt,env):
    if stmt[0]=='Assign':
        v=stmt[1][0].split(": ")[1]
        env[v]=eval_expr(stmt[1][1],env)
        print(f"EXEC: {v}={env[v]}")
    elif stmt[0]=='Print':
        print("PRINT:", eval_expr(stmt[1][0],env))
    elif stmt[0]=='While':
        cond=stmt[1][0]
        while eval_expr(cond,env):
            for s in stmt[1][1][1]:
                exec_stmt(s,env)

def execute(ast,symtab):
    env={k:0 for k in symtab}
    print("\n=== Début exécution ===")
    for s in ast:
        exec_stmt(s,env)

print("\n=== Exécution MiniPython ===")
execute(ast_semantic,symbol_table)
print("=== Fin exécution ===")
