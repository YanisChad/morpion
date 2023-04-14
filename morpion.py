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
        if self.joueur_actuel == "X":
            joueur = "X"
            self.joueur_actuel = "O"
        else:
            joueur = "O"
            self.joueur_actuel = "X"
            
        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = joueur
            if os.path.exists("coups.csv"):
                df = pd.read_csv("coups.csv", sep=';')
            else :
                df = pd.DataFrame(columns=["tour", "joueur", "ligne", "colonne"])
            # Charger le fichier CSV existant s'il existe, sinon créer un nouveau DataFrame
            self.coups.append((self.tour, joueur, ligne, colonne))
            
            # Ajouter les coordonnées du coup joué au DataFrame
            # Exporter le DataFrame dans le fichier CSV
            df_temp = pd.DataFrame(self.coups, columns=["tour", "joueur", "ligne", "colonne"])
            #concat the two dataframes
            result_df = pd.concat([df, df_temp])
            result_df.to_csv("coups.csv", index=False, sep=';')
            self.tour += 1
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")
        
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
        self.morpion.joueur_actuel = "O"
        while True:
            ligne = random.randint(0, 2)
            colonne = random.randint(0, 2)
            if self.morpion.grille[ligne][colonne] == " ":
                break
        self.morpion.grille[ligne][colonne] = self.morpion.joueur_actuel
        if self.morpion.est_gagne():
            self.cases[ligne][colonne].configure(text=self.morpion.grille[ligne][colonne])
            messagebox.showinfo("Fin de partie", "Le joueur {} a gagné ! Clique sur replay pour rejouer".format(self.morpion.joueur_actuel))
        elif self.morpion.est_plein():
            self.cases[ligne][colonne].configure(text=self.morpion.grille[ligne][colonne])
            messagebox.showinfo("Fin de partie", "Match nul !")
        else:
            self.cases[ligne][colonne].configure(text=self.morpion.grille[ligne][colonne])
            self.morpion.coups.append((self.morpion.tour, self.morpion.joueur_actuel, ligne, colonne))
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
            else :
                self.play_computer()
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")

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



if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("Jeu de morpion")
    fenetre.geometry("900x600")
    jeu = Application(fenetre)
    jeu.pack()
    fenetre.mainloop()