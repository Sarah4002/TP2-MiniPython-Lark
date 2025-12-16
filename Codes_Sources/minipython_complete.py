# fichier: minipython_complete.py
from lark import Lark, Transformer
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os

# ------------------------------
# 1. Lecture interactive du code MiniPython
# ------------------------------
print("Entrez votre code MiniPython (finissez par une ligne vide) :")
lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    lines.append(line)
code_source = "\n".join(lines)

# ------------------------------
# 2. Chargement grammaire Lark
# ------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
grammar_path = os.path.join(script_dir, "minipython.lark")

with open(grammar_path, "r", encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(grammar, start="start", parser="lalr", lexer="basic")

# ------------------------------
# 3. Analyse lexicale
# ------------------------------
print("\n=== Phase lexicale (Lark) ===")
tokens = list(parser.lex(code_source))
for t in tokens:
    print(t)

# ------------------------------
# 4. AST syntaxique via Transformer
# ------------------------------
class SyntaxTransformer(Transformer):
    def start(self, items): return list(items)
    def decl(self, items): return ("decl(L)", items[0], 'int')
    def var_list(self, items): return [str(i) for i in items]
    def assign(self, items): return ("assign(S)", str(items[0]), items[1])
    def add(self, items): return ('+(S)', str(items[0]), items[1])
    def print_stmt(self, items): return ("print(S)", str(items[0]))
    def while_stmt(self, items): return ("while", items[0], items[1])
    def if_stmt(self, items): return ("if", items[0], items[1])
    def condition(self, items): return (items[0], str(items[1]), items[2])
    def NUMBER(self, n): return int(n)
    def CNAME(self, n): return str(n)

tree = parser.parse(code_source)
ast_syntax = SyntaxTransformer().transform(tree)

print("\n=== AST syntaxique ===")
for node in ast_syntax:
    print(node)

# ------------------------------
# 5. Analyse sémantique
# ------------------------------
class SemanticChecker:
    def __init__(self): self.symbol_table = {}

    def check(self, ast_list):
        new_ast = []
        for stmt in ast_list:
            if stmt[0] == 'decl(L)':
                for var in stmt[1]:
                    if var in self.symbol_table:
                        raise Exception(f"Variable {var} déjà déclarée")
                    self.symbol_table[var] = 'int'
                new_ast.append(stmt)
            elif stmt[0] == 'assign(S)':
                var, expr = stmt[1], stmt[2]
                if var not in self.symbol_table:
                    raise Exception(f"Variable {var} non déclarée")
                if isinstance(expr, tuple) and expr[0] == '+(S)':
                    if expr[1] not in self.symbol_table:
                        raise Exception(f"Variable {expr[1]} non déclarée")
                new_ast.append(stmt)
            elif stmt[0] == 'print(S)':
                var = stmt[1]
                if var not in self.symbol_table:
                    raise Exception(f"Variable {var} non déclarée")
                new_ast.append(stmt)
            elif stmt[0] in ['while', 'if']:
                cond, block = stmt[1], stmt[2]
                for s in block:
                    if s[0] == 'assign(S)' and s[1] not in self.symbol_table:
                        raise Exception(f"Variable {s[1]} non déclarée")
                new_ast.append(stmt)
        return new_ast

semantic = SemanticChecker()
ast_semantic = semantic.check(ast_syntax)

print("\n=== AST après analyse sémantique ===")
for node in ast_semantic:
    print(node)

print("\n=== Table des symboles ===")
for var, typ in semantic.symbol_table.items():
    print(f"{var}: {typ}")

# ------------------------------
# 6. Visualisation AST
# ------------------------------
def build_anytree(node, parent=None):
    if isinstance(node, tuple):
        n = Node(node[0], parent=parent)
        for c in node[1:]:
            build_anytree(c, n)
        return n
    elif isinstance(node, list):
        for item in node:
            build_anytree(item, parent)
        return parent
    else:
        Node(str(node), parent=parent)
        return parent

root = build_anytree(("root", *ast_semantic))
print("\n=== AST visuel console ===")
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")

# Export DOT/PNG
try:
    output_path = os.path.join(script_dir, "ast_lark.png")
    dot_path = os.path.join(script_dir, "ast_lark.dot")
    DotExporter(root).to_dotfile(dot_path)
    import subprocess
    result = subprocess.run(['dot', '-Tpng', dot_path, '-o', output_path],
                            capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n=== Image PNG sauvegardée : {output_path} ===")
    else:
        print(f"\nErreur Graphviz : {result.stderr}")
except Exception as e:
    print(f"\nErreur export AST : {e}")

# ------------------------------
# 7. Exécution MiniPython
# ------------------------------
def eval_condition(cond, runtime):
    op, left, right = cond
    left_val = runtime[left] if left in runtime else int(left)
    right_val = runtime[right] if right in runtime else int(right)
    if op == '<': return left_val < right_val
    if op == '==': return left_val == right_val
    if op == '>': return left_val > right_val
    return False

def execute_stmt(stmt, runtime):
    if stmt[0] == 'assign(S)':
        var, val = stmt[1], stmt[2]
        if isinstance(val, tuple) and val[0] == '+(S)':
            left_val = runtime[val[1]] if val[1] in runtime else int(val[1])
            right_val = val[2]
            runtime[var] = left_val + right_val
        elif isinstance(val, int):
            runtime[var] = val
        else:
            runtime[var] = runtime[val]
    elif stmt[0] == 'print(S)':
        print(runtime[stmt[1]])
    elif stmt[0] == 'while':
        cond, block = stmt[1], stmt[2]
        while eval_condition(cond, runtime):
            for s in block:
                execute_stmt(s, runtime)
    elif stmt[0] == 'if':
        cond, block = stmt[1], stmt[2]
        if eval_condition(cond, runtime):
            for s in block:
                execute_stmt(s, runtime)

def execute(ast, symbol_table):
    runtime = {var: None for var in symbol_table.keys()}
    for stmt in ast:
        execute_stmt(stmt, runtime)

print("\n=== Exécution MiniPython ===")
execute(ast_semantic, semantic.symbol_table)

# ------------------------------
# 8. Génération TAC simple
# ------------------------------
def generate_TAC(ast):
    tac = []
    for stmt in ast:
        if stmt[0] == 'decl(L)':
            for var in stmt[1]:
                tac.append(f"DECLARE {var}")
        elif stmt[0] == 'assign(S)':
            val = stmt[2]
            if isinstance(val, tuple) and val[0] == '+(S)':
                tac.append(f"LOAD {val[1]}")
                tac.append(f"ADD {val[2]}")
                tac.append(f"STORE {stmt[1]}")
            else:
                tac.append(f"LOAD {val}")
                tac.append(f"STORE {stmt[1]}")
        elif stmt[0] == 'print(S)':
            tac.append(f"PRINT {stmt[1]}")
    return tac

tac_code = generate_TAC(ast_semantic)
print("\n=== Code intermédiaire (TAC) ===")
for line in tac_code:
    print(line)

