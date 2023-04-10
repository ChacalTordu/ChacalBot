# CHACALBOT

**DESCRIPTION**
Chacalbot est un bot Discord destiné à aider les joueurs à gérer les événements de gaming sur leur serveur. Il dispose de fonctionnalités telles que l'affichage d'arbres de tournois et de poules, la création de tournois de jeux ou même de multigaming, avec des statistiques pour chaque joueur, des horaires d'événements et plus encore. 
Le projet est encore en cours de construction.

**Fonctionnalités**
Créer des tournois
Rejoindre/Quitter des tournois
Envoyer des messages d'aide

**Installation**
Clonez ce dépôt Git sur votre ordinateur

Mettez-vous dans l'environement en executant :
source ./monvenv/bin/activate

Installez les dépendances Python avec la commande pip install -r requirements.txt

Créez un fichier config.json à la racine du projet et ajoutez-y ce code :

{
    "bot_token": "votre_token",
    "command_prefix" : "§"
}

Lancez le bot avec la commande python main.py

**Utilisation**
Ajoutez votre bot Discord à votre serveur Discord en utilisant l'URL suivante :

bash
Copy code
https://discordapp.com/oauth2/authorize?&client_id=691306082475442217&scope=bot&permissions=8

Utilisez le préfixe definie dans votre json suivi de l'une des commandes disponibles pour utiliser votre bot.

§createtournament : Créer un tournoi
§join : Rejoindre un tournoi
§leave : Quitter un tournoi
§help : Afficher les commandes disponibles

**Contributions**
Les contributions sont les bienvenues ! Si vous souhaitez proposer des améliorations ou des fonctionnalités supplémentaires pour ce projet, n'hésitez pas à ouvrir une pull request.

**License**
Opensource, servez-vous