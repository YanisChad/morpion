import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import os
import matplotlib.pyplot as plt
import csv

class Morpion:
    def __init__(self):
        self.grille = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.coups = []
        self.tour = 0
        self.dict = {(0,0):0, (0,1):0, (0,2):0, (1,0):0, (1,1):0, (1,2):0, (2,0):0, (2,1):0, (2,2):0}

    # Méthode pour jouer un coup
    def jouer(self, ligne, colonne):
        self.joueur_actuel = "X"
        joueur = "X"

        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = joueur
            # Charger le fichier CSV existant s'il existe, sinon créer un nouveau DataFrame
            if os.path.exists("coups.csv"):
                self.df = pd.read_csv("coups.csv", sep=';')
            else :
                self.df = pd.DataFrame(columns=["tour", "joueur", "ligne", "colonne", "win_by"])

            # Ajouter le coup joué au DataFrame et enregistrer le coup
            if self.est_gagne() == False and self.est_plein() == False:
                self.coups.append((self.tour, joueur, ligne, colonne, "X" if self.est_gagne() else "not_finished"))

            # Si le joueur gagne, ajouter le coup gagnant au DataFrame et enregistrer
            if (self.est_gagne() == True):
                self.coups.append((self.tour, joueur, ligne, colonne, "X"))
                self.export_df(ligne, colonne, joueur,"won")

            # exporter le df dans le cas d'une égalité
            if (self.tour == 8 and self.est_gagne() == False and self.est_plein() == True):
                self.coups.append((self.tour, "X", ligne, colonne, "draw"))
                self.export_df(ligne, colonne, joueur, "draw")
            self.tour += 1
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")

    def trouver_partie_similaire(self, new_df, df):
        for i in range(len(df)):
            df1_partie = df.iloc[i, 1:] # Extraire une partie de la première dataframe
            for j in range(len(new_df)):
                df2_partie = new_df.iloc[j, 1:] # Extraire une partie de la deuxième dataframe
                if df1_partie.equals(df2_partie): # Comparer les deux parties
                    return new_df.iloc[j, :] # Retourner la première partie similaire trouvée
        print("ZEBIIIIIIIiii")
        return None # Si aucune partie similaire n'a été trouvée, retourner None

    def export_df(self, ligne, colonne, joueur, status):
        df_temp = pd.DataFrame(self.coups, columns=["tour", "joueur", "ligne", "colonne", "win_by"])
        # Concaténer les deux DataFrames
        result_df = pd.concat([self.df, df_temp])
        result_df.to_csv("coups.csv", index=False, sep=';')

    # Remplir le fichier CSV avec les coups possibles
    def fill_possible_coup(self):
        for i in range(3):
            for j in range(3):
                new_row = pd.DataFrame({"ligne": [i], "colonne": [j], "value": [0]})
                self.possible_coups = pd.concat([self.possible_coups, new_row], ignore_index=True)
        self.possible_coups.to_csv("possible_coups.csv", index=False, sep=';')

    def est_gagne(self):
        df_temp = pd.DataFrame(self.coups, columns=["tour", "joueur", "ligne", "colonne", "win_by"])
        print(self.trouver_partie_similaire(df_temp, self.df))
        # Vérification des lignes
        for ligne in range(3):
            if self.grille[ligne][0] == self.grille[ligne][1] == self.grille[ligne][2] != " ":
                return True
        
        # Vérification des colonnes
        for colonne in range(3):
            if self.grille[0][colonne] == self.grille[1][colonne] == self.grille[2][colonne] != " ":
                return True
        print(self.grille)

        # Vérification des diagonales
        if self.grille[0][0] == self.grille[1][1] == self.grille[2][2] != " ":
            return True
        if self.grille[0][2] == self.grille[1][1] == self.grille[2][0] != " ":
            return True
        
        return False

    def est_plein(self):
        for ligne in range(3):
            for colonne in range(3):
                if self.grille[ligne][colonne] == " ":
                    return False
        return True

class Case(tk.Button):
    def __init__(self, master, ligne, colonne, morpion, cases):
        super().__init__(master, text=" ", font=("Arial", 24), width=7, height=4, command=self.cliquer)
        self.ligne = ligne
        self.colonne = colonne
        self.morpion = morpion
        self.cases = cases

    # Faire jouer l'IA
    def play_computer(self):
        ia = IA(self.morpion) # Initialisez l'IA ici
        ia.jouer()

        for i in range(3):
            for j in range(3):
                self.cases[i][j].configure(text=self.morpion.grille[i][j])
        
        if self.morpion.est_gagne():
            self.cases[self.ligne][self.colonne].configure(text=self.morpion.grille[self.ligne][self.colonne])
            self.morpion.export_df(self.ligne, self.colonne, "O", "won")
            messagebox.showinfo("Fin de partie", "Le joueur {} a gagné ! Clique sur replay pour rejouer".format(self.morpion.joueur_actuel))
        elif self.morpion.est_plein():
            messagebox.showinfo("Fin de partie", "Match nul !")
        else:
            self.cases[self.ligne][self.colonne].configure(text=self.morpion.grille[self.ligne][self.colonne])
            self.morpion.tour += 1

    # Méthode appelée lorsqu'un joueur clique sur une case
    def cliquer(self):
        self.morpion.joueur_actuel = "X"
        if self.morpion.grille[self.ligne][self.colonne] == " ":
            self.morpion.jouer(self.ligne, self.colonne)
            self.configure(text=self.morpion.grille[self.ligne][self.colonne])
            if self.morpion.est_gagne():
                messagebox.showinfo("Fin de partie", "Le joueur x a gagné ! Clique sur replay pour rejouer")
                print(self.morpion.coups)
            elif self.morpion.est_plein():
                messagebox.showinfo("Fin de partie", "Match nul !")
            else:
                self.morpion.joueur_actuel = "O"
                ia = IA(self.morpion)  # Initialisez l'IA ici
                self.play_computer()
                for i in range(3):
                    for j in range(3):
                        self.cases[i][j].configure(text=self.morpion.grille[i][j])
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")



class IA:
    # Constructeur
    def __init__(self, morpion):
        # Initialiser les attributs avec les informations du jeu
        self.morpion = morpion
        self.grille = morpion.grille
        self.joueur_actuel = morpion.joueur_actuel

    # Méthode pour évaluer un coup hypothétique
    def evaluer_grille(self, ligne, colonne, joueur):
        # Créer une copie de la grille et jouer le coup
        coup = (ligne, colonne)
        grille_copie = [row.copy() for row in self.grille]
        grille_copie[coup[0]][coup[1]] = joueur

        # Initialiser le score d'évaluation
        evaluation = 0

        # Vérifier les lignes et attribuer des points en fonction des critères d'évaluation
        for ligne in grille_copie:
            if ligne.count(joueur) == 2 and " " in ligne:
                evaluation += 10
            elif ligne.count(joueur) == 3:
                evaluation += 1000

        # Vérifier les colonnes et attribuer des points en fonction des critères d'évaluation
        for i in range(3):
            colonne = [grille_copie[j][i] for j in range(3)]
            if colonne.count(joueur) == 2 and " " in colonne:
                evaluation += 10
            elif colonne.count(joueur) == 3:
                evaluation += 1000

        # Vérifier les diagonales et attribuer des points en fonction des critères d'évaluation
        diagonale1 = [grille_copie[i][i] for i in range(3)]
        diagonale2 = [grille_copie[i][2 - i] for i in range(3)]

        if diagonale1.count(joueur) == 2 and " " in diagonale1:
            evaluation += 10
        elif diagonale1.count(joueur) == 3:
            evaluation += 1000
        if diagonale2.count(joueur) == 2 and " " in diagonale2:
            evaluation += 10
        elif diagonale2.count(joueur) == 3:
            evaluation += 1000

        # Attribuer des points pour un coup dans un coin ou au centre
        coins = [(0, 2), (0, 0), (2, 0), (2, 2)]
        centre = (1, 1)
        if coup in coins:
            evaluation += 5
        elif coup == centre:
            evaluation += 10

        # Retourner le score d'évaluation
        return evaluation

    def meilleur_coup(self):
        # Initialiser le meilleur score et le meilleur coup
        meilleur_score = -float("inf")
        meilleur_coup = None

        # Parcourir chaque case de la grille
        for ligne in range(3):
            for colonne in range(3):
                # Si la case est vide, évaluer le coup
                if self.morpion.grille[ligne][colonne] == " ":
                    score_coup = self.evaluer_grille(ligne, colonne, self.joueur_actuel)
                    score_adversaire = self.evaluer_grille(ligne, colonne, "X" if self.joueur_actuel == "O" else "O")

                    # Si l'IA a la possibilité de gagner, elle choisit ce coup
                    if score_coup >= 1000:
                        return (ligne, colonne)
                    # Sinon, si elle peut bloquer le joueur, elle le fait
                    elif score_adversaire >= 1000:
                        meilleur_score = score_adversaire
                        meilleur_coup = (ligne, colonne)
                    # Sinon, elle continue à chercher le meilleur coup
                    elif score_coup > meilleur_score:
                        meilleur_score = score_coup
                        meilleur_coup = (ligne, colonne)

        # Retourner le meilleur coup trouvé
        return meilleur_coup

    def jouer(self):
        # Trouver le meilleur coup
        meilleur_coup = self.meilleur_coup()

        # Si un meilleur coup est trouvé
        if meilleur_coup is not None:
            ligne, colonne = meilleur_coup
            self.morpion.grille[ligne][colonne] = self.morpion.joueur_actuel
            self.morpion.coups.append((self.morpion.tour, self.morpion.joueur_actuel, meilleur_coup[0], meilleur_coup[1], "O" if self.morpion.est_gagne() else "not_finished"))

        else:
            # Si aucun meilleur coup n'est trouvé, l'IA choisit un coup aléatoire
            ligne, colonne = random.choice(
                [(i, j) for i in range(3) for j in range(3) if self.morpion.grille[i][j] == " "])
            self.morpion.grille[ligne][colonne] = self.morpion.joueur_actuel
            self.morpion.coups.append((self.morpion.tour, self.morpion.joueur_actuel, ligne, colonne, "O" if self.morpion.est_gagne() else "not_finished"))


class Application(tk.Frame):
    # Constructeur
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.morpion = Morpion()
        self.cases = [[None, None, None], [None, None, None], [None, None, None]]
        self.replay = [None]
        self.creer_widgets()

    # Méthode pour réinitialiser le jeu
    def rejouer(self):
        self.morpion = Morpion()
        self.creer_widgets()
        self.replay.destroy()
        self.bouton_graphique.destroy()

    # Méthode pour créer les widgets (cases et boutons)
    def creer_widgets(self):
        for ligne in range(3):
            for colonne in range(3):
                case = Case(self, ligne, colonne, self.morpion, self.cases)
                case.grid(row=ligne, column=colonne)
                self.cases[ligne][colonne] = case
        self.replay = tk.Button(self.master, text="Rejouer", command=self.rejouer)
        self.replay.pack()
        self.bouton_graphique = tk.Button(self.master, text="Graphique", command=self.visualiser_graphique)
        self.bouton_graphique.pack()

    # Méthode pour compter les résultats à partir d'un fichier
    def counter_result(self, nom_fichier):
        victoires_x = 0
        victoires_o = 0
        egalites = 0

        with open(nom_fichier, 'r', newline='') as fichier:
            lecteur_csv = csv.reader(fichier, delimiter=';')
            next(lecteur_csv)  # Ignorer la première ligne d'en-tête

            for ligne in lecteur_csv:
                resultat = ligne[4]
                if resultat == 'X':
                    victoires_x += 1
                elif resultat == 'O':
                    victoires_o += 1
                elif resultat == 'draw':
                    egalites += 1

        return victoires_x, victoires_o, egalites

    # Méthode pour afficher un graphique des résultats
    def visualiser_graphique(self):
        nom_fichier = 'coups.csv'
        victoires_x, victoires_o, egalites = self.counter_result(nom_fichier)
        total_victoires = victoires_x + victoires_o + egalites
        x = ['X', 'O', 'Égalités']
        y = [victoires_x / total_victoires * 100, victoires_o / total_victoires * 100, egalites / total_victoires * 100]
        colors = ['red', 'blue', 'green']

        plt.bar(x, y, color=colors)
        plt.xlabel("Joueur")
        plt.ylabel("Pourcentage de victoires")
        plt.title("Comparaison des victoires entre X et O (en pourcentage)")
        plt.show()

# Fonction principale pour lancer l'application
def main():
    fenetre = tk.Tk()
    fenetre.title("Jeu de morpion")
    fenetre.geometry("900x600")
    jeu = Application(fenetre)
    jeu.pack()
    number_of_colors = 8

    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    print(color)
    fenetre.configure(background=color)
    image = tk.PhotoImage(file="maxime.png")
    label = tk.Label(image=image)
    label.image = image
    # Positionnement de l'image
    label.position = (0, 100)

    label.pack()


    fenetre.mainloop()


if __name__ == "__main__":
    main()