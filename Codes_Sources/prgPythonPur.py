from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re
import os
 
# ------------------------------
# 1. Code source MiniPython
# ------------------------------
code_source = """
int x, y;
x = 5;
y = x + 2;
print(y);
"""
 
# ------------------------------
# 2. Analyse lexicale
# ------------------------------
token_specification = [
    ('NUMBER', r'\d+'), ('INT', r'int'), ('PRINT', r'print'),
    ('ID', r'[A-Za-z_]\w*'), ('COMMA', r','), ('SEMICOLON', r';'),
    ('PLUS', r'\+'), ('EQUAL', r'='), ('LPAR', r'\('), ('RPAR', r'\)'),
    ('SKIP', r'[ \t\n]+')
]
regex = '|'.join(f'(?P<{n}>{p})' for n, p in token_specification)
tokens = [(m.lastgroup, m.group()) for m in re.finditer(regex, code_source) if m.lastgroup != 'SKIP']
 
print("\n=== Phase lexicale ===")
for t in tokens:
    print(t)
 
# ------------------------------
# 3. Analyse syntaxique & construction AST
# ------------------------------
symbol_table = {}
ast = []
 
i = 0
while i < len(tokens):
    tok, val = tokens[i]
    if tok == 'INT':  # Déclaration de variables
        i += 1
        vars_list = []
        while i < len(tokens) and tokens[i][0] != 'SEMICOLON':
            if tokens[i][0] == 'ID':
                vars_list.append(tokens[i][1])
            i += 1
        for v in vars_list:
            symbol_table[v] = 'int'
        ast.append(('Decl', [('Var: ' + v + ' (type=int)') for v in vars_list]))
        i += 1
    elif tok == 'ID':  # Assignation
        var_name = val
        i += 2  # skip '='
        if i >= len(tokens):
            break
        left_tok, left_val = tokens[i]
        i += 1
        if i < len(tokens) and tokens[i][0] == 'PLUS':
            i += 1
            if i >= len(tokens):
                break
            right_val = int(tokens[i][1])
            i += 1
            expr = ('Expr: +', [('Var: ' + left_val), ('Const: ' + str(right_val))])
        else:
            expr = ('Expr', [('Const: ' + left_val) if left_val.isdigit() else ('Var: ' + left_val)])
        ast.append(('Assign', [('Var: ' + var_name), expr]))
        i += 1  # skip ';'
    elif tok == 'PRINT':
        i += 2  # skip '('
        if i >= len(tokens):
            break
        var_name = tokens[i][1]
        i += 2  # skip ')' and ';'
        ast.append(('Print', [('Var: ' + var_name)]))
    else:
        i += 1
 
print("\n=== AST syntaxique brut ===")
for node in ast:
    print(node)
 
# ------------------------------
# 4. Analyse sémantique simple
# ------------------------------
def semantic_check(ast, symbol_table):
    new_ast = []
    for stmt in ast:
        if stmt[0].startswith('Decl'):
            new_ast.append(stmt)
        elif stmt[0].startswith('Assign'):
            var = stmt[1][0].split(': ')[1]
            if var not in symbol_table:
                raise Exception(f"Erreur sémantique : variable {var} non déclarée")
            new_ast.append(stmt)
        elif stmt[0].startswith('Print'):
            var = stmt[1][0].split(': ')[1]
            if var not in symbol_table:
                raise Exception(f"Erreur sémantique : variable {var} non déclarée")
            new_ast.append(stmt)
    return new_ast
 
ast_semantic = semantic_check(ast, symbol_table)
print("\n=== AST après analyse sémantique ===")
for node in ast_semantic:
    print(node)
 
# ------------------------------
# 5. Visualisation AST avec anytree
# ------------------------------
def build_anytree(node, parent=None):
    if isinstance(node, tuple):
        n = Node(node[0], parent=parent)
        for c in node[1]:
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
 
root_node = build_anytree(("Program", ast_semantic))
print("\n=== AST visuel console ===")
for pre, fill, node in RenderTree(root_node):
    print(f"{pre}{node.name}")
 
# Export Graphviz (optionnel - peut être ignoré si problème d'installation)
try:
    # Exporter un fichier DOT local (sans passer par Temp)
    DotExporter(root_node).to_dotfile("ast.dot")
    print("\nFichier DOT généré : ast.dot")

    # Convertir DOT -> PNG sans fichier temporaire caché
    import os
    ret = os.system("dot -Tpng ast.dot -o ast_graphviz.png")

    if ret == 0:
        print("\nAST exporté en image : ast_graphviz.png")
    else:
        print("\nGraphviz installé mais l'exécution de 'dot' a échoué.")
        print("Vérifie que Graphviz est dans le PATH. (where dot)")

except Exception as e:
    print(f"\nErreur Graphviz : {e}")
    print("Pour installer: pip install graphviz ET télécharger Graphviz depuis https://graphviz.org/download/")

# ------------------------------
# 6. Exécution MiniPython - VERSION CORRIGÉE
# ------------------------------
def execute(ast, symbol_table):
    runtime = {var: 0 for var in symbol_table.keys()}  # Initialiser à 0
   
    print("\n=== Début exécution ===")
   
    for stmt in ast:
        if stmt[0].startswith('Assign'):
            var = stmt[1][0].split(': ')[1]
            val_expr = stmt[1][1]  # L'expression à assigner
           
            if isinstance(val_expr, tuple) and val_expr[0] == 'Expr: +':
                # Gestion de l'addition: y = x + 2
                left_node = val_expr[1][0]
                right_node = val_expr[2][0]
               
                # Extraire les valeurs
                if 'Var:' in left_node:
                    left_var = left_node.split(': ')[1]
                    left_val = runtime[left_var]
                else:  # Const
                    left_val = int(left_node.split(': ')[1])
               
                if 'Const:' in right_node:
                    right_val = int(right_node.split(': ')[1])
                else:  # Var
                    right_var = right_node.split(': ')[1]
                    right_val = runtime[right_var]
               
                runtime[var] = left_val + right_val
                print(f"EXEC: {var} = {left_val} + {right_val} = {runtime[var]}")
               
            else:
                # Affectation simple: x = 5
                if isinstance(val_expr, tuple) and val_expr[0] == 'Expr':
                    if val_expr[1]:  # Vérifier que la liste n'est pas vide
                        value_node = val_expr[1][0]  # Premier élément de la liste
                    else:
                        value_node = 'Const: 0'  # Valeur par défaut
                else:
                    value_node = val_expr[0] if val_expr else 'Const: 0'
               
                if 'Const:' in value_node:
                    value = int(value_node.split(': ')[1])
                    runtime[var] = value
                    print(f"EXEC: {var} = {value}")
                elif 'Var:' in value_node:
                    source_var = value_node.split(': ')[1]
                    runtime[var] = runtime[source_var]
                    print(f"EXEC: {var} = {source_var} = {runtime[var]}")
                   
        elif stmt[0].startswith('Print'):
            var = stmt[1][0].split(': ')[1]
            print(f"PRINT: {runtime[var]}")
 
print("\n=== Exécution MiniPython ===")
execute(ast_semantic, symbol_table)
print("=== Fin exécution ===")
 