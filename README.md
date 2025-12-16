# 🐍 TP2 — MiniPython (Analyse avec Lark)

<div align="center">

![MiniPython Logo](C:\Users\Testing\python\Compilation\TP2\assets\logo.png)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Lark](https://img.shields.io/badge/Lark-Parser-green.svg)](https://github.com/lark-parser/lark)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**Un compilateur éducatif pour MiniPython utilisant Lark**

[Installation](#-installation) • [Utilisation](#-utilisation) • [Exemples](#-exemples) • [Documentation](#-documentation)

</div>

---

## 📖 Description

Un projet pédagogique complet qui implémente un analyseur syntaxique pour le langage **MiniPython** en utilisant le parser **Lark**. Ce projet permet de :

- ✅ Définir une grammaire formelle avec Lark
- ✅ Analyser du code source MiniPython
- ✅ Générer un Arbre de Syntaxe Abstraite (AST)
- ✅ Visualiser l'AST avec Graphviz
- ✅ Apprendre les concepts de compilation

### 🎯 Objectifs Pédagogiques

- Comprendre les grammaires formelles (BNF/EBNF)
- Maîtriser l'utilisation de Lark pour le parsing
- Générer et manipuler des AST
- Visualiser la structure syntaxique d'un programme

---

## 📦 Contenu du Projet

```
TP2-MiniPython-Lark/
│
├── assets/
│   └── images/
│       ├── logo.png
│       └── logo.svg
│
├── Codes_Sources/
│   ├── minipython_complete.py      # Script principal d'analyse
│   ├── prgPythonPur.py             # Exemples de programmes
│   └── Analyse_Lark_Automatique/
│       ├── analyse_*.py            # Scripts d'analyse spécifiques
│       └── sorties/                # Résultats d'analyse
│
├── version_lark/
│   ├── minipython.lark             # Version alternative de la grammaire
│   └── archives/                   # Versions historiques
│
├── grammaire/
│   └── minipython.lark             # Grammaire principale Lark
│
├── exemples/
│   ├── exemple.minipy              # Programme exemple simple
│   ├── exemple_avance.minipy       # Programme avec structures complexes
│   └── test_complet.minipy         # Test de toutes les fonctionnalités
│
├── output/
│   ├── ast.dot                     # AST en format Graphviz
│   ├── ast_lark.dot                # AST généré par Lark
│   └── ast_temp.dot                # AST temporaire
│
├── tests/
│   └── test_parser.py              # Tests unitaires (à venir)
│
├── README.md                       # Ce fichier
├── LICENSE                         # Licence MIT
└── requirements.txt                # Dépendances Python
```

---

## ⚙️ Prérequis

### Logiciels Requis

- **Python 3.10+** (testé avec Python 3.10, 3.11, 3.12)
- **pip** (gestionnaire de paquets Python)
- **Graphviz** (optionnel, pour visualiser les AST)

### Installation de Graphviz (Optionnel)

#### Windows
```bash
# Avec Chocolatey
choco install graphviz

# Ou télécharger depuis : https://graphviz.org/download/
```

#### macOS
```bash
brew install graphviz
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install graphviz
```

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/TP2-MiniPython-Lark.git
cd TP2-MiniPython-Lark
```

### 2. Créer un environnement virtuel (Recommandé)

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt` :**
```
lark-parser>=1.1.0
graphviz>=0.20.0
```

---

## 🎮 Utilisation

### Analyse Simple

Analyser un fichier MiniPython et afficher l'AST :

```bash
python Codes_Sources/minipython_complete.py exemples/exemple.minipy
```

### Options Disponibles

```bash
# Afficher l'AST en mode texte
python Codes_Sources/minipython_complete.py exemple.minipy --text

# Générer un fichier DOT pour Graphviz
python Codes_Sources/minipython_complete.py exemple.minipy --dot output/ast.dot

# Mode verbose (afficher les détails)
python Codes_Sources/minipython_complete.py exemple.minipy --verbose

# Générer l'image de l'AST directement (nécessite Graphviz)
python Codes_Sources/minipython_complete.py exemple.minipy --output ast.png
```

### Visualiser l'AST avec Graphviz

Si vous avez généré un fichier `.dot` :

```bash
# Générer une image PNG
dot -Tpng output/ast.dot -o output/ast.png

# Générer un PDF
dot -Tpdf output/ast.dot -o output/ast.pdf

# Générer un SVG
dot -Tsvg output/ast.dot -o output/ast.svg
```

---

## 📝 Exemples

### Exemple 1 : Programme Simple

**Fichier : `exemples/exemple_simple.minipy`**

```python
/* Programme simple MiniPython */

int x;
int y;

x = 10;
y = 20;

if (x < y) {
    print("x est plus petit que y");
} else {
    print("x est plus grand ou égal à y");
}
```

**Exécution :**
```bash
python Codes_Sources/minipython_complete.py exemples/exemple_simple.minipy
```

**Sortie attendue :**
```
✅ Analyse réussie !
Programme analysé avec succès.
AST généré : output/ast.dot
```

### Exemple 2 : Boucles et Tableaux

**Fichier : `exemples/exemple_boucle.minipy`**

```python
/* Boucle while et tableaux */

int tableau[5];
int i;
int somme;

i = 0;
somme = 0;

while (i < 5) {
    tableau[i] = i * 2;
    somme = somme + tableau[i];
    i = i + 1;
}

print(somme);
```

### Exemple 3 : Procédures

**Fichier : `exemples/exemple_procedure.minipy`**

```python
/* Définition et appel de procédure */

def procedure afficherMessage(string msg) {
    print(msg);
    return;
}

def procedure calculer(int a, int b) {
    int resultat;
    resultat = a + b;
    print(resultat);
    return;
}

string message;
message = "Bonjour MiniPython !";
afficherMessage(message);

int x;
int y;
x = 15;
y = 25;
calculer(x, y);
```

---

## 🔧 Grammaire MiniPython

### Fonctionnalités Supportées

| Fonctionnalité | Syntaxe | Exemple |
|----------------|---------|---------|
| **Déclarations** | `type identifiant;` | `int x;` |
| **Tableaux** | `type id[taille];` | `int tab[10];` |
| **Matrices** | `type id[n][m];` | `float mat[3][3];` |
| **Affectation** | `id = expr;` | `x = 5 + 3;` |
| **Conditions** | `if (cond) {...} else {...}` | `if (x > 0) {...}` |
| **Boucles** | `while (cond) {...}` | `while (i < 10) {...}` |
| **Affichage** | `print(expr);` | `print("Hello");` |
| **Procédures** | `def procedure nom(params) {...}` | Voir exemples |
| **Commentaires** | `/* ... */` | `/* commentaire */` |
| **Opérateurs arithmétiques** | `+ - * / ()` | `(a + b) * c` |
| **Opérateurs logiques** | `&& || !` | `(x > 0) && (y < 10)` |
| **Comparaisons** | `< > == !=` | `x == 5` |

### Types de Données

- `int` — Entier
- `float` — Nombre à virgule flottante
- `bool` — Booléen (true/false)
- `string` — Chaîne de caractères

### Extrait de la Grammaire Lark

```lark
// Fichier: minipython.lark

start: program

program: (declaration | statement)*

declaration: type IDENTIFIER ("," IDENTIFIER)* ";"
           | type IDENTIFIER "[" NUMBER "]" ";"
           | type IDENTIFIER "[" NUMBER "]" "[" NUMBER "]" ";"

type: "int" | "float" | "bool" | "string"

statement: assignment
         | if_statement
         | while_statement
         | print_statement
         | procedure_declaration

assignment: IDENTIFIER "=" expression ";"

expression: term
          | expression "+" term
          | expression "-" term

term: factor
    | term "*" factor
    | term "/" factor

factor: IDENTIFIER
      | NUMBER
      | "(" expression ")"
      | "true"
      | "false"
      | STRING

// ... (reste de la grammaire)
```

---

## 🧪 Tests & Validation

### Exécuter les Tests

```bash
# Tests unitaires (à venir)
python -m pytest tests/

# Test manuel avec un exemple
python Codes_Sources/minipython_complete.py exemples/test_complet.minipy
```

### Validation des Exemples

Pour valider que tout fonctionne correctement :

```bash
# Tester tous les exemples
for file in exemples/*.minipy; do
    echo "Testing $file..."
    python Codes_Sources/minipython_complete.py "$file"
done
```

### Vérifier la Génération des AST

Après l'analyse, vérifiez que les fichiers `.dot` sont créés dans `output/` :

```bash
ls -lh output/*.dot
```

---

## 📚 Documentation

### Architecture du Projet

1. **Grammaire Lark** (`minipython.lark`)
   - Définit la syntaxe du langage MiniPython
   - Utilise la notation EBNF

2. **Parser** (`minipython_complete.py`)
   - Lit le fichier source
   - Applique la grammaire Lark
   - Génère l'AST

3. **Générateur AST**
   - Transforme l'arbre de parsing en AST
   - Exporte en format DOT pour Graphviz

### Comment Lark Fonctionne

Lark utilise une approche déclarative :

```python
from lark import Lark, Transformer

# 1. Charger la grammaire
parser = Lark.open('minipython.lark', start='program')

# 2. Parser le code
tree = parser.parse(code_source)

# 3. Transformer l'arbre (optionnel)
class MiniPythonTransformer(Transformer):
    def declaration(self, items):
        # Traiter les déclarations
        pass

transformer = MiniPythonTransformer()
ast = transformer.transform(tree)
```

### Ressources Utiles

- [Documentation officielle Lark](https://lark-parser.readthedocs.io/)
- [Tutoriel Lark](https://lark-parser.readthedocs.io/en/latest/json_tutorial.html)
- [Grammaire EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)
- [Graphviz Documentation](https://graphviz.org/documentation/)

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment participer :

### 1. Forker le Projet

```bash
# Cliquez sur "Fork" sur GitHub
git clone https://github.com/votre-username/TP2-MiniPython-Lark.git
```

### 2. Créer une Branche

```bash
git checkout -b feature/amelioration-grammaire
```

### 3. Faire vos Modifications

- Améliorez la grammaire
- Ajoutez des exemples
- Corrigez des bugs
- Améliorez la documentation

### 4. Committer et Pousser

```bash
git add .
git commit -m "Ajout: support des fonctions avec retour"
git push origin feature/amelioration-grammaire
```

### 5. Ouvrir une Pull Request

- Allez sur GitHub
- Cliquez sur "New Pull Request"
- Décrivez vos changements

### Idées de Contributions

- [ ] Ajouter des tests unitaires complets
- [ ] Supporter les fonctions avec valeur de retour
- [ ] Ajouter le type `char`
- [ ] Implémenter la boucle `for`
- [ ] Ajouter des opérateurs bit à bit
- [ ] Créer un interpréteur pour exécuter le code
- [ ] Améliorer les messages d'erreur
- [ ] Ajouter un mode interactif (REPL)

---

## 🐛 Rapport de Bugs

Si vous trouvez un bug, veuillez ouvrir une **issue** sur GitHub avec :

1. **Description du problème**
2. **Étapes pour reproduire**
3. **Comportement attendu vs observé**
4. **Fichier MiniPython problématique**
5. **Message d'erreur complet**
6. **Version de Python utilisée**

**Template d'issue :**

```markdown
## Bug Description
[Description claire du bug]

## Reproduction
1. Créer le fichier `bug.minipy` avec ce contenu : ...
2. Exécuter : `python minipython_complete.py bug.minipy`
3. Observer l'erreur : ...

## Comportement Attendu
[Ce qui devrait se passer]

## Comportement Observé
[Ce qui se passe réellement]

## Environnement
- Python : 3.12
- Lark : 1.1.9
- OS : Windows 11
```

---

## 👥 Contributeurs

### Équipe de Développement

- **Votre Nom** - *Développeur Principal* - [@votre-github](https://github.com/votre-username)
- **Nom Binôme** - *Co-Développeur* - [@binome-github](https://github.com/binome-username)

### Encadrement Pédagogique

- **Dr. Nom Enseignant** - *Encadrant*
- **Université Abou Bekr Belkaid** - Tlemcen, Algérie
- **Département d'Informatique** - 4ème année Ingénieur Génie Logiciel

### Remerciements

Un grand merci à :
- L'équipe **Lark** pour leur excellent parser
- La communauté **Python** pour les outils et bibliothèques
- Tous les contributeurs qui ont amélioré ce projet

---

## 📄 Licence

Ce projet est sous licence **MIT License**.

```
MIT License

Copyright (c) 2025 [Votre Nom]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🎓 Contexte Académique

### Informations du Cours

- **Matière** : Compilation 2
- **Niveau** : 4ème année Ingénieur Génie Logiciel
- **Établissement** : Université Abou Bekr Belkaid - Tlemcen
- **Département** : Informatique
- **Année Universitaire** : 2024/2025
- **Semestre** : Automne 2025

### Objectifs du TP

Ce TP vise à :
1. Comprendre les phases de compilation (analyse lexicale/syntaxique)
2. Maîtriser l'utilisation d'un générateur de parser (Lark)
3. Manipuler les arbres syntaxiques abstraits (AST)
4. Visualiser et déboguer des structures d'arbres
5. Documenter un projet logiciel

---

## 📞 Contact

Pour toute question ou suggestion :

- **Email** : votre.email@etu.univ-tlemcen.dz
- **GitHub** : [@votre-username](https://github.com/votre-username)
- **Issues** : [GitHub Issues](https://github.com/votre-username/TP2-MiniPython-Lark/issues)

---

## 🗺️ Roadmap

### Version Actuelle (v1.0)
- [x] Grammaire Lark fonctionnelle
- [x] Parser opérationnel
- [x] Génération d'AST en format DOT
- [x] Exemples de base

### Prochaines Versions

#### v1.1 (Court terme)
- [ ] Tests unitaires complets
- [ ] Amélioration des messages d'erreur
- [ ] Documentation API complète

#### v1.2 (Moyen terme)
- [ ] Support des fonctions avec retour
- [ ] Boucle `for`
- [ ] Opérateurs supplémentaires

#### v2.0 (Long terme)
- [ ] Interpréteur fonctionnel
- [ ] Optimisation de code
- [ ] Génération de code machine

---

## 📊 Statistiques du Projet

![GitHub repo size](https://img.shields.io/github/repo-size/votre-username/TP2-MiniPython-Lark)
![GitHub code size](https://img.shields.io/github/languages/code-size/votre-username/TP2-MiniPython-Lark)
![Lines of code](https://img.shields.io/tokei/lines/github/votre-username/TP2-MiniPython-Lark)

---

## 🔗 Liens Utiles

- [GitHub Repository](https://github.com/votre-username/TP2-MiniPython-Lark)
- [Documentation Lark](https://lark-parser.readthedocs.io/)
- [Python Official Docs](https://docs.python.org/3/)
- [Graphviz Gallery](https://graphviz.org/gallery/)

---

<div align="center">

**Fait avec ❤️ à l'Université de Tlemcen**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Lark](https://img.shields.io/badge/Lark-Parser-green?style=for-the-badge)
![Graphviz](https://img.shields.io/badge/Graphviz-Visualization-orange?style=for-the-badge)

⭐ **N'oubliez pas de mettre une étoile si ce projet vous a aidé !** ⭐

</div>#   T P 2 - M i n i P y t h o n - L a r k  
 