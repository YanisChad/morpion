Ce programme est le jeu du Morpion utilisant la bibliothèque tkinter pour créer une interface graphique.

Le jeu est implémenté dans la classe Morpion, qui contient l'état du jeu, y compris le tour du joueur actuel, l'état du plateau, la liste des coups joués et la progression du jeu. La progression du jeu est stockée dans un DataFrame Pandas et exportée dans un fichier CSV après chaque coup.

La classe Case représente une cellule du plateau de jeu et gère les entrées de l'utilisateur en liant une méthode cliqeur() au bouton. Cette méthode ajoute le coup en cours au plateau et appelle la méthode jouer() de la classe Morpion pour mettre à jour l'état du jeu. Elle met également à jour le texte du bouton pour afficher le coup du joueur en cours.

La classe IA implémente une IA de base qui joue le jeu automatiquement. Elle utilise une simple heuristique pour déterminer le meilleur coup en évaluant le potentiel de chaque cellule vide sur le plateau.

La classe Application met en place l'interface graphique et crée le plateau de jeu en créant une instance de la classe Case pour chaque case.

La méthode counter_result() est utilisée pour compter le nombre de victoires de chaque joueur et le nombre d'égalités en lisant le fichier CSV exporté.

La méthode visualiser_graphique() utilise les données obtenues par la méthode counter_result() pour tracer un diagramme à barres à l'aide de matplotlib.

Le code gère également le cas où l'utilisateur clique sur le bouton replay, ce qui réinitialise l'état du jeu et recrée le plateau de jeu.

Traduit avec www.DeepL.com/Translator (version gratuite)
