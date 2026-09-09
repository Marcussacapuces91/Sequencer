# 📘 DRUM‑ASCII v1.3 — Spécification complète

## 1. Structure générale du fichier
Un fichier DRUM‑ASCII v1.3 contient, dans cet ordre :

1. **Entête** (métadonnées)
2. **Sections** (avec mesures)
3. **Bloc INSTRUMENTS** (définition des voies)
4. **Bloc PLAYORDER** (ordonnancement final)

Les blocs 1 et 2 sont obligatoires.  
Les blocs 3 et 4 sont optionnels.

---

## 2. Entête
Bloc simple, lignes `clé: valeur` :

```
FORMAT: DRUM-ASCII
TITLE: <titre>
TEMPO: <bpm>
TIME: <signature>
```

Clés obligatoires : `FORMAT`, `TITLE`, `TEMPO`, `TIME`.

---

## 3. Sections
Une section commence par :

```
SECTION: <nom>
```

Elle contient une liste ordonnée de mesures.

---

## 4. Mesures
Une mesure commence par :

```
MEASURE: <numéro>
```

Elle contient une ou plusieurs lignes d’instruments :

```
<ALIAS>: <pattern ASCII>
```

Exemple :

```
HH: x x x x x x x x
SN: - o - o - - - -
BD: o - o - - - - -
```

### Règles :
- Le pattern est une **liste de symboles séparés par des espaces**.
- La subdivision est déterminée par le **nombre de colonnes**.
- Les alias doivent correspondre à des instruments définis dans le bloc INSTRUMENTS (si présent).

---

## 5. Bloc INSTRUMENTS
Bloc optionnel, placé **avant** le PLAYORDER.

Syntaxe :

```
INSTRUMENTS:
  ALIAS = Name(param1=val1, param2=val2, ...)
```

Exemples :

```
INSTRUMENTS:
  HH = HiHatClosed(class=HiHat, pitch=42, velocity=90)
  SN = Snare(class=Snare, pitch=38, velocity=100)
  BD = Kick(class=Kick, pitch=36, velocity=110)
```

### Règles :
- `ALIAS` est le nom utilisé dans les mesures.
- `Name` est le nom de l’instrument logique.
- Les paramètres sont passés au constructeur interne du moteur.
- Les valeurs peuvent être : `int`, `float`, `string`.

---

## 6. Bloc PLAYORDER
Bloc optionnel, placé **à la fin du fichier**.

S’il est absent → ordre par défaut = ordre de découverte des sections.

Syntaxe :

```
PLAYORDER: <expression>
```

### 6.1. Répétition simple
```
INTRO*3
```

### 6.2. Liste
```
INTRO*1, VERSE*4, CHORUS*2
```

### 6.3. Groupes
```
[VERSE, CHORUS]*2
(A, B)*3
```

### 6.4. Groupes imbriqués
```
([A, B]*2, C)*3
```

### 6.5. Règles de grammaire
- Séparateur : `,`
- Répétition : `*N`
- Groupes : `[...]` ou `(...)`
- Les noms doivent correspondre à des sections existantes.

Le PLAYORDER est transformé en une **liste flattenée** de noms de sections.
