import tkinter as tk
from tkinter import messagebox
import random

class Morpion:
    def __init__(self):
        self.joueur_actuel = "X"
        self.grille = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        
    def jouer(self, ligne, colonne):
        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = self.joueur_actuel
            if self.joueur_actuel == "X":
                self.joueur_actuel = "O"
            else:
                self.joueur_actuel = "X"
        else:
            messagebox.showwarning("Erreur", "Case déjà occupée")

            
    def est_gagne(self):
        # Vérification des lignes
        for ligne in range(3):
            if self.grille[ligne][0] == self.grille[ligne][1] == self.grille[ligne][2] != " ":
                return True
        
        # Vérification des colonnes
        for colonne in range(3):
            print(self.grille)
            if self.grille[0][colonne] == self.grille[1][colonne] == self.grille[2][colonne] != " ":
                return True
        
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
    def __init__(self, master, ligne, colonne, morpion):
        super().__init__(master, text=" ", font=("Arial", 24), width=7, height=4, command=self.cliquer)
        self.ligne = ligne
        self.colonne = colonne
        self.morpion = morpion
        
    def cliquer(self):
        self.morpion.jouer(self.ligne, self.colonne)
        self.configure(text=self.morpion.grille[self.ligne][self.colonne])
        if self.morpion.est_gagne():
            if self.morpion.joueur_actuel == "X":
                self.morpion.joueur_actuel = "O"
            else:
                self.morpion.joueur_actuel = "O"
                self.morpion.joueur_actuel = "X"
            messagebox.showinfo("Fin de partie", "Le joueur {} a gagné ! Clique sur replay pour rejouer".format(self.morpion.joueur_actuel))

        elif self.morpion.est_plein():
            messagebox.showinfo("Fin de partie", "Match nul !")
            

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
                case = Case(self, ligne, colonne, self.morpion)
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

print(Morpion().grille)
