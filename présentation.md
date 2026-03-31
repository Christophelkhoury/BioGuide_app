# 1-Présentation générale du projet
Dans le cadre des Trophées NSI, dont le thème est informatique et nature, nous avons souhaité développer une application mettant en valeur les ressources naturelles souvent délaissées au profit de produits chimiques ou ultra-transformés.

L’idée est née d’un constat : pour des problèmes du quotidien (maux de tête, douleurs légères, inflammations…), les solutions systématiquement privilégiées sont les médicaments, alors que des alternatives naturelles existent.

Notre problématique initiale était donc :
comment utiliser l’informatique pour proposer des remèdes naturels fiables, accessibles et adaptés à des symptômes courants ?

Nous avons choisi de nous concentrer sur le domaine de la santé afin de concevoir une application utile et concrète.

Notre objectif est de développer une application capable d’analyser une demande utilisateur et de proposer des solutions naturelles adaptées, tout en sensibilisant à une consommation plus responsable.

Ce projet ne vise pas à remplacer les traitements médicaux pour des maladies graves, mais à proposer des alternatives naturelles pour des situations simples et sans danger.

# 2-Organisation du travail
## Présentation de l’équipe:
Notre groupe est formé de trois élèves de terminale au Grand Lycée Franco Libanais. Nous avons travaillé ensemble tout au long du dévéloppement de BioGuide, en s’entre aidant régulièrement pour partager les idées et améliorer l’application
o	Christophe El Khoury
o	Tia Kahil
o	Alaa Hamdan

## Rôle de chacun:
o	**Christophe**: dévéloppement principal de l’application comme la structure du site, gestion des pages, intégration avec Stramlit et organisation visuelle du site.

o	**Tia**: implémentation de l’IA comme le traitement des symptômes, la génération de réponses, l’exploitation des données des livres et montage de la vidéo.

o	**Alaa**: codage python d'une fonction qui utilise un systeme de mots clés pour retrouver les remèdes correspondants, design et expérience utilisateur comme l’interface et l’ergonomie.

## Répartition des tâches:
La documentation du projet a été fait collectivement, en répartissant des parties à rédiger puis une mise en commun.
Et le reste était un dévéloppement en groupe comme :
o	La conception de l’idée du projet
o	Le choix de fonctionnalités principales
o	Les tests
o	Les dernières améliorations

## Temps passé sur le projet:
Nous avons commencé à travailler sur l’application début janvier 2026, donc deux mois et demi de dévéloppement total. Nous avons pu nous répartir la tache avec des travaux personnels et des séances en groupe, formant plusieurs dizaines d’heures totales dédiées au projet.

# 3-Etapes du projet
Dans un premier temps, nous avons recherché une idée en lien avec le thème, puis défini notre problématique autour des remèdes naturels.

Nous avons ensuite effectué des recherches approfondies à partir de deux ouvrages de référence le médecin des pauvres ecrit par le docteur Beauvillard et La santé ou la medecine populaire de Jules Clément qui constituent la base des données utilisées dans notre application.

Une étape particulièrement importante et complexe de notre projet a été la récupération et l’exploitation des données issues des livres. En effet, ces ouvrages étant anciens et non structurés pour un usage informatique, il a été nécessaire de transformer leur contenu en données exploitables.
Pour cela, nous avons récupéré le contenu des livres grace a la version numérique du site gallica , puis nous avons utilisé Python pour traiter ces données.
Ensuite, nous avons du mettre en place un travail de nettoyage et de structuration du texte : avec la suppression des éléments inutiles, organisation des informations, et identification des parties importantes (symptômes, remèdes…).

Après, nous avons transformé ces données en une base de données manipulable en Python sous forme de structures de données SQL permettant de stocker les remèdes et les symptomes. Cela nous permet d'associer chaque symptôme à un ou plusieurs remèdes naturels et d'effectuer des recherches plus rapides et efficaces dans notre application.

Cette étape a été essentielle, car elle a permis de passer d’un contenu brut à une base exploitable par notre programme, et constitue le fondement de toute la logique de notre application.

Le cœur du projet repose sur un programme développé en Python, qui constitue l’élément central de notre application. Ce programme permet d’analyser les symptômes des utilisateurs , rechercher des correspondances dans une base de données, et de proposer des remèdes naturels adaptés.

Nous avons mis en place un système de recherche par mots-clés, permettant de faire correspondre les symptômes saisis avec les remèdes présents dans notre base.

Une forme d’intelligence artificielle (basée sur le traitement de texte et la correspondance de mots) a été intégrée afin d’améliorer la pertinence des réponses en analysant les requêtes de l’utilisateur.

Nous avons également développé un code permettant de retrouver la page exacte du livre et de l’afficher sous forme de lien, afin de pouvoir lire la page entière si on le souhaite.

Enfin, nous avons conçu une interface utilisateur permettant d’interagir avec le programme Python, rendant l’application accessible et intuitive.

# 4-Fonctionnement du projet
## Etat d’avancement et travail en groupe:
Au moment du dépôt, notre projet est complètement fonctionnel: l’utilisateur a la possibilité d’interagir avec l’interface, de décrire ses symptômes et d’obtenir des réponses pertinentes. Nous avons travaillé en collaboration tout au long du projet, en partageant régulièrement le dévéloppement de BioGuide en se servant de GitHub et en testant ensemble chaque nouvelle fonctionnalité pour assurer la cohérence de l’ensemble.

## Approches mises en œuvre pour vérifier l’absence de bugs:
En testant à plusieurs reprises, en particulier sur l’IA, par exemple en saisissant différents types de symptômes, nous avons pu vérifier la pertinence des réponses et leur cohérence. Nous avons aussi testé des cas extrêmes ou imprécis afin d’améliorer la rigourosité du système et corriger les erreurs retrouvées.

## Difficultés rencontrées et solutions apportées:
- Le problème le plus important concernait la structure de l’application. Au début, l’IA et la recherche étaient regroupées en une page, ce qui donnait des résultats peu pertinents. Nous avons alors séparé les fonctionnalités en deux pages, mais cela ne marchait pas non plus correctement. La solution était de combiner la recherche dans les ouvrages avec l’IA, permettant une analyse plus précise et des réponses plus cohérentes.

- Une autre difficulté était le prompt de l’IA: elle proposait des remèdes sans expliquer leur utilisation. Nous avons donc amélioré le prompt pour obtenir des réponses plus complètes, avec des instruction capables de guider l’utilisateur.

# 5-Ouverture
Pour améliorer notre projet, nous avons envisagé plusieurs pistes comme intégrer un système de filtrage prenant en compte les allergies, l’âge ou certaines conditions médicales, on a également pensé à ajouter une dimension culturelle en précisant l’origine des remèdes et leur histoire, ou à améliorer l’intelligence artificielle pour proposer des réponses plus précises et personnalisées.

En prenant du recul, notre projet pourrait sembler similaire à certaines intelligences artificielles existantes. Cependant, il se distingue par son ancrage dans des sources précises,	sa spécialisation dans les remèdes naturels datant des années 90, et sa volonté de sensibilisation écologique.

Néanmoins, certaines limites existent, notamment : une base de données encore limitée, une dépendance aux mots-clés, et l’absence de validation médicale complète.

Ce projet nous a permis de développer de nombreuses compétences comme la structuration et l’exploitation de bases de données, le traitement de texte, et surtout d’améliorer nos compétences en python en apprenant une nouvelle façon de coder un peu différente de celle qu’on a pu voir en classe.

Nous avons également intégré une démarche d’inclusion dans notre projet en proposant une interface simple, accessible à tous, en valorisant des solutions naturelles souvent utilisées dans différentes cultures, et en proposant une alternative accessible dans des contextes où l’accès aux médicaments peut être limité ou évitée.
