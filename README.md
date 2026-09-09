# 🎛️ Sequencer

## 📌 Présentation
**Sequencer** est un moteur de séquences programmable permettant d’enchaîner des actions selon une timeline, des pas, ou des événements.  
Le projet fournit une architecture simple, extensible et modulaire pour créer, éditer et exécuter des séquences dans un environnement embarqué ou applicatif.

Il est conçu pour être :
- **Précis** — timing stable, gestion fine des steps.  
- **Flexible** — actions personnalisables, plugins, drivers.  
- **Portable** — aucune dépendance lourde, compatible microcontrôleurs et environnements desktop.  
- **Lisible** — code structuré, documentation claire, logique simple à suivre.

## 🚀 Fonctionnalités principales
- Gestion d’une **timeline** ou d’une **step list**.  
- Exécution séquentielle, parallèle ou conditionnelle.  
- Système d’**actions** extensible (callbacks, lambdas, drivers).  
- Support des **boucles**, **triggers**, **événements**.  
- Mode **simulation** pour tester les séquences sans matériel.  
- API simple pour créer, charger, sauvegarder des séquences.  
- Hooks pour instrumentation, logs, monitoring.

## 🧱 Architecture cible

```
/src
 ├── core/
 │    ├── sequencer.py        # Moteur principal
 │    ├── timeline.py         # Gestion du temps et des steps
 │    ├── action.py           # Interface des actions
 │    └── scheduler.py        # Orchestration et exécution
 ├── drivers/
 │    └── ...                 # Actions spécifiques (IO, hardware, etc.)
 ├── utils/
 │    └── logger.py           # Logs, instrumentation
/tests
 └── ...                      # Tests unitaires
```

## 📦 Installation
### Prérequis

- Python ≥ 3.10  
- (Optionnel) Matériel ou drivers spécifiques selon les actions

### Installation

```bash
git clone https://github.com/ton-projet/sequenceur.git
cd sequenceur
pip install -r requirements.txt
```

## 🧪 Exemple minimal

Voici un exemple simple de création et exécution d’une séquence :

```python
from sequenceur import Sequencer, Action

class PrintAction(Action):
    def run(self, context):
        print(f"Step: {context['step']}")

seq = Sequencer()

seq.add_step(time=0.0, action=PrintAction())
seq.add_step(time=1.0, action=PrintAction())
seq.add_step(time=2.0, action=PrintAction())

seq.run()
```

## ⚙️ Configuration

Le séquenceur peut être configuré via :

- un fichier `config.yaml`
- des paramètres passés au constructeur
- des options runtime (mode simulation, vitesse, logs)

Exemple de configuration YAML :

```yaml
sequencer:
  mode: simulation
  speed: 1.0
  log_level: info
```

## 📚 Documentation

La documentation complète couvre :

- l’API du séquenceur  
- la création d’actions personnalisées  
- l’intégration dans un projet embarqué  
- les drivers disponibles  
- les bonnes pratiques de timing  

👉 Elle est disponible dans `/docs` ou via MkDocs si tu l’utilises.

## 🧩 Roadmap

Dans mes rêves :

- [ ] Éditeur graphique de séquences  
- [ ] Export/import JSON  
- [ ] Actions asynchrones  
- [ ] Support MIDI / DMX / GPIO selon le contexte  
- [ ] Intégration avec asyncio  

## 🤝 Contribution

Les contributions sont évidemment les bienvenues :

1. Fork du repo  
2. Création d’une branche  
3. Commit clair et structuré  
4. Pull request avec description détaillée  

## 📄 Licence

Ce projet est distribué sous licence MIT (modifiable selon ton besoin).

## 🔧 Auteur

Projet développé par **Marc**, passionné d’embedded, d’architecture logicielle et de systèmes temps réel.
