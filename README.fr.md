Contexte

Dans le cadre d'une evaluation environnementale ou lors de la réalisation d'un premier diagnostic rapide, l'une des étapes essentielles est la collecte des données environnementales. Ce processus implique dans un premier temps d'aller chercher les données qui se trouvent sur les plateformes publiques comme Géoportail, Géoportail  de l'urbanisme  ou encore Géorisques. Cependant, cette étape peut être chronophage car il faut parcourir différentes plateformes pour récupérer les informations dont on a besoin. D'autre part, l'IGN, l’Institut national de l’information géographique et forestière,  qui est l'opérateur de référence pour l'information géographique et forestière en France a développé un certain nombre d'API afin de permettre aux utilisateurs expérimentés d'avoir accès à ces données publiques et realiser des traitements avancés qui ne sont toujours pas possible de realiser sur les plateformes ci-dessus.

C'est à la suite de ce constat qu'est né l'idée de développer un outil pour simplifier ce processus de collecte des données afin de dédier plus de temps à l'analyse et à l'évaluation environnementale. Dans cet outil, il y a deux modules:
⦁	Le module de téléchargement des données
⦁	Le module de diagnostic rapide des enjeux:
Ces deux modules viennent exploiter les API mis en place par l'IGN

Module de téléchargement

ce module permet de télécharger uniquement les données qui sont souvent utilisées lors des évaluations environnementales. Ainsi, il n'est plus nécessaire de parcourir différentes plateformes pour récupérer la donnée.
Le principe de fonctionnement est le suivant. L'utilisateur renseigne la commune dans laquelle se trouve le projet et l'outil va récupérer les données environnementales qui concernent la commune. Les données téléchargées sont dans un format exploitable sous QGIS ou ArcGIS.
A ce jour, le module permet de télécharger les données suivantes:
⦁	ZNIEFF
⦁	Sites Natura 2000
⦁	Parcs Naturels Régionaux
⦁	Parcs Naturels Marins
⦁	Parcs Nationaux
⦁	Servitudes (sites inscrits/classés, monuments historiques, etc.)
⦁	PLU et PLUi


Module de diagnostic rapide des enjeux

ce module permet de réaliser un diagnostic rapide des enjeux environnementaux en utilisant aussi les données environnementales les plus utilisées dans les évaluations environnementales.
Le principe de fonctionnement est le suivant. L'utilisateur importe l’emprise de l'aire d’étude et l'outil retourne la liste des enjeux environnementaux qui concernent l'aire d’étude. A ce jour l’outil permet de déterminer si vous êtes concerné par les périmètres suivants:
⦁	ZNIEFF
⦁	Sites Natura 2000
⦁	Parcs Naturels Régionaux
⦁	Parcs Naturels Marins
⦁	Parcs Nationaux
⦁	Servitudes (sites inscrits/classés, monuments historiques, etc.)
⦁	L’outil vous permet aussi de déterminer les zones urbaines du PLU/PLUi que votre aire d’étude intercepte. Il ne permet pas encore de déterminer si l'aire d'étude est concernée par d'autres prescriptions comme emplacement réservé, espace boisé classé, alignement d'arbres, etc.


Perspectives
L’outil est encore au niveau de prototype et en cours de développement. Il est prévu de développer une interface graphique.
Seules les données répertoriées dans la base de données de l’IGN et disponibles via le flux WFS Géoportail sont actuellement prises en charge. D’autres types de données seront progressivement ajoutés.
