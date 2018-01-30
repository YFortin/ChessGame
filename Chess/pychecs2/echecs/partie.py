# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""
from pychecs2.echecs.echiquier import Echiquier, Pion, Cavalier, Dame, Tour, Fou


class Partie:
    """La classe Partie contient les informations sur une partie d'échecs, c'est à dire un échiquier, puis
    un joueur actif (blanc ou noir). Des méthodes sont disponibles pour faire avancer la partie et interagir
    avec l'utilisateur.

    Attributes:
        joueur_actif (str): La couleur du joueur actif, 'blanc' ou 'noir'.
        echiquier (Echiquier): L'échiquier sur lequel se déroule la partie.

    """
    def __init__(self):
        # Le joueur débutant une partie d'échecs est le joueur blanc.
        self.joueur_actif = 'blanc'

        # Création d'une instance de la classe Echiquier, qui sera manipulée dans les méthodes de la classe.
        self.echiquier = Echiquier()

    def determiner_gagnant(self):
        """Détermine la couleur du joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        le roi de la couleur adverse doit être absente de l'échiquier.

        Returns:
            str: 'blanc' si le joueur blanc a gagné, 'noir' si c'est plutôt le joueur noir, et 'aucun' si aucun
                joueur n'a encore gagné.

        """


        if not self.echiquier.roi_de_couleur_est_dans_echiquier('noir'):
            return 'blanc'
        elif not self.echiquier.roi_de_couleur_est_dans_echiquier('blanc'):
            return 'noir'

        return 'aucun'

    def partie_terminee(self):
        """Vérifie si la partie est terminée. Une partie est terminée si un gagnant peut être déclaré.

        Returns:
            bool: True si la partie est terminée, et False autrement.

        """
        toutes_les_position = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'
                               , 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'
                               , 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'
                               , 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'
                               , 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'
                               , 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'
                               , 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'
                               , 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']
        var = 0
        for i in toutes_les_position:
            if isinstance(self.echiquier.recuperer_piece_a_position(i), Pion) == True or isinstance(self.echiquier.recuperer_piece_a_position(i), Tour) == True or isinstance(self.echiquier.recuperer_piece_a_position(i), Fou)==True or isinstance(self.echiquier.recuperer_piece_a_position(i), Cavalier) == True or isinstance(self.echiquier.recuperer_piece_a_position(i), Dame) == True:
                var = 1
        if var == 0:
            return True
        else:
            return self.determiner_gagnant() != 'aucun'

    def demander_positions(self):
        """Demande à l'utilisateur d'entrer les positions de départ et d'arrivée pour faire un déplacement. Si les
        positions entrées sont valides (si le déplacement est valide), on retourne les deux positions. On doit
        redemander tant que l'utilisateur ne donne pas des positions valides.

        Returns:
            str, str: Deux chaînes de caractères représentant les deux positions valides fournies par l'utilisateurs.

        """
        while True:
            # On demande et valide la position source.
            while True:
                source = input("Entrez position source: ")
                if self.echiquier.position_est_valide(source) and self.echiquier.couleur_piece_a_position(source) == self.joueur_actif:
                    break

                print("Position invalide.\n")

            # On demande et valide la position cible.
            cible = input("Entrez position cible: ")
            if self.echiquier.deplacement_est_valide(source, cible):
                return source, cible

            print("Déplacement invalide.\n")

    def joueur_suivant(self):
        """Change le joueur actif: passe de blanc à noir, ou de noir à blanc, selon la couleur du joueur actif.

        """
        if self.joueur_actif == 'blanc':
            self.joueur_actif = 'noir'
        else:
            self.joueur_actif = 'blanc'

    def jouer(self):
        """Tant que la partie n'est pas terminée, joue la partie. À chaque tour :
            - On affiche l'échiquier.
            - On demande les deux positions.
            - On fait le déplacement sur l'échiquier.
            - On passe au joueur suivant.

        Une fois la partie terminée, on félicite le joueur gagnant!

        """
        while not self.partie_terminee():
            print(self.echiquier)
            print("\nAu tour du joueur {}".format(self.joueur_actif))
            source, cible = self.demander_positions()
            self.echiquier.deplacer(source, cible)
            self.joueur_suivant()

        print(self.echiquier)
        print("\nPartie terminée! Le joueur {} a gagné".format(self.determiner_gagnant()))
