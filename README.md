# Jeu-de-la-vie

## Présentation du projet
Il s'agit de programmer un Jeu De La Vie en python, en utilisant la synchronisation avec des threads
 
## Lancement du programme
* Télécharger le projet, lancer le fichier main.py avec une commande python du stype : python main.py
* S'assurer d'avoir les bibliothèques python requises comme pygame, threading, time.

Si elles sont pas déjà installées pygame : https://www.pygame.org/wiki/GettingStarted 
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
On a crée (nb lignes * nb colonnes) de threads qui s'executent à l'infini en calculant dans un premier temps le nombre de voisins de chaque cellule, puis dans un deuxième temps la valeur de la cellule à l'étape suivante. Pour s'assurer que le calcul du nombre de tous les voisins soit effectué avant d'entamer le changement de valeur aux cellules de la grille, on utilise deux barrières de synchronisation, l'une va s'assurer que le calcul du nombre de voisin est terminé et l'autre que le changement de cellule est terminé.
