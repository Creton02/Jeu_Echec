import pygame


WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS


class Tableau():
    def __init__(self, liste_pieces:list):
        self.tableau = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        for Piece in liste_pieces:
            self.tableau[Piece.pos[0]][Piece.pos[1]] = Piece
    
    
    def roi_en_echec(self, tour_blanc):
        #Cette fonctoin vérifie si le roi est un échec, elle est utilisé pour la fonction d'echec et mat et de condition d'égalité
        couleur = "noir"
        if tour_blanc:
            couleur = "blanc"
        for e in range(len(self.tableau)):
            for i in range(len(self.tableau)):
                if self.tableau[e][i] != 0:
                    if self.tableau[e][i].couleur == couleur and self.tableau[e][i].is_king == True:
                        position_roi = (e, i)
                        break
        return(self.tableau[position_roi[0]][position_roi[1]].is_checked(self))

        

    def is_checkmate_or_stalemate(self, tour_blanc):
        #Cette fonction vérifie l'état de la partie, elle détecte si une couleur en particuler est en échec, ou en condition d'égalité
        is_checkmate = False
        is_stalemate = False
        couleur = "noir"
        if tour_blanc:
            couleur = "blanc"
        
        deplacements_possibles = 0
        
        for e in range(len(self.tableau)):
            for i in range(len(self.tableau)):
                if self.tableau[e][i] != 0:
                    if self.tableau[e][i].couleur == couleur:
                        deplacements_possibles += len(self.tableau[e][i].legal_moves_board(self))
        
        if deplacements_possibles == 0:
            print("CHECKMATE")
            if couleur == "noir":
                print(f"L'équipe blanche remporte la partie!")
            else:
                print(f"L'équipe noire remporte la partie!")
            is_checkmate = True
        
        if not self.roi_en_echec(tour_blanc):
            is_stalemate = True
        
        
        return is_checkmate, is_stalemate
        
    
    def deplacement(self, Piece:object, position_deplacement, tour_blanc):
        if (Piece.couleur == "blanc" and tour_blanc) or (Piece.couleur == "noir" and not tour_blanc):
            
            if self.tableau[position_deplacement[0]][position_deplacement[1]] != 0:
                
                if self.tableau[position_deplacement[0]][position_deplacement[1]].couleur != Piece.couleur and (position_deplacement[0], position_deplacement[1]) in Piece.legal_moves_board(self):
                    
                    #Déplacement de la tour dans le cas du rock
                    if Piece.is_king and abs(Piece.pos[1] - position_deplacement[1]) == 2:
                        #côté roi blanc
                        if position_deplacement[1] == 6 and Piece.couleur == "blanc":
                            self.tableau[7][5] = self.tableau[7][7]
                            self.tableau[7][7] = 0
                            self.tableau[7][5].pos = [7, 5]
                        #côté roi noir
                        elif position_deplacement[1] == 6 and Piece.couleur == "noir":
                            self.tableau[0][5] = self.tableau[0][7]
                            self.tableau[0][7] = 0
                            self.tableau[0][5].pos = [0, 5]
                        #côté reine blanc
                        elif position_deplacement[1] == 2 and Piece.couleur == "blanc":
                            self.tableau[7][3] = self.tableau[7][0]
                            self.tableau[7][0] = 0
                            self.tableau[7][3].pos = [7, 3]
                        #côté reine noir
                        elif position_deplacement[1] == 2 and Piece.couleur == "noir":
                            self.tableau[0][3] = self.tableau[0][0]
                            self.tableau[0][0] = 0
                    
                    self.tableau[position_deplacement[0]][position_deplacement[1]] = Piece
                    self.tableau[Piece.pos[0]][Piece.pos[1]] = 0
                    Piece.pos = [position_deplacement[0], position_deplacement[1]]
                    Piece.mouvements += 1
                    #Vérification de promotion
                    if Piece.is_pawn:
                        if Piece.couleur == "blanc" and Piece.pos[0] == 0:
                            self.tableau[position_deplacement[0]][position_deplacement[1]] = Reine(Piece.pos[0], Piece.pos[1], equipe=1)
                            print("PROMOTION")
                        elif Piece.pos[0] == 7:
                            self.tableau[position_deplacement[0]][position_deplacement[1]] = Reine(Piece.pos[0], Piece.pos[0])

                    return True
                else: 
                    return False
            elif (position_deplacement[0], position_deplacement[1]) in Piece.legal_moves_board(self):
                
                #Déplacement de la tour dans le cas du rock
                if Piece.is_king and abs(Piece.pos[1] - position_deplacement[1]) == 2:
                        #côté roi blanc
                        if position_deplacement[1] == 6 and Piece.couleur == "blanc":
                            self.tableau[7][5] = self.tableau[7][7]
                            self.tableau[7][7] = 0
                            self.tableau[7][5].pos = [7, 5]
                        #côté roi noir
                        elif position_deplacement[1] == 6 and Piece.couleur == "noir":
                            self.tableau[0][5] = self.tableau[0][7]
                            self.tableau[0][7] = 0
                            self.tableau[0][5].pos = [0, 5]
                        #côté reine blanc
                        elif position_deplacement[1] == 2 and Piece.couleur == "blanc":
                            self.tableau[7][3] = self.tableau[7][0]
                            self.tableau[7][0] = 0
                            self.tableau[7][3].pos = [7, 3]
                        #côté reine noir
                        elif position_deplacement[1] == 2 and Piece.couleur == "noir":
                            self.tableau[0][3] = self.tableau[0][0]
                            self.tableau[0][0] = 0
                            self.tableau[0][3].pos = [0, 3]
                            
                    
                self.tableau[position_deplacement[0]][position_deplacement[1]] = Piece
                self.tableau[Piece.pos[0]][Piece.pos[1]] = 0
                Piece.pos = [position_deplacement[0], position_deplacement[1]]
                Piece.mouvements += 1
                #Vérification de promotion

                if Piece.is_pawn:
                    if Piece.couleur == "blanc" and Piece.pos[0] == 0:
                        self.tableau[position_deplacement[0]][position_deplacement[1]] = Reine(Piece.pos[0], Piece.pos[1], equipe=1)
                        print("PROMOTION")
                    elif Piece.pos[0] == 7:
                        self.tableau[position_deplacement[0]][position_deplacement[1]] = Reine(Piece.pos[0], Piece.pos[0])
                        
                
                return True
    

            
class Piece(): 
    def __init__(self, x, y, equipe:int = 0, is_king:bool = False):
        #Initialisation des informations pour chaques pièce, il faut:
        #La position
        #La couleur
        #Le nombre de déplacements
        #L'emplacement du fichier pour l'Affichage
        self.pos = x, y
        self.is_king = is_king
        self.is_pawn = False
        if equipe == 0:
            self.couleur = "noir"
        else:
            self.couleur = "blanc"
        self.mouvements = 0
        try:
            original_image = pygame.image.load(self.get_image_path())
            self.image = pygame.transform.smoothscale(original_image, (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error:
            print(f"Une erreur est survenue lors de l'importation {self.get_image_path}")
            self.image = pygame.surface((SQUARE_SIZE, SQUARE_SIZE))
    

    def deplacement(self): #Fonction pour aider l'implémentation potentiel de nouvelles pièces
        raise NotImplementedError("Subclasses must implement deplacement()")
    
    
    def get_image_path(self): #Fonction pour aider l'implémentation potentiel de nouvelles pièces
        raise NotImplementedError("Subclasses must implement get_image_path()")
    
    
    def legal_moves(self, Tableau:object):
        #cette fonction est la fonction de base si elle n'a pas été codé dans une classe de pièce spécifique, elle regarde si les déplacements vont vers une case allié ou ennemie,
        #elle fait ensuite le tri
        can_go = self.deplacement()
        legal_moves:list = []
        for (x, y) in can_go:
            if Tableau.tableau[x][y] != 0:
                if Tableau.tableau[x][y].couleur == self.couleur:
                    pass
                else:
                    legal_moves.append((x, y))
            else:
                legal_moves.append((x, y))
        return legal_moves 
    
    
    def trouver_roi(self, Tableau:Tableau):
        #Cette fonction est très simple, elle trouve la position du roi et retourne seulement la position
        for e in range(len(Tableau.tableau)):
            for i in range(len(Tableau.tableau)):
                
                if Tableau.tableau[e][i] != 0:
                    
                    if Tableau.tableau[e][i].couleur == self.couleur and Tableau.tableau[e][i].is_king == True:
                        return((e, i))


    def legal_moves_board(self, Tableau:Tableau): 
        #La fonction la plus importante selon moi, elle regarde si le mouvement met son roi en echec.
        #liste de retour
        new_can_go = []
        #Position originale pour la simulation de mouvement
        position_originale = tuple(self.pos)

        #Test de tout les coups
        for x, y in self.legal_moves(Tableau):
            case_visee = (x, y)
            
            #Position de la piece sur la case visée pour la simulation de mouvement
            piece_sur_case = Tableau.tableau[case_visee[0]][case_visee[1]]
            
            #Regarder si la case est occupé par un allié
            if piece_sur_case != 0 and piece_sur_case.couleur == self.couleur:
                continue
            
            #Déplacement
            Tableau.tableau[case_visee[0]][case_visee[1]] = self
            Tableau.tableau[position_originale[0]][position_originale[1]] = 0
            self.pos = case_visee
            
            #Recherche du roi
            a, b = self.trouver_roi(Tableau)
            
            #Vérification de condition d'échec du roi
            if not Tableau.tableau[a][b].is_checked(Tableau):
                
                #Tri pour la nouvelle liste, seulement les coup qui ne mettent pas le roi en échec passent au triage
                new_can_go.append(case_visee)

            #Rétablissement du tableau à son état original
            self.pos = position_originale
            Tableau.tableau[position_originale[0]][position_originale[1]] = self
            Tableau.tableau[case_visee[0]][case_visee[1]] = piece_sur_case
             
        return new_can_go
                        
                    
                        
class Pion(Piece): 
    def __init__(self, x, y, equipe = 0, is_king = False):
        super().__init__(x, y, equipe, is_king)
        self.is_pawn = True

    
    def legal_moves(self, Tableau:Tableau):
        #Cette fonction retourne les mouvements pour le pion, il faut un cas pour le premier déplacement, un cas pour tous les autres déplacements, et un case pour la capture d'ennemie
        legal_moves = []
        x, y = self.pos
        direction = -1 if self.couleur == "blanc" else 1
        
        # Mouvement simple vers l'avant
        if Tableau.tableau[x + direction][y] == 0:
            legal_moves.append((x + direction, y))

            # Mouvement initial de 2 cases
            if self.mouvements == 0 and Tableau.tableau[x + 2 * direction][y] == 0:
                legal_moves.append((x + 2 * direction, y))

        # Capture diagonale
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            
            if 0 <= nx < 8 and 0 <= ny < 8:
                if Tableau.tableau[nx][ny] != 0 and Tableau.tableau[nx][ny].couleur != self.couleur:
                    legal_moves.append((nx, ny))

        return legal_moves
    

    def get_image_path(self):
        return "chess/pieces/white-pawn.png" if self.couleur == "blanc" else "chess/pieces/black-pawn.png"
    
    
    
class Tour(Piece):
    def legal_moves(self, Tableau):
        #Cette fonction analyse les trajectoires et retourne une liste de déplacement conforme aux règles des échecs
        x, y = self.pos
        legal_moves = []
        for i in range(4):
            limite = [False, False, False, False] #Cette liste de limite permet de déterminer lorsque la trajectoire est interrompu, pour chaques horizontales et verticales
            
            for e in range(1, 8):
                
                horizontals = [(e, 0), (-e, 0), (0, e), (0, -e)]
                
                if 0 <= (x + horizontals[i][0]) < 8 and 0 <= (y + horizontals[i][1]) < 8:
                    if limite[i] == False:
                        if Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]] == 0:
                            legal_moves.append((x + horizontals[i][0], y + horizontals[i][1]))
                            
                        else:
                            if Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]].couleur == self.couleur:
                                limite[i] = True
                                
                            elif Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]].couleur != self.couleur:
                                legal_moves.append((x + horizontals[i][0], y + horizontals[i][1]))
                                limite[i] = True
        return legal_moves
    
    
    def get_image_path(self):
        return "chess/pieces/white-rook.png" if self.couleur == "blanc" else "chess/pieces/black-rook.png"



class Cavalier(Piece):
    def deplacement(self): # Retourne une liste des déplacements possible
        can_go = []
        can_go.append((self.pos[0] + 2, self.pos[1] + 1))
        can_go.append((self.pos[0] + 2, self.pos[1] - 1))
        can_go.append((self.pos[0] - 2, self.pos[1] + 1))
        can_go.append((self.pos[0] - 2, self.pos[1] - 1))
        can_go.append((self.pos[0] + 1, self.pos[1] + 2))
        can_go.append((self.pos[0] + 1, self.pos[1] - 2))
        can_go.append((self.pos[0] - 1, self.pos[1] + 2))
        can_go.append((self.pos[0] - 1, self.pos[1] - 2))
        
        return [(x, y) for x, y in can_go if 0 <= x < 8 and 0 <= y < 8] # Pour ne pas dépasser le tableau
    
    
    def get_image_path(self):
        return "chess/pieces/white-knight.png" if self.couleur == "blanc" else "chess/pieces/black-knight.png"



class Reine(Piece):
    def legal_moves(self, Tableau):
        x, y = self.pos
        
        legal_moves = []
        for i in range(4):
            limite_h = [False, False, False, False]#Cette liste de limite permet de déterminer lorsque la trajectoire est interrompu, pour chaques horizontales et verticales
            limite_d = [False, False, False, False]#Cette liste de limite permet de déterminer lorsque la trajectoire est interrompu, pour chaques diagonales
            
            
            for e in range(1, 8):
                horizontals = [(e, 0), (-e, 0), (0, e), (0, -e)]
                diagonals = [(e, e), (-e, e), (e, -e), (-e, -e)]
                
                
                if 0 <= (x + horizontals[i][0]) < 8 and 0 <= (y + horizontals[i][1]) < 8:
                    
                    
                    if limite_h[i] == False:
                        
                        
                        if Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]] == 0:
                            legal_moves.append((x + horizontals[i][0], y + horizontals[i][1]))
                            
                            
                        else:
                            if Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]].couleur == self.couleur:
                                limite_h[i] = True
                                
                                
                            elif Tableau.tableau[x + horizontals[i][0]][y + horizontals[i][1]].couleur != self.couleur:
                                legal_moves.append((x + horizontals[i][0], y + horizontals[i][1]))
                                limite_h[i] = True
                                
                                
                if 0 <= (x + diagonals[i][0]) < 8 and 0 <= (y + diagonals[i][1]) < 8:
                    if limite_d[i] == False:
                        
                        if Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]] == 0:
                            legal_moves.append((x + diagonals[i][0], y + diagonals[i][1]))
                            
                        else:
                            if Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]].couleur == self.couleur:
                                limite_d[i] = True
                                
                            elif Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]].couleur != self.couleur:
                                legal_moves.append((x + diagonals[i][0], y + diagonals[i][1]))
                                limite_d[i] = True
                                
        return legal_moves
    
    
    def get_image_path(self):
        return "chess/pieces/white-queen.png" if self.couleur == "blanc" else "chess/pieces/black-queen.png"


  
class Fou(Piece):
    #Cette fonction donne les déplacements possibles pour les Fous,
    #il faut regarder la trajectoire et arrèter lorsque une case sur la trajectoire arrive sur une case allié ou ennemie
    def legal_moves(self, Tableau):
        x, y = self.pos
        legal_moves = []
        for i in range(4):
            limite = [False, False, False, False] #Cette liste de limite permet de déterminer lorsque la trajectoire est interrompu, pour chaque diagonale
            
            for e in range(1, 8):
                diagonals = [(e, e), (-e, e), (e, -e), (-e, -e)]
                
                if 0 <= (x + diagonals[i][0]) < 8 and 0 <= (y + diagonals[i][1]) < 8:
                    if limite[i] == False:
                        
                        if Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]] == 0:
                            legal_moves.append((x + diagonals[i][0], y + diagonals[i][1]))
                            
                        else:
                            if Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]].couleur == self.couleur:
                                limite[i] = True
                                
                            elif Tableau.tableau[x + diagonals[i][0]][y + diagonals[i][1]].couleur != self.couleur:
                                legal_moves.append((x + diagonals[i][0], y + diagonals[i][1]))
                                limite[i] = True
        return legal_moves
    
    
    def get_image_path(self):
        return "chess/pieces/white-bishop.png" if self.couleur == "blanc" else "chess/pieces/black-bishop.png"



class Roi(Piece):
    def deplacement(self): # Retourne la liste de tous les déplacements de base du roi
        can_go = []
        can_go.append((self.pos[0] + 1, self.pos[1] + 1))
        can_go.append((self.pos[0] - 1, self.pos[1] + 1))
        can_go.append((self.pos[0] + 1, self.pos[1] - 1))
        can_go.append((self.pos[0] - 1, self.pos[1] - 1))
        can_go.append((self.pos[0] + 1, self.pos[1]))
        can_go.append((self.pos[0] - 1, self.pos[1]))
        can_go.append((self.pos[0], self.pos[1] + 1))
        can_go.append((self.pos[0], self.pos[1] - 1))

        return [(x, y) for x, y in can_go if 0 <= x < 8 and 0 <= y < 8] # Pour ne pas les bornes du tableau
    
    
    def castle(self, Tableau=Tableau):
        #Cette fonction regarde si les cases entre le roi et sa tour sont vide, si elles le sont, elle retourne le déplacement qui permet le roque
        castle_can_go = []
        if self.mouvements == 0:
            if self.couleur == "blanc":
                
                #7, 5. 7, 6 vide, 7, 7 tour et deplacement = 0
                if Tableau.tableau[7][5] == 0 and Tableau.tableau[7][6] == 0 and Tableau.tableau[7][7].mouvements == 0:
                    castle_can_go.append((7, 6))
                    
                #7, 3. 7, 2 vide, 7, 1 tour et deplacement = 0
                if Tableau.tableau[7][3] == 0 and Tableau.tableau[7][2] == 0 and Tableau.tableau[7][1] == 0 and Tableau.tableau[7][0].mouvements == 0:
                    castle_can_go.append((7, 2))
                    
            if self.couleur == "noir":
                
                 #7, 5. 7, 6 vide, 7, 7 tour et deplacement = 0
                if Tableau.tableau[0][5] == 0 and Tableau.tableau[0][6] == 0 and Tableau.tableau[0][7].mouvements == 0:
                    castle_can_go.append((0, 6))
                    
                #7, 3. 7, 2 vide, 7, 1 tour et deplacement = 0
                if Tableau.tableau[0][3] == 0 and Tableau.tableau[0][2] == 0 and Tableau.tableau[0][1] == 0 and Tableau.tableau[0][0].mouvements == 0:
                    castle_can_go.append((0, 2))
                    
        return castle_can_go
    
    
    def is_checked(self, Tableau:Tableau):
        #Cette fonction analyse le tableau pour indiquer si le roi est en échec
        
        is_checked:bool = False
        
        for e in range(len(Tableau.tableau)):
            for i in range(len(Tableau.tableau[e])):
                
                case = Tableau.tableau[e][i]
                
                if case != 0:
                    
                    if case.is_king == True and case.couleur != self.couleur:
                        if self.pos in case.deplacement():
                            return True
                        
                    if case.is_king == True:
                        continue
                    
                    if case.couleur != self.couleur:
                        if self.pos in case.legal_moves(Tableau):
                            is_checked = True
                            
        return is_checked
    
    
    def legal_moves(self, Tableau:Tableau):
        #Cette fonction analyse le Tableau afin de déterminer si les mouvements possibles mettent le roi en échec
        #Elle fait une simulation d'un tour: effectue les déplacements et analyse la condition d'échec du roi, si elle est vrais, le déplacement est rejeté
        can_go = self.deplacement()
        if self.castle(Tableau) != None:
            
            for e in range(len(self.castle(Tableau))):
                can_go.append(self.castle(Tableau)[e])
    
        new_can_go = []
        
        position_originale = tuple(self.pos)
        for x, y in can_go:
            case_visee = (x, y)
            
            # Regarder si la case est occupé par un allié
            piece_sur_case = Tableau.tableau[case_visee[0]][case_visee[1]]
            if piece_sur_case != 0 and piece_sur_case.couleur == self.couleur:
                continue
            
            Tableau.tableau[case_visee[0]][case_visee[1]] = self
            Tableau.tableau[position_originale[0]][position_originale[1]] = 0
            self.pos = case_visee
        
            
            if not self.is_checked(Tableau):
                new_can_go.append(case_visee)
            
            self.pos = position_originale
            Tableau.tableau[position_originale[0]][position_originale[1]] = self
            Tableau.tableau[case_visee[0]][case_visee[1]] = piece_sur_case

            
        return new_can_go


    def get_image_path(self):
        return "chess/pieces/white-king.png" if self.couleur == "blanc" else "chess/pieces/black-king.png"