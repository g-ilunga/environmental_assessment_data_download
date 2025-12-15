# Project Name

[English version →](README.en.md) | [Version Française →](README.fr.md)


# 🗺️ Outil de Téléchargement des Données Environnementales

## 🧭 Présentation de l’outil

### ⚙️ Contexte  
Dans le cadre d’un projet ou par curiosité personnelle, on peut être amené à se poser la question sur les enjeux environnementaux présents dans le périmètre d’une aire d’étude.  
Pour répondre à cette question, une pratique courante consiste à télécharger les données environnementales (ZNIEFF, sites Natura 2000, géologie, etc.) à partir de différents portails, puis à les importer dans un logiciel SIG (QGIS ou ArcGIS) pour réaliser les analyses.

Cependant, la multiplicité de ces portails rend le processus long et fastidieux.  
C’est dans ce contexte qu’est née **l’idée de centraliser sur une plateforme le téléchargement de toutes les données nécessaires à une évaluation environnementale.**

---

### 🧰 Description de l’outil  
Au lieu de se rendre sur plusieurs plateformes, **l’outil centralise le téléchargement** des données environnementales.

#### Fonctionnement :  
1. L’utilisateur renseigne la **commune** dans laquelle se trouve son projet.  
2. Grâce aux **API** (notamment le flux **WFS** de l’IGN Géoservices), la plateforme se connecte aux différentes bases de données.  
3. Les **données environnementales intersectant la commune** sont téléchargées automatiquement.

#### Données actuellement prises en compte :  
- ZNIEFF  
- Sites Natura 2000  
- Parcs Naturels Régionaux  
- Parcs Naturels Marins  
- Parcs Nationaux  
- Servitudes (sites inscrits/classés, monuments historiques, etc.)  
- PLU et PLUi  

---

### 🚧 Limites et perspectives  
- Seules les données répertoriées dans la **base de données de l’IGN** et disponibles via **flux WFS** sont actuellement prises en charge.  
- D’autres types de données seront ajoutés progressivement.  
- L’outil est aujourd’hui un **script Python**, mais une **interface graphique** est prévue dans les prochaines étapes.

---

## 💻 Développement technique de l’outil

- **Langage :** Python 3.10  
- **Structure modulaire :** plusieurs scripts, chacun avec une fonctionnalité spécifique.

### 📂 Arborescence du projet

| Dossier / Fichier                  | Description                                  |
|-----------------------------------|----------------------------------------------|
| **municipalities_dataset/**        | Contient les données des communes             |
| ├── `municipalities_boundary.gpkg` | Emprises des communes                          |
| └── `municipalities_points.csv`   | Coordonnées géographiques de chaque commune   |
| **config_dataset.json**            | Liste des données environnementales et leurs paramètres |
| **config_urls.json**               | URLs utilisées par l’outil                    |
| **download_functions.py**          | Fonctions de téléchargement                    |
| **xml_builder.py**                 | Construction des requêtes de recherche        |
| **xml_builder_gpu.py**             | Requêtes pour le Géoportail de l’Urbanisme    |
| **main.py**                        | Script principal (point d’entrée de l’outil). C'est ce script qui est utilisé pour lancer l'outil  |
| **requirements.txt**               | Liste des dépendances Python                   |

---
