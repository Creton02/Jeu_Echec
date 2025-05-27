import pygame
import sys
from pieces import Pion, Tour, Tableau, Cavalier, Reine, Roi, Fou, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE
pygame.init()

#Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 128, 50)
SURLIGNAGE = (0, 255, 0)
SURLIGNAGE2 = (255, 0, 0)
SURLIGNAGE3 = (155, 155, 255)

#Écran
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess")

#Préparation du tableau de jeu
liste_pieces = []

#Initialisation équipe noir
for e in range(8):
    liste_pieces.append(Pion(1, e))
liste_pieces.append(Cavalier(0, 1))
liste_pieces.append(Cavalier(0, 6))
liste_pieces.append(Tour(0, 0))
liste_pieces.append(Tour(0, 7))
liste_pieces.append(Reine(0, 3))
liste_pieces.append(Roi(0, 4, is_king=True))
liste_pieces.append(Fou(0, 2))
liste_pieces.append(Fou(0, 5))

#Initialisation équipe blanc
for e in range(8):
    liste_pieces.append(Pion(6, e, equipe=1))
liste_pieces.append(Cavalier(7, 1, equipe=1))
liste_pieces.append(Cavalier(7, 6, equipe=1))
liste_pieces.append(Tour(7, 0, equipe=1))
liste_pieces.append(Tour(7, 7, equipe=1))
liste_pieces.append(Reine(7, 3, equipe=1))
liste_pieces.append(Roi(7, 4, equipe=1, is_king=True))
liste_pieces.append(Fou(7, 2, equipe=1))
liste_pieces.append(Fou(7, 5, equipe=1))

#Initialisation du tableau
board = Tableau(liste_pieces)

selected_square = None
second_selected_square = None
tour_blanc = True
tours = 0

def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = BLANC if (row + col) % 2 == 0 else NOIR
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)
            
            if board.tableau[row][col] != 0:
                piece = board.tableau[row][col]
                win.blit(piece.image, rect)

            
            # surligne la case sélectionné
            if selected_square == (row, col):
                pygame.draw.rect(win, SURLIGNAGE, rect, 4)

                
    if selected_square: # surligne les mouvements possibles
        piece = board.tableau[selected_square[0]][selected_square[1]]
        if piece != 0:
            if (piece.couleur == "blanc" and tour_blanc) or (piece.couleur == "noir" and not tour_blanc):
                for move in piece.legal_moves_board(board):#board.can_go(piece): 
                    row, col = move
                    if 0 <= row < 8 and 0 <= col < 8:
                        highlight_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(win, SURLIGNAGE3, highlight_rect, 3)
            

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= col < 8:
        return (row, col)
    return None


def afficher_menu_principal(ecran):
    font_titre = pygame.font.SysFont("Arial", 60, bold=True)
    font_bouton = pygame.font.SysFont("Arial", 36)
    
    titre = font_titre.render("JEU D'ÉCHECS", True, (255, 255, 255))
    
    bouton_jouer_rect = pygame.Rect(WIDTH // 2 - 150, 220, 300, 60)
    bouton_quitter_rect = pygame.Rect(WIDTH // 2 - 150, 320, 300, 60)

    en_menu = True
    while en_menu:
        ecran.fill((30, 30, 30))

        # Affichage du titre
        ecran.blit(titre, (WIDTH // 2 - titre.get_width() // 2, 100))

        # Gère la souris
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()

        # Bouton Jouer
        if bouton_jouer_rect.collidepoint(souris):
            pygame.draw.rect(ecran, (100, 200, 100), bouton_jouer_rect)
            if clic[0]:
                en_menu = False  # Lance le jeu
        else:
            pygame.draw.rect(ecran, (50, 150, 50), bouton_jouer_rect)

        # Bouton Quitter
        if bouton_quitter_rect.collidepoint(souris):
            pygame.draw.rect(ecran, (200, 100, 100), bouton_quitter_rect)
            if clic[0]:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(ecran, (150, 50, 50), bouton_quitter_rect)

        # Texte sur les boutons
        texte_jouer = font_bouton.render("Nouvelle partie", True, (255, 255, 255))
        texte_quitter = font_bouton.render("Quitter", True, (255, 255, 255))
        ecran.blit(texte_jouer, (WIDTH // 2 - texte_jouer.get_width() // 2, 230))
        ecran.blit(texte_quitter, (WIDTH // 2 - texte_quitter.get_width() // 2, 330))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def affichage_fin(tour_blanc):
    couleur = "noir"
    if tour_blanc:
        couleur = "blanc"
        
    if couleur == "noir":
        pass #blanc remporte
    else:
        pass #noir remporte




def main():
    afficher_menu_principal(WIN)
    
    global selected_square, second_selected_square, tour_blanc, tours
    
    running = True
    while running:
        draw_board(WIN)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = get_square_under_mouse(pygame.mouse.get_pos())
                
                if clicked_square:
                    
                    
                    if selected_square == clicked_square:
                        selected_square = None  # Déselectionner
                        
                        
                    elif selected_square != None and second_selected_square == None:
                        second_selected_square = clicked_square # Sélectionner un second carré
                        if board.tableau[selected_square[0]][selected_square[1]] != 0:  
                            deplacement_fait = board.deplacement(board.tableau[selected_square[0]][selected_square[1]], clicked_square, tour_blanc)
                            
                            if deplacement_fait == True:
                                selected_square = None
                                second_selected_square = None
                                tour_blanc = not tour_blanc
                                tours += 1
                                if board.is_checkmate_or_stalemate(tour_blanc)[0] == True:
                                    if board.is_checkmate_or_stalemate(tour_blanc)[1] == True:
                                        print("Partie nulle")
                                    else:
                                        affichage_fin(tour_blanc)
                                
                                
                    elif selected_square != None and second_selected_square != None:
                        selected_square = clicked_square # Désectionner le second carré et sélectionner le nouveau carré
                        second_selected_square = None
                    else:
                        selected_square = clicked_square # Sélectionner le nouveau carré
    pygame.quit()
    sys.exit()    


if __name__ == "__main__":
    main()