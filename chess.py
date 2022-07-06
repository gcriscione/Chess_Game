from asyncio.windows_events import NULL
from turtle import width
from numpy import number
import pygame
# ********************************
#comado di inizializzazione -----------------------------------------------------------------------------------------
pygame.init()


# Regolazione Display
win_width = 680
win_heigth = 680
flags = 0
win = pygame.display.set_mode((win_width, win_heigth), flags)     #crea un display con dimensione fissata
pygame.display.set_caption("Chess")                               #modifica il nome della finestra
FPS = 30                                                          #aggiornamento dei segnali  (refreash della pagina)
clock = pygame.time.Clock() 
background = (140, 140, 140)
GREEN = (118, 150, 86)                            #Colore cella 1 scacchiera
WHITE = (238, 238, 210)                           #Colore cella 2 scacchiera
YELLOW1 = (186, 202, 43)                          #colore selezione cella 1
YELLOW2 = (246, 246, 105)                         #colore selezione cella 2
RED = (255,0,0)                                   #colore scacco re
size_cell = 75
first_cell_x = 40
first_cell_y = 40
font = pygame.font.Font("freesansbold.ttf", 24)           #setta il font e la grandezza del testo
# - - - - - - - - - - - - - - - - - - - - - - - - - 


#--------------------------------------  CLASSI ------------------------------------------------------
class cell(object):
    def __init__(self, win, color, posx, posy, piece=NULL):
        self.__color = color
        self.posx = posx
        self.posy = posy
        self.__win = win
        self.__piece = piece

    def draw(self):
        if self.__color != NULL:
            x = first_cell_x + (size_cell * self.posx)
            y = first_cell_y + (size_cell * self.posy)
            pygame.draw.rect(self.__win, self.__color, (x, y, 75, 75))
        if self.__piece != NULL:
            self.__piece.draw(self.posx, self.posy)

    def set_color(self, color):
        self.__color = color
        return self                #consete di lavorare meglio con l'oggetto ( ES. piece.set_color(RED).get_color() )
    
    def get_color(self):
        return self.__color

    def set_piece(self, piece):
        self.__piece = piece
        return self

    def get_piece(self):
        return self.__piece

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Cell:(color: "+str(self.__color)+", posx: "+str(self.__posx)+", posy: "+str(self.__posy)+", piece: "+str(self.__piece)+")}"
        return s

    def get_posx(self):
        return self.posx

    def get_posy(self):
        return self.posy

# Classi Pezzi
class king(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color 
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wk.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bk.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
        
        if ( (abs(posx_1-posx_2)<=1) and (abs(posy_1-posy_2)<=1) ):
            return True
        
        print("Moviemnto non valido")
        print("> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posx_2)+")")
        return False

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    @staticmethod
    def get_posx():
        return 4
    
    @staticmethod
    def get_posy():
        return 0

class Queen(object):
    #costruttore( colore(True=White) )
    def __init__(self, color): 
        self.color = color
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wq.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bq.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
        
        #Controlla che non ci siano pezzi nelle celle di transizione, dalla cella di partenza fino alla cella destinazione (estremi esclusi)
        if(posx_1 == posx_2):
            #controlla se ci sono pezzi in mezzo
            movement = 1    
            if(posy_1 > posy_2):
                movement = -1
            for i in range((posy_1+movement), posy_2, movement):
                if (chess_board[posx_1][i].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
                    return False
            return True

        elif(posy_1 == posy_2):
            #controlla se ci sono pezzi in mezzo
            movement = 1    
            if(posy_1 > posy_2):
                movement = -1
            for i in range((posy_1+movement), posy_2, movement):
                if (chess_board[posx_1][i].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
                    return False
            return True
        
        elif((posx_1 - posx_2) == (posy_1 - posy_2)):
            #controlla se ci sono pezzi in mezzo
            movement = 1             #indica in che verso si sposta
            if(posy_1 > posy_2):
                movement = -1
            #print("Controllo ("+str(movement)+", "+str(posy_1-posy_2)+") :")

            for i in range(1, abs(posy_1-posy_2), 1):
                check_x = (posx_1+(movement*i))
                check_y = (posy_1+(movement*i))
                #print("("+str(check_x)+","+str(check_y)+"), ",end="")
                if (chess_board[check_x][check_y].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True
        
        elif((posx_1 - posx_2) == (posy_2 - posy_1)):
            #controlla se ci sono pezzi in mezzo
            movement = 1             #indica in che verso si sposta
            if(posx_1 > posx_2):     #spostamento a sinistra
                movement = -1
            for i in range(1, abs(posx_1-posx_2), 1):
                check_x = (posx_1+(movement*i))
                check_y = (posy_1+((-movement)*i))
                if (chess_board[check_x][check_y].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True
        
        print("Moviemnto non valido")
        print("> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posx_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

class Rook(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color 
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wr.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/br.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):
        global chess_board

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False

        if ( (posx_1 == posx_2) ):
            #controlla se ci sono pezzi in mezzo
            movement = 1    
            if(posy_1 > posy_2):
                movement = -1
            for i in range((posy_1+movement), posy_2, movement):
                if (chess_board[posx_1][i].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
                    return False

            return True

        elif( (posy_1 == posy_2) ):
            #controlla se ci sono pezzi in mezzo
            movement = 1    
            if(posx_1 > posx_2):
                movement = -1
            for i in range((posx_1+movement), posx_2, movement):
                if (chess_board[i][posy_1].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
                    return False

            return True
        
        
        print("Moviemnto non valido")
        print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

class Knight(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wn.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bn.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
        
        if ( (abs(posx_1 - posx_2)==2 and (abs(posy_1 - posy_2)==1)) or (abs(posx_1 - posx_2)==1 and (abs(posy_1 - posy_2)==2)) ):
            return True
        
        print("Moviemnto non valido")
        print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

class Bishop(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wb.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bb.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):
        global chess_board

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
        
        if ( ((posx_1 - posx_2) == (posy_1 - posy_2))):
            #controlla se ci sono pezzi in mezzo
            movement = 1             #indica in che verso si sposta
            if(posy_1 > posy_2):
                movement = -1
            #print("Controllo ("+str(movement)+", "+str(posy_1-posy_2)+") :")

            for i in range(1, abs(posy_1-posy_2), 1):
                check_x = (posx_1+(movement*i))
                check_y = (posy_1+(movement*i))
                #print("("+str(check_x)+","+str(check_y)+"), ",end="")
                if (chess_board[check_x][check_y].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True
        elif( ((posx_1 - posx_2) == (posy_2 - posy_1)) ):
            #controlla se ci sono pezzi in mezzo
            movement = 1             #indica in che verso si sposta
            if(posx_1 > posx_2):     #spostamento a sinistra
                movement = -1
            for i in range(1, abs(posx_1-posx_2), 1):
                check_x = (posx_1+(movement*i))
                check_y = (posy_1+((-movement)*i))
                if (chess_board[check_x][check_y].get_piece() != NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True 
        
        print("Moviemnto non valido")
        print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False


    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

class Pawn(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wp.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bp.png'), (75, 75))

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        x = first_cell_x + (size_cell * posx)
        y = first_cell_y + (size_cell * posy)
        return (x,y)

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimento False
    def move(self, posx_1, posy_1, posx_2, posy_2):
        global chess_board

        #setta delle variabili di supporto per poter spostare il pedone di 2
        check = 1             #max celle spostamento pedone in avanti
        if self.color:
            c = -1            #spostamento verso l'alto
            if (posy_1==6):
                check = 2     #max celle spostamento pedone
        else:
            c = 1            #spostamento verso il basso
            if (posy_1==1):
                check = 2     #max celle spostamento pedone


        #controlla se nella cella di destinazione c'è un pezzo
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
            #ritorna true solo se sta mangiando un pezzo avversario con uno spostamento obliquo
            elif( (abs(posx_1 - posx_2)==1) and ((posy_2 - posy_1)*c==1) ):
                return True


        #controlla se lo spostamento in avanti può essere effettuato
        elif ( ((posx_1 - posx_2)==0) and ((posy_2 - posy_1)*c>=0 and (posy_2 - posy_1)*c<=check) ):
            #verifica se c'è un pezzo nella cella di passaggio in caso di spostamento di 2 celle
            if(check==2):
                if(chess_board[(posx_1)][(posy_1+c)].get_piece()!=NULL):
                    print("Moviemnto non valido")
                    print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(posx_1)+","+str(posy_1+c)+")")
                    return False
            return True

        
        print("Moviemnto non valido")
        print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo
#-------------------------------------- ******* ------------------------------------------------------




#--------------------------------------  FUNZIONI ------------------------------------------------------
#funzione di inizializzazione che crea il testo dei numeri e lettere a bordo tastiera
def set_text_chessboard():
    numbers = []
    for i in range(8,0,-1):
        numbers.append(font.render(str(i), True, (0,0,0)))       #setta: scritta, visible, fontground, background

    letters = []
    for i in range(0,8):
        letters.append(font.render(chr(65+i), True, (0,0,0)))       #setta: scritta, visible, fontground, background
    
    return (numbers, letters)

#inizializza la matrice chess_board che rappresenta la scacchiera
def set_chessboard(chess_board):
    global win
    column = []

    #costruzione della scacchiera
    for i in range(0,8):
        for j in range(0,8):
            if ((i+j)%2 == 0):
                column.append(cell(win, NULL, i, j))
            else:
                column.append(cell(win, NULL, i, j))
        chess_board.append(column)
        column = []
    
#Inserimento pezzi sulla schacchiera
def insert_piece_init(chess_board):
    #         White Piece
    #King
    chess_board[king.get_posx()][ (7-king.get_posy()) ].set_piece(king(True)) 

    #Queen
    chess_board[3][7].set_piece(Queen(True))

    #Rook
    chess_board[0][7].set_piece(Rook(True))
    chess_board[7][7].set_piece(Rook(True))

    #Bishop
    chess_board[2][7].set_piece(Bishop(True))
    chess_board[5][7].set_piece(Bishop(True))

    #Knight
    chess_board[1][7].set_piece(Knight(True))
    chess_board[6][7].set_piece(Knight(True))

    #Pawn
    for i in range(0, 8):
        chess_board[i][6].set_piece(Pawn(True))

    #         Black Piece
    #king
    chess_board[king.get_posx()][king.get_posy()].set_piece(king(False)) 

    #Rook
    chess_board[0][0].set_piece(Rook(False))
    chess_board[7][0].set_piece(Rook(False))

    #Bishop
    chess_board[2][0].set_piece(Bishop(False))
    chess_board[5][0].set_piece(Bishop(False))

    #Knight
    chess_board[1][0].set_piece(Knight(False))
    chess_board[6][0].set_piece(Knight(False))

    #Pawn
    for i in range(0, 8):
        chess_board[i][1].set_piece(Pawn(False))

    #Queen
    chess_board[3][0].set_piece(Queen(False))



#date le coordinate x,y del mouse ritorna la posizione della cella corrispondente
def get_posxy(x, y):
    posx = (x - first_cell_x)//size_cell
    posy = (y - first_cell_y)//size_cell
    return (posx, posy)

#ritorna il colore di selezione in base alla posizione della cella
def color_select_cell(posx, posy):
    if ((posx+posy)%2 == 0):
        return YELLOW1 
    else:
        return YELLOW2

#controlla se il re in pos(posx, posy) si trova in un situazione di scacco
def check_scacco(posx, posy):
    global chess_board

    print("pos:"+str(posx)+", "+str(posy))

    #controlla l'asse verticale dal basso verso l'alto
    print("\n\nVerticale1:")
    for i in range(0, (posy), 1):
        print("pos:"+str(posx)+", "+str(posy-(i+1)), end=" - ")

    #controlla l'asse verticale dall'alto verso il basso
    print("\n\nVerticale2:")
    for i in range(0, (7-posy), 1):
        print("pos:"+str(posx)+", "+str(posy+(i+1)), end=" - ")

    #controlla l'asse orizzontale da destra verso sinistra  ( [<-] )
    print("\n\nOrizzontale1:")
    for i in range(0, (posx), 1):
        print("pos:"+str(posx-(i+1))+", "+str(posy), end=" - ")

    #controlla l'asse orizzontale da sinistra verso destra  ( [->] )
    print("\n\nOrizzontale2:")
    for i in range(0, (7-posx), 1):
        print("pos:"+str(posx+(i+1))+", "+str(posy), end=" - ")

    #controlla la diagonale1_up dal basso verso l'alto ( [\] )
    print("\n\nDiagonale1_up:")
    for i in range(0, posx, 1):
        print("pos:"+str(posx-(i+1))+", "+str(posy-(i+1)), end=" - ")

    #controlla la diagonale1_down dall'alto verso il basso ( [\] )
    print("\n\nDiagonale1_down:")
    for i in range(0, (7-posx), 1):
        print("pos:"+str(posx+(i+1))+", "+str(posy+(i+1)), end=" - ")
    
    #controlla la diagonale2_up dal basso verso l'alto ( [/] )
    print("\n\nDiagonale2_up:")
    for i in range(0, min(posx, posy), 1):
        print("pos:"+str(posx+(i+1))+", "+str(posy-(i+1)), end=" - ")

    #controlla la diagonale2_down dall'alto verso il basso ( [/] )
    print("\n\nDiagonale2_down:")
    for i in range(1, (7-max(posx, posy)), 1):
        print("pos:"+str(posx-i)+", "+str(posy+i), end=" - ")
        


#Colora la cella della scacchiera di default
def color_cell_chessboard(posx, posy):
    global win, GREEN, WHITE

    x = first_cell_x + (size_cell * posx)
    y = first_cell_y + (size_cell * posy)
    if ((posx+posy)%2 == 0):
        pygame.draw.rect(win, GREEN, (x, y, 75, 75))
    else:
        pygame.draw.rect(win, WHITE, (x, y, 75, 75))

#stampa della scacchiera
def draw_chessboard(chess_board, numbers, letters):

    number_x = first_cell_x/3                      #pos_x numeri
    number_y = first_cell_y + (size_cell/3)        #posy_ numeri
    letters_x = first_cell_x + (size_cell/3)       #pos_x lettere
    letters_y = first_cell_y/3                     #pos_y lettere

    for i, column in enumerate(chess_board):
        #stampa i numeri e lettere
        win.blit(numbers[i], (number_x, number_y))                      #stampa i numeri a sinistra della scacchiera
        win.blit(numbers[i], ((win_width - number_x - 15), number_y))   #stampa i numeri a destra della scacchiera
        number_y += size_cell
        win.blit(letters[i], (letters_x, letters_y))                      #stampa le lettere a sinistra della scacchiera
        win.blit(letters[i], (letters_x, (win_heigth - letters_y - 18)))  #stampa le lettere a destra della scacchiera
        letters_x += size_cell

        for j,cell in enumerate(column):
            color_cell_chessboard(i, j)
            cell.draw()
            

#funzione che disegna il display
def redraw(chess_board, numbers, letters):
    global win, background

    win.fill(background)                                #setta lo sfondo
    
    draw_chessboard(chess_board, numbers, letters)     #desegna la scacchiera

    #aggiorna il display
    pygame.display.update()
#-------------------------------------- ********* -------------------------------------------------------




#Mian-Loop *********************************************************************************************************
input = True                                   #indica se è arrivato un qualche segnale e deve aggiornare lo schermo  
run = True                                     #condizione loop
chess_board = []                               #matrice che rappresenta la scacchiera
set_chessboard(chess_board)                    #inizializza le celle della scacchiera 
insert_piece_init(chess_board)                 #inserisce i pezzi nella schacchiera
pos_wKing = (4, 7)                             #posizione iniziale del re bianco
pos_bKing = (4, 0)                             #posizione iniziale del re nero
scacco = False                                 #stato di scacco
(numbers, letters) = set_text_chessboard()     #crea 2 array con numeri e lettere in formato font.render necessati per disegnare la scacchiera
switch_mouse = True                            #variabile di supporto per gestire il click del mouse
select_cells = 2                               #indica il numero di celle selezionate
turn_color = True                              #indica a quale colore tocca muovere (True = turno Bianco)
cell1 = chess_board[0][0]                      #variabile di supporto per lo spostamento dei pezzi  (inizializzata con valore generico solo per evitare un ulteriore controllo)
cell2 = chess_board[0][0]                      #variabile di supporto per lo spostamento dei pezzi  ( '' '' '' )
tmp_color_cell = WHITE                         #variabile temporanea per settare il colore di una cella



check_scacco(4,3)



while(False):
    clock.tick(30)                       #tempo di aggiornamento dell'immagine (FPS) 

    #controlla gli eventi
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:      #interromente il ciclo se viene premuto quit
            run = False

    #controlla se il mouse passa da up a down (utiliazza variabile di supporto switch_mouse)  
    if( (event.type == pygame.MOUSEBUTTONDOWN) and switch_mouse ): 
        mx, my = pygame.mouse.get_pos()              #prende le coordinate del mouse
        posx, posy = get_posxy(mx, my)               #estrae la posizione della cella dove si trova il mouse
        
        #controlla che la cella selezionata sia valida
        if( (posx>=0 and posx<8) and (posy>=0 and posy<8) ):

            #controlla se non era già stata selezionata una cella
            if(select_cells==2):
                #controlla che la cella selezionata abbia un pezzo e che il colore tale pezzo == turn_color
                if(chess_board[posx][posy].get_piece() != NULL and chess_board[posx][posy].get_piece().get_color() == turn_color):
                    select_cells = 1                          #indica che è stata selezionata una cella
                    cell1.set_color(NULL)                     #deseleziona la cella1 precedente
                    cell2.set_color(NULL)                     #deseleziona la cella2 precedente
                    cell1 = chess_board[posx][posy]           #cella1 = cella indicata dal cursore
                    tmp_color_cell = color_select_cell(cell1.get_posx(), cell1.get_posy())
                    cell1.set_color(tmp_color_cell)            #setta il colore della cella1 se è presente un pezzo
                

            #caso in cui era già stata selezionata una cella
            else:
                select_cells = 2                           #indica che sono state selezionate 2 celle
                cell2 = chess_board[posx][posy]            #cella destinazione

                #controlla che cella di partenza e di destinazione siano diverse
                if( (cell1.posx != cell2.posx) or (cell1.posy != cell2.posy) ):
                    #controlla se viene selezionato un'altro pezzo dello stesso colore
                    if(chess_board[posx][posy].get_piece() != NULL and chess_board[posx][posy].get_piece().get_color() == turn_color):
                        select_cells = 1                          #indica che è stata selezionata una cella
                        cell1.set_color(NULL)                     #deseleziona la cella1 precedente
                        cell1 = chess_board[posx][posy]           #cella1 = cella indicata dal cursore
                        tmp_color_cell = color_select_cell(cell1.get_posx(), cell1.get_posy())
                        cell1.set_color(tmp_color_cell)                   #setta il colore della cella1 se è presente un pezzo

                    #controlla che il pezzo in cella1 può spostarsi in cella2
                    elif(cell1.get_piece().move(cell1.posx, cell1.posy, cell2.posx, cell2.posy)):
                        tmp_color_cell = color_select_cell(cell2.get_posx(), cell2.get_posy())
                        cell2.set_color(tmp_color_cell)            #setta il colore della cella2 selezionata dal cursore
                        cell2.set_piece(cell1.get_piece())         #copia il pezzo in cella1 --> cella2
                        cell1.set_piece(NULL)                      #elimina il pezzo in cella1
                        turn_color = not(turn_color)               #cambia turno

                        #controlla se il pezzo appena spostato è un pedone
                        if( isinstance(cell2.get_piece(), Pawn) ):
                            #controlla se un pedone (bianco) è arrivato in fondo alla scacchiera
                            if( (cell2.posy == 0) ):
                                cell2.set_piece(Queen(True))
                            elif( (cell2.posy == 7) ):
                                cell2.set_piece(Queen(False))
                    else:
                        cell1.set_color(NULL)
            
            input = True    
            switch_mouse = False                         #setta a False per evitare che con il mouse premuto esegua questo IF


            #print(str((posx, posy)))
        
    #setta switch_mode=True quando il mouse viene rilasciato
    elif event.type == pygame.MOUSEBUTTONUP and not(switch_mouse):
        switch_mouse = True                          


    #aggiorna solo se arriva qualche input
    if input:
        redraw(chess_board, numbers, letters)
        input = False


pygame.quit()