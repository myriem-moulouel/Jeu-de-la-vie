# Jeu-de-la-vie

## Présentation du projet
Il s'agit de programmer un Jeu De La Vie en python, en utilisant la synchronisation avec des threads

## Lancement du programme
* Télécharger le projet, lancer le fichier main.py avec une commande python du stype : python main.py
* S'assurer d'avoir les bibliothèques python requises comme pygame, threading, time
* Rentrer le nombre de lignes et de colonnes que vous désirez

<div style="display:flex">
     <div style="flex:1;padding-right:10px;">
          <img src="[img/image1.png](https://user-images.githubusercontent.com/60098131/211201593-3aafc3a9-5808-4015-9401-0f3dca57f237.png)" width="300"/>
     </div>
     <div style="flex:1;padding-left:10px;">
          <img src="[img/image2.png](https://user-images.githubusercontent.com/60098131/211201614-3a849ac4-9818-4b80-888f-9e71a25a5d13.png)" width="300"/>
     </div>
</div>

![image](https://user-images.githubusercontent.com/60098131/211201593-3aafc3a9-5808-4015-9401-0f3dca57f237.png)  |  ![image](https://user-images.githubusercontent.com/60098131/211201614-3a849ac4-9818-4b80-888f-9e71a25a5d13.png)

* Séléctionnez les cellules vivantes initiales de votre choix pour commencer le jeu avec le clique gauche de la souris, déséléctionnez avec le clique droit puis Entrer

![image](https://user-images.githubusercontent.com/60098131/211202186-6e43c27c-8eb6-4e70-a055-2a7f6c9f1790.png)

* Observez le jeu !

![image](https://user-images.githubusercontent.com/60098131/211202237-1a2f7da7-c14e-4a43-880d-59e8ec97656e.png)


## La partie synchronisée:
On a crée (nb lignes * nb colonnes) de threads qui s'executent à l'infini en calculant dans un premier temps le nombre de voisins de chaque cellule, puis dans un deuxième temps la valeur de la cellule à l'étape suivante. Pour s'assurer que le calcul du nombre de tous les voisins soit effectué avant d'entamer le changement de valeur aux cellules de la grille, on utilise deux barrières de synchronisation, l'une va s'assurer que le calcul du nombre de voisin est terminé et l'autre que le changement de cellule est terminé.
