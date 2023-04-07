import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import os

class Morpion:
    def __init__(self):
        self.grille = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def jouer(self, ligne, colonne):
        self.joueur_actuel = "X"
        if self.joueur_actuel == "X":
            joueur = "X"
            self.joueur_actuel = "O"
        else:
            joueur = "O"
            self.joueur_actuel = "X"
            
        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = joueur
            # Charger le fichier CSV existant s'il existe, sinon créer un nouveau DataFrame
            if os.path.exists("coups.csv"):
                df = pd.read_csv("coups.csv")
            else:
                df = pd.DataFrame(columns=["joueur", "ligne", "colonne"])
            # Ajouter les coordonnées du coup joué au DataFrame
            # Exporter le DataFrame dans le fichier CSV
            df.to_csv("coups.csv", index=False)
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
        self.cases[ligne][colonne].configure(text=self.morpion.grille[ligne][colonne])
        

    def cliquer(self):
        self.morpion.joueur_actuel = "X"
        if self.morpion.grille[self.ligne][self.colonne] == " ":
            self.morpion.jouer(self.ligne, self.colonne)
            self.configure(text=self.morpion.grille[self.ligne][self.colonne])
            if self.morpion.est_gagne():
                messagebox.showinfo("Fin de partie", "Le joueur x a gagné ! Clique sur replay pour rejouer")
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


if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("Jeu de morpion")
    fenetre.geometry("900x600")
    jeu = Application(fenetre)
    jeu.pack()
    fenetre.mainloop()

# print(Morpion().grille)