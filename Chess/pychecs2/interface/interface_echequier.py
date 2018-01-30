
from tkinter import Tk, Canvas, Label, NSEW ,Frame, Button, StringVar, ttk , filedialog,  N, W, LabelFrame, NW
import pickle
import webbrowser
import os
from pychecs2.echecs.partie import Partie
from pychecs2.echecs.piece import Roi, Pion, Cavalier, Dame, Tour, Fou


class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case, partie):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8
        self.partie = partie

        self.couleur_1 = 'white'
        self.couleur_2 = 'grey'

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)



        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)


    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.

        """
        self.delete('case')


        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = self.couleur_1
                else:
                    couleur = self.couleur_2

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

    def dessiner_pieces(self):
        self.delete('piece')


        # Pour tout paire position, pièce:
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.partie.echiquier.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.partie.echiquier.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text=(piece),
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.dessiner_pieces()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Échiquier")

        # Creation d'une nouvelle partie
        self.partie = Partie()
        self.sauvegarder("Revenir")



        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie)
        self.canvas_echiquier.grid(sticky=NSEW)

        # Frame bouton Sauvegare/NG/coup précédent
        self.frame_sauvegarde = Frame(self)
        self.frame_sauvegarde.grid(row =1)

        # label invisible
        self.label_invisible1 = Label(self.frame_sauvegarde)
        self.label_invisible1.grid(row=0)

        # Creation d'un bouton nouvelle partie
        self.boutton_nouvelle_partie = Button(self.frame_sauvegarde, text = 'Nouvelle Partie', command=self.nouvelle_partie)
        self.boutton_nouvelle_partie.grid()

        # label invisible
        self.label_invisible2 = Label(self.frame_sauvegarde)
        self.label_invisible2.grid(row=1, column=2)

        # Creation d'un bouton précédant
        self.boutton_revenir = Button(self.frame_sauvegarde, text='Coup précédant', command=self.revenir)
        self.boutton_revenir.grid(row=1, column=3)

        # label invisible
        self.label_invisible2 = Label(self.frame_sauvegarde)
        self.label_invisible2.grid(row=1, column=4)

        # Sauvegarder
        self.boutton_sauvegarde = Button(self.frame_sauvegarde, text='Sauvegarder', command=self.faire_sauvegarder)
        self.boutton_sauvegarde.grid(row=1, column=5)

        # label invisible
        self.label_invisible2 = Label(self.frame_sauvegarde)
        self.label_invisible2.grid(row=1, column=6)

        # Charger
        self.bouton_charger = Button(self.frame_sauvegarde, text='     Charger     ', command=self.faire_charger)
        self.bouton_charger.grid(row=1, column=7)

        # Frame joueur actif
        self.frame_info = LabelFrame(self, text="Joueur actif")
        self.frame_info.grid(row=0, column=1, sticky=NW)

        self.label_temporaire = Label(self.frame_info, text="C'est le tour au joueur "+self.partie.joueur_actif, background='snow')
        self.label_temporaire.grid(row=0, sticky=N, column=0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=1,column=0, padx=100)

        # label theme
        self.label_theme = Label(self.frame_info, text="Thème:")
        self.label_theme.grid(row=2, sticky=W)

        # Changer de thème
        self.valeur = StringVar()
        self.boite_theme = ttk.Combobox(self.frame_info,textvariable=self.valeur, state="readonly")
        self.boite_theme["values"] = ["Classique", "Noel", "Saint-Valentin", "Doritos-MountainDew"]
        self.boite_theme.current(0)
        self.boite_theme.grid(row=3)
        self.boite_theme.bind("<<ComboboxSelected>>", self.changer_theme)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=4,column=0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=5,column=0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=6,column=0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=7,column=0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=8,column=0)

        # bouton Reglement
        self.bouton_reglement = Button(self.frame_info, text='Règlements', command=self.montre_reglement)
        self.bouton_reglement.grid(row = 9, column = 0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=10,column=0)

        # bouton Troll
        self.bouton_troll = Button(self.frame_info, text='Ne pas cliquer :)',background = 'red', command=self.troll)
        self.bouton_troll.grid(row = 11, column = 0)

        # label invisible
        self.label_invisible = Label(self.frame_info)
        self.label_invisible.grid(row=12,column=0,pady =58)

        # label note
        self.label_note = Label(self.frame_info,text='*Note:', background = 'yellow')
        self.label_note.grid(row=13,column=0,sticky=NW)
        self.label_clic1 = Label(self.frame_info,text='Clique gauche = Sélectionner pièce')
        self.label_clic1.grid(row=14,column=0,sticky=NW)
        self.label_clic2 = Label(self.frame_info,text='Clique droit = Déposer pièce')
        self.label_clic2.grid(row=15,column=0,sticky=NW)


        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()


        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)
        self.canvas_echiquier.bind('<Button-3>', self.deposer)

    def faire_sauvegarder(self):
        try:
            self.sauvegarder(filedialog.asksaveasfilename(initialdir=os.path.join(os.path.realpath(os.path.curdir), 'Sauvegarde')))

        except FileNotFoundError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = "La partie n'a pas été sauvegardée"
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()


    def faire_charger(self):
        try:
            self.charger(filedialog.askopenfilename(initialdir=os.path.join(os.path.realpath(os.path.curdir), 'Sauvegarde')))
        except FileNotFoundError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Aucune partie n'a été chargée"
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()


    def sauvegarder(self, nom_fichier):

            with open(nom_fichier, 'wb') as partie:
                a = self.partie.echiquier.dictionnaire_pieces
                b = self.partie.joueur_actif

                pickle.dump(a, partie)
                pickle.dump(b, partie)



            partie.close()


    def charger(self, nom_fichier):


        with open(nom_fichier, 'rb') as partie:
            a = pickle.load(partie)
            b = pickle.load(partie)
            self.partie.echiquier.dictionnaire_pieces = a
            self.partie.joueur_actif = b


        partie.close()


        self.messages['text'] = ''
        self.canvas_echiquier.dessiner_cases()
        self.canvas_echiquier.dessiner_pieces()
        self.label_temporaire['text'] ="C'est le tour au joueur "+self.partie.joueur_actif

    class MauvaiseCouleur(Exception):
        pass

    class DeplacementInvalide(Exception):
        pass

    def selectionner(self, event):

        toutes_les_position = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'
                               , 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'
                               , 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'
                               , 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'
                               , 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'
                               , 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'
                               , 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'
                               , 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']

        if self.partie.partie_terminee() == False:

            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne = event.y // self.canvas_echiquier.n_pixels_par_case
            colonne = event.x // self.canvas_echiquier.n_pixels_par_case
            position_source = "{}{}".format(self.canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.partie.echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))
            liste_lettre_a_chiffre = {'a': 0,'b': 1, 'c': 2, 'd': 3, 'e': 4 ,'f': 5 ,'g': 6 ,'h': 7 }
            couleur_joueur_actif = self.partie.joueur_actif
            couleur_piece_selectionnée = self.partie.echiquier.couleur_piece_a_position(position_source)


            try:

                self.canvas_echiquier.dessiner_cases()
                self.canvas_echiquier.dessiner_pieces()
                piece = self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position_source]

                # On change la valeur de l'attribut position_selectionnee.
                self.position_selectionnee = position_source
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)
                self.canvas_echiquier.grid()


                if self.position_selectionnee is not None:
                    self.canvas_echiquier.create_rectangle(liste_lettre_a_chiffre[position_source[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case - int(position_source[1]) * self.canvas_echiquier.n_pixels_par_case, self.canvas_echiquier.n_pixels_par_case + liste_lettre_a_chiffre[position_source[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case -int(position_source[1]) * self.canvas_echiquier.n_pixels_par_case + self.canvas_echiquier.n_pixels_par_case, fill='yellow', tags='case')

                    for i in toutes_les_position:
                        if self.partie.echiquier.deplacement_est_valide(position_source,i):
                            self.canvas_echiquier.create_rectangle(liste_lettre_a_chiffre[i[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case - int(i[1]) * self.canvas_echiquier.n_pixels_par_case, self.canvas_echiquier.n_pixels_par_case + liste_lettre_a_chiffre[i[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case -int(i[1]) * self.canvas_echiquier.n_pixels_par_case + self.canvas_echiquier.n_pixels_par_case, fill='cyan', tags='case')
                            if self.partie.echiquier.recuperer_piece_a_position(i) is not None:
                                self.canvas_echiquier.create_rectangle(liste_lettre_a_chiffre[i[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case - int(i[1]) * self.canvas_echiquier.n_pixels_par_case, self.canvas_echiquier.n_pixels_par_case + liste_lettre_a_chiffre[i[0]] * self.canvas_echiquier.n_pixels_par_case, 8*self.canvas_echiquier.n_pixels_par_case -int(i[1]) * self.canvas_echiquier.n_pixels_par_case + self.canvas_echiquier.n_pixels_par_case, fill='red', tags='case')
                    self.canvas_echiquier.dessiner_pieces()
                if couleur_joueur_actif != couleur_piece_selectionnée:
                    raise self.MauvaiseCouleur





            except self.MauvaiseCouleur:
                self.messages['foreground'] = 'red'
                self.messages['text'] = "Erreur: Cette pièce n'est pas la votre"
                self.canvas_echiquier.dessiner_cases()
                self.canvas_echiquier.dessiner_pieces()

            except KeyError:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
                self.canvas_echiquier.dessiner_cases()
                self.canvas_echiquier.dessiner_pieces()


    def deposer(self, event):


        toutes_les_position = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'
                               , 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'
                               , 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'
                               , 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'
                               , 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'
                               , 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'
                               , 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'
                               , 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']


        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        global position_cible
        position_cible = "{}{}".format(self.canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.partie.echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))

        if self.partie.echiquier.deplacement_est_valide(self.position_selectionnee, position_cible) == True:
            self.sauvegarder("Revenir")

        try:
            var = 1
            if self.partie.echiquier.couleur_piece_a_position(self.position_selectionnee) == self.partie.joueur_actif:
                if self.partie.echiquier.deplacer(self.position_selectionnee, position_cible) == True:
                    self.partie.echiquier.deplacer(self.position_selectionnee, position_cible)
                    var = 0
                    if isinstance(self.partie.echiquier.recuperer_piece_a_position(position_cible), Pion) == True:
                        if self.partie.echiquier.couleur_piece_a_position(position_cible) == 'blanc':
                            if position_cible[1] == '8':
                                self.partie.echiquier.dictionnaire_pieces[position_cible] = Dame('blanc')
                                self.canvas_echiquier.dessiner_cases()
                                self.canvas_echiquier.dessiner_pieces()
                        elif self.partie.echiquier.couleur_piece_a_position(position_cible) == 'noir':
                            if position_cible[1] == '1':
                                self.partie.echiquier.dictionnaire_pieces[position_cible] = Dame('noir')
                                self.canvas_echiquier.dessiner_cases()
                                self.canvas_echiquier.dessiner_pieces()


                    self.canvas_echiquier.dessiner_cases()
                    self.canvas_echiquier.dessiner_pieces()
                    self.partie.partie_terminee()
                    for i in toutes_les_position:
                        if self.partie.echiquier.deplacement_est_valide(position_cible,i) and isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Roi) == True:
                            self.partie.joueur_suivant()
                            self.messages['foreground'] = 'red'
                            self.messages['text'] = 'Le Roi '+self.partie.joueur_actif+' est en échec'
                            self.partie.joueur_suivant()
                            self.canvas_echiquier.dessiner_cases()
                            self.canvas_echiquier.dessiner_pieces()


                        if isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Pion) == True or isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Tour) == True or isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Fou)==True or isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Cavalier) == True or isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Dame) == True:
                            var = 1



                    self.partie.joueur_suivant()
                    self.label_temporaire['text'] ="C'est le tour au joueur "+self.partie.joueur_actif



                else:
                    raise self.DeplacementInvalide

        except self.DeplacementInvalide:
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'Erreur: Deplacement invalide'
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()


        if self.partie.partie_terminee() == True:
            for i in toutes_les_position:
                if isinstance(self.partie.echiquier.recuperer_piece_a_position(i), Roi) == True:
                    couleur = self.partie.echiquier.couleur_piece_a_position(i)
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'La partie est terminer.'
            self.label_temporaire['text'] = 'Félicitation joueur '+couleur
            if var == 0:
                self.label_temporaire['text'] =  'Partie nulle de type pat'
                var2 = 1
                self.canvas_echiquier.dessiner_cases()
                self.canvas_echiquier.dessiner_pieces()

            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()

    def nouvelle_partie(self):

        self.charger("Nouvelle_partie")
        self.label_temporaire['text'] ="C'est le tour au joueur "+self.partie.joueur_actif

    def revenir(self):
        self.charger("Revenir")
        self.label_temporaire['text'] ="C'est le tour au joueur "+self.partie.joueur_actif


    def changer_theme(self, event):
        if self.valeur.get() == 'Noel':
            self.canvas_echiquier.couleur_1 = 'red3'
            self.canvas_echiquier.couleur_2 = 'chartreuse4'
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()

        elif self.valeur.get() == 'Saint-Valentin':
            self.canvas_echiquier.couleur_1 = 'magenta'
            self.canvas_echiquier.couleur_2 = 'pink'
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()

        elif self.valeur.get() == 'Doritos-MountainDew':
            self.canvas_echiquier.couleur_1 = 'dark orange'
            self.canvas_echiquier.couleur_2 = 'chartreuse'
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()

        else:
            self.canvas_echiquier.couleur_1 = 'white'
            self.canvas_echiquier.couleur_2 = 'grey'
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.dessiner_pieces()

    def montre_reglement(self):

        webbrowser.open_new("https://fr.wikipedia.org/wiki/R%C3%A8gles_du_jeu_d'%C3%A9checs")

    def troll(self):

        webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.bouton_troll['text'] = 'On vous avait prévenu'