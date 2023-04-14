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

    def jouer(self, ligne, colonne):
        print(self.evaluer_coup(ligne, colonne))
        self.joueur_actuel = "X"
        joueur = "X"

        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = joueur
            if os.path.exists("coups.csv"):
                self.df = pd.read_csv("coups.csv", sep=';')
            else :
                self.df = pd.DataFrame(columns=["tour", "joueur", "ligne", "colonne", "win_by"])
            # Charger le fichier CSV existant s'il existe, sinon créer un nouveau DataFrame
            if self.est_gagne() == False and self.est_plein() == False:
                self.coups.append((self.tour, joueur, ligne, colonne, "X" if self.est_gagne() else "not_finished"))
            if (self.est_gagne() == True):
                self.export_df(ligne, colonne, joueur,"won")
            # exporter le df dans le cas d'une égalité
            if (self.tour == 8 and self.est_gagne() == False and self.est_plein() == True):
                self.coups.append((self.tour, "X", ligne, colonne, "draw"))
                self.export_df(ligne, colonne, joueur, "draw")
            self.tour += 1
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")

    def export_df(self, ligne, colonne, joueur, status):
        if status != "draw":
            self.coups.append((self.tour, joueur, ligne, colonne, joueur))
        df_temp = pd.DataFrame(self.coups, columns=["tour", "joueur", "ligne", "colonne", "win_by"])
        #concat the two dataframes
        result_df = pd.concat([self.df, df_temp])
        result_df.to_csv("coups.csv", index=False, sep=';')

    def fill_possible_coup(self):
        for i in range(3):
            for j in range(3):
                new_row = pd.DataFrame({"ligne": [i], "colonne": [j], "value": [0]})
                self.possible_coups = pd.concat([self.possible_coups, new_row], ignore_index=True)
        self.possible_coups.to_csv("possible_coups.csv", index=False, sep=';')

    def est_gagne(self):
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
    
    def evaluer_coup(self, ligne, colonne):
        coup = (ligne, colonne)
        # Copier la grille pour éviter de la modifier directement
        grille_copie = [row.copy() for row in self.grille]

        # Appliquer le coup dans la grille
        grille_copie[coup[0]][coup[1]] = self.joueur_actuel

        # Évaluer le coup pour le joueur donné
        evaluation = 0

        # Vérifier les lignes
        for ligne in grille_copie:
            if ligne.count(self.joueur_actuel) == 3:
                evaluation += 100

        # Vérifier les colonnes
        for i in range(3):
            colonne = [grille_copie[j][i] for j in range(3)]
            if colonne.count(self.joueur_actuel) == 3:
                evaluation += 100

        # Vérifier les diagonales
        diagonale1 = [grille_copie[i][i] for i in range(3)]
        diagonale2 = [grille_copie[i][2-i] for i in range(3)]
        if diagonale1.count(self.joueur_actuel) == 3 or diagonale2.count(self.joueur_actuel) == 3:
            evaluation += 100

        # Ajouter des points pour un coup dans un coin ou au centre
        coins = [(0, 0), (0, 2), (2, 0), (2, 2)]
        centre = (1, 1)
        if coup in coins:
            evaluation += 25
        elif coup == centre:
            evaluation += 50

        return evaluation

    
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
            
            
    def play_computer(self):
        ia = IA(self.morpion)
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
            self.morpion.coups.append((self.morpion.tour, self.morpion.joueur_actuel, self.ligne, self.colonne, "O" if self.morpion.est_gagne() else "not_finished"))
            self.morpion.tour += 1



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
    def __init__(self, morpion):
        self.morpion = morpion
        self.grille = morpion.grille
        self.joueur_actuel = morpion.joueur_actuel

    def evaluer_grille(self, ligne, colonne, joueur):
        coup = (ligne, colonne)
        grille_copie = [row.copy() for row in self.grille]
        grille_copie[coup[0]][coup[1]] = joueur

        evaluation = 0

        # Vérifier les lignes
        for ligne in grille_copie:
            if ligne.count(joueur) == 2 and " " in ligne:
                evaluation += 100

        # Vérifier les colonnes
        for i in range(3):
            colonne = [grille_copie[j][i] for j in range(3)]
            if colonne.count(joueur) == 2 and " " in colonne:
                evaluation += 100

        # Vérifier les diagonales
        diagonale1 = [grille_copie[i][i] for i in range(3)]
        diagonale2 = [grille_copie[i][2 - i] for i in range(3)]

        if diagonale1.count(joueur) == 2 and " " in diagonale1:
            evaluation += 100
        if diagonale2.count(joueur) == 2 and " " in diagonale2:
            evaluation += 100

        # Ajouter des points pour un coup dans un coin ou au centre
        coins = [(0, 0), (0, 2), (2, 0), (2, 2)]
        centre = (1, 1)
        if coup in coins:
            evaluation += 25
        elif coup == centre:
            evaluation += 50

        return evaluation

    def meilleur_coup(self):
        meilleur_score = -float("inf")
        meilleur_coup = None

        for ligne in range(3):
            for colonne in range(3):
                if self.morpion.grille[ligne][colonne] == " ":
                    score_coup = self.evaluer_grille(ligne, colonne, self.joueur_actuel)
                    score_adversaire = self.evaluer_grille(ligne, colonne, "X" if self.joueur_actuel == "O" else "O")

                    # Si l'IA a la possibilité de gagner, elle choisit ce coup
                    if score_coup >= 100:
                        return (ligne, colonne)
                    # Sinon, si elle peut bloquer le joueur, elle le fait
                    elif score_adversaire >= 100:
                        meilleur_score = score_adversaire
                        meilleur_coup = (ligne, colonne)
                    # Sinon, elle continue à chercher le meilleur coup
                    elif score_coup > meilleur_score:
                        meilleur_score = score_coup
                        meilleur_coup = (ligne, colonne)

        return meilleur_coup

    def jouer(self):
        meilleur_coup = self.meilleur_coup()

        if meilleur_coup is not None:
            ligne, colonne = meilleur_coup
            self.morpion.grille[ligne][colonne] = self.morpion.joueur_actuel
        else:
            # Si aucun meilleur coup n'est trouvé, l'IA choisit un coup aléatoire
            ligne, colonne = random.choice(
                [(i, j) for i in range(3) for j in range(3) if self.morpion.grille[i][j] == " "])
            self.morpion.grille[ligne][colonne] = self.morpion.joueur_actuel


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.morpion = Morpion()
        self.cases = [[None, None, None], [None, None, None], [None, None, None]]
        self.replay = [None]
        self.creer_widgets()

    def rejouer(self):
        self.morpion = Morpion()
        self.creer_widgets()
        self.replay.destroy()

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

    def visualiser_graphique(self):
        nom_fichier = 'coups.csv'
        victoires_x, victoires_o, egalites = self.counter_result(nom_fichier)
        x = ['X', 'O', 'Égalités']  # Ajout de 'Égalités' dans la liste x
        y = [victoires_x, victoires_o, egalites]  # Ajout de egalites dans la liste y
        colors = ['red', 'blue', 'green']  # Ajout de 'green' dans la liste colors

        plt.bar(x, y, color=colors)
        plt.xlabel("Joueur")
        plt.ylabel("Nombre de victoires")
        plt.title("Comparaison des victoires entre X et O")
        plt.show()



def main():
    fenetre = tk.Tk()
    fenetre.title("Jeu de morpion")
    fenetre.geometry("900x600")
    jeu = Application(fenetre)
    jeu.pack()
    fenetre.mainloop()


if __name__ == "__main__":
    main()
