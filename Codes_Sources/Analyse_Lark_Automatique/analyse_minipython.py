from lark import Lark, Transformer, Tree
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os
 
# Obtenir le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
grammar_path = os.path.join(script_dir, "minipython.lark")
 
# Charger la grammaire .lark depuis le fichier
with open(grammar_path, "r", encoding="utf-8") as f:
    grammar = f.read()
 
parser = Lark(grammar, start="start", parser="lalr", lexer="basic")
 
code_source = """
int x, y;
x = 5;
y = x + 2;
print(y);
"""
 
# ------------------------------
# 2. Analyse lexicale
# ------------------------------
print("\n=== Phase lexicale (Lark) ===")
tokens = list(parser.lex(code_source))
for t in tokens:
    print(t)
 
# ------------------------------
# 3. AST syntaxique avec Lark Transformer
# ------------------------------
class SyntaxTransformer(Transformer):
    def start(self, items):
        return list(items)
   
    def decl(self, items):
        # items[0] est var_list
        return ("decl(L)", items[0], 'int')
   
    def var_list(self, items):
        # Retourner la liste des noms de variables
        return [str(item) for item in items]
   
    def assign(self, items):
        # items[0] = CNAME, items[1] = expr
        return ("assign(S)", str(items[0]), items[1])
   
    def add(self, items):
        # items[0] = CNAME, items[1] = NUMBER
        return ('+(S)', str(items[0]), int(items[1]))
   
    def print_stmt(self, items):
        return ("print(S)", str(items[0]))
   
    def NUMBER(self, n):
        return int(n)
   
    def CNAME(self, n):
        return str(n)
 
tree = parser.parse(code_source)
print("\n=== Arbre de parsing brut ===")
print(tree.pretty())
 
ast_syntax = SyntaxTransformer().transform(tree)
 
print("\n=== AST syntaxique (Lark) ===")
for node in ast_syntax:
    print(node)
 
# ------------------------------
# 4. Analyse sémantique
# ------------------------------
class SemanticTransformer:
    def __init__(self):
        self.symbol_table = {}
 
    def check(self, ast_list):
        new_ast = []
        for stmt in ast_list:
            if stmt[0] == "decl(L)":
                var_list = stmt[1]
                for var in var_list:
                    if var in self.symbol_table:
                        raise Exception(f"Erreur : variable {var} déjà déclarée")
                    self.symbol_table[var] = 'int'
                new_ast.append(stmt)
 
            elif stmt[0] == "assign(S)":
                var, expr = stmt[1], stmt[2]
                if var not in self.symbol_table:
                    raise Exception(f"Erreur : variable {var} non déclarée")
               
                # Vérifier l'expression
                if isinstance(expr, tuple) and expr[0] == '+(S)':
                    left = expr[1]
                    if left not in self.symbol_table:
                        raise Exception(f"Erreur : variable {left} non déclarée dans l'expression")
                elif isinstance(expr, str) and expr not in self.symbol_table:
                    # C'est une variable
                    try:
                        int(expr)  # Si c'est un nombre, pas de problème
                    except ValueError:
                        raise Exception(f"Erreur : variable {expr} non déclarée")
               
                new_ast.append(stmt)
 
            elif stmt[0] == "print(S)":
                var = stmt[1]
                if var not in self.symbol_table:
                    raise Exception(f"Erreur : variable {var} non déclarée")
                new_ast.append(stmt)
 
        return new_ast
 
semantic = SemanticTransformer()
ast_semantic = semantic.check(ast_syntax)
 
print("\n=== AST après analyse sémantique ===")
for node in ast_semantic:
    print(node)
 
print("\n=== Table des symboles ===")
for var, typ in semantic.symbol_table.items():
    print(f"{var}: {typ}")
 
# ------------------------------
# 5. Visualisation AST
# ------------------------------
def build_anytree(node, parent=None):
    if isinstance(node, tuple):
        n = Node(node[0], parent=parent)
        for c in node[1:]:
            build_anytree(c, n)
        return n
    elif isinstance(node, list):
        n = Node("list", parent=parent)
        for item in node:
            build_anytree(item, n)
        return n
    else:
        Node(str(node), parent=parent)
        return parent
 
root = build_anytree(("root", *ast_semantic))
 
print("\n=== AST visuel console ===")
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")
 
# Sauvegarder l'image dans le même répertoire que le script
output_path = os.path.join(script_dir, "ast_lark.png")
dot_path = os.path.join(script_dir, "ast_lark.dot")
 
try:
    # Créer d'abord le fichier .dot
    DotExporter(root).to_dotfile(dot_path)
    print(f"\n=== Fichier DOT sauvegardé : {dot_path} ===")
   
    # Puis générer l'image PNG
    import subprocess
    result = subprocess.run(['dot', '-Tpng', dot_path, '-o', output_path],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"=== Image PNG sauvegardée : {output_path} ===")
    else:
        print(f"=== Erreur Graphviz : {result.stderr} ===")
        print("Vous pouvez visualiser le fichier .dot manuellement")
except FileNotFoundError:
    print("\n=== Graphviz n'est pas installé ===")
    print("Installez-le depuis : https://graphviz.org/download/")
    print(f"Le fichier DOT a été créé : {dot_path}")
except Exception as e:
    print(f"\n=== Erreur lors de la sauvegarde : {e} ===")
    print("Le fichier .dot devrait être accessible")
 
# ------------------------------
# 6. Exécution MiniPython
# ------------------------------
def execute(ast, symbol_table):
    runtime = {var: None for var in symbol_table.keys()}
 
    for stmt in ast:
        if stmt[0] == 'assign(S)':
            var = stmt[1]
            val = stmt[2]
 
            if isinstance(val, tuple) and val[0] == '+(S)':
                # Addition: variable + nombre
                left = runtime[val[1]] if val[1] in runtime else int(val[1])
                right = val[2]
                runtime[var] = left + right
            elif isinstance(val, int):
                # Nombre direct
                runtime[var] = val
            else:
                # Variable
                runtime[var] = runtime[val]
 
        elif stmt[0] == 'print(S)':
            var = stmt[1]
            print(runtime[var])
 
print("\n=== Exécution MiniPython ===")
execute(ast_semantic, semantic.symbol_table)
 