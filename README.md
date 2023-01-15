# Jeu-de-la-vie

## Mini-projet : Le Jeu de la Vie
Le jeu de la vie de Conway représente l'évolution d'une population de cellules contenue dans un tableau bidi-
mensionnel. Chaque case du tableau contient 0 ou 1 cellule et on simule l’ ́evolution de la population en divisant le
temps en une suite d’instants et en calculant (suivant des règles décrites plus loin) la population à chaque instant.

## Régles d'évolution :
Pour savoir l'état d’une case à l'étape n + 1, on regarde son état et celui de ses 8 voisines à l'instant n.
— Si elle est vide et qu’elle a exactement 3 cases voisines occup ́ees, elle devient occup ́ee par une nouvelle
cellule. Sinon elle reste vide.
— Si elle est occup ́ee et qu’elle a exactement 2 ou 3 cases voisines  ́egalement occup ́ees, la cellule qui occupe
la case survit. Sinon le cellule disparaˆıt.

## Présentation du projet
Il s'agit de programmer un Jeu De La Vie en python, en utilisant la synchronisation avec des threads.
* Première approche : séquencielle, sans synchronisation, dans le fichier `main_sequencial.py`.
* Deuxième approche : n_row * n_col threads qui calculent les (n_row * n_col) cases de la grille, dans le fichier `main_synchro.py`.
 
## Lancement du programme
* Télécharger le projet, lancer le fichier main.py avec une commande python du stype : `python main_synchro.py` pour lancer la version synchronisée et `python main_sequencial.py` pour lancer la version séquencielle.
* S'assurer d'avoir les bibliothèques python requises comme pygame, threading, time.

Si elle n'est pas déjà installée pygame : https://www.pygame.org/wiki/GettingStarted 
* Rentrer le nombre de lignes et de colonnes que vous désirez

<div id="image-table">
    <table>
	    <tr>
    	    <td style="padding:10px">
        	<img src="https://user-images.githubusercontent.com/60098131/211201593-3aafc3a9-5808-4015-9401-0f3dca57f237.png" width="400"/>
      	    </td>
            <td style="padding:10px">
            	<img src="https://user-images.githubusercontent.com/60098131/211201614-3a849ac4-9818-4b80-888f-9e71a25a5d13.png" width="400"/>
            </td>
        </tr>
    </table>
</div>

* Séléctionnez les cellules vivantes initiales de votre choix pour commencer le jeu avec le clique gauche de la souris, déséléctionnez avec le clique droit puis Entrer

* Observez le jeu !

<div id="image-table2">
    <table>
	    <tr>
    	    <td style="padding:10px">
        	<img src="https://user-images.githubusercontent.com/60098131/211202186-6e43c27c-8eb6-4e70-a055-2a7f6c9f1790.png" width="400"/>
      	    </td>
            <td style="padding:10px">
            	<img src="https://user-images.githubusercontent.com/60098131/211202237-1a2f7da7-c14e-4a43-880d-59e8ec97656e.png" width="400"/>
            </td>
        </tr>
    </table>
</div>

## La partie synchronisée:
On a crée (nb lignes * nb colonnes) de threads qui s'executent à l'infini en calculant le nombre de voisins de chaque cellule, puis la valeur de la cellule à l'étape suivante. 

Pour s'assurer que le calcul du nombre de tous les voisins soit effectué avant d'entamer le changement de valeur aux cellules de la grille, on utilise deux barrières de synchronisation, l'une va s'assurer que le calcul du nombre de voisin est terminé et l'autre que le changement de cellule est terminé.

## Variables globales:
Écrites dans le fichier `Ressources/variables.py`

* La largeur et la hauteur de la grille :
Width, Height = 700, 700

* Les couleurs utilisées pour l'affichage des cases de la grille :
White = (255, 255, 255)
Black = (0, 0, 0)

* Variable utilisée dans la version synchronisée pour ralentir l'affichage via la thread `self.time_barrier` :
REFRESH_RATE = 0.25
