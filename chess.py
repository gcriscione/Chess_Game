from asyncio.windows_events import NULL
import pygame


#comando di inizializzazione -----------------------------------------------------------------------------------------
pygame.init()


# Regolazione Display
win_width = 680
win_heigth = 680
flags = 0
win = pygame.display.set_mode((win_width, win_heigth), flags)     #crea un display con dimensione fissata
pygame.display.set_caption("Chess")                               #modifica il nome della finestra
FPS = 30                                                          #aggiornamento dei segnali  (refresh della pagina)
clock = pygame.time.Clock() 
background = (140, 140, 140)
GREEN = (118, 150, 86)                            #Colore cella 1 scacchiera
WHITE = (238, 238, 210)                           #Colore cella 2 scacchiera
YELLOW1 = (186, 202, 43)                          #colore selezione cella 1
YELLOW2 = (246, 246, 105)                         #colore selezione cella 2
RED = (200,0,0)                                   #colore scacco re
size_cell = 75                                    #dimensione cella quadrata
first_cell_x = 40                                 #distanza scacchiera dal margine destro/sinistro
first_cell_y = 40                                 #distanza scacchiera dal margine superiore/inferiore
font = pygame.font.Font("freesansbold.ttf", 24)   #setta il font e la grandezza del testo
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
        return self                #consente di lavorare meglio con l'oggetto ( ES. piece.set_color(RED).get_color() )
    
    def get_color(self):
        return self.__color

    def set_piece(self, piece):
        self.__piece = piece
        return self

    def get_piece(self):
        return self.__piece

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Cell:(color: "+str(self.__color)+", posx: "+str(self.posx)+", posy: "+str(self.posy)+", piece: "+str(self.__piece)+")}"
        return s


# Classi Pezzi
class king(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color  = color 
        self.scacco = False                #indica se il re è sotto scacco
        self.moved  = False                #indica se il re si è mai spostato dall'inizio della partita
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

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimenti False
    def move(self, posx_1, posy_1, posx_2, posy_2):
        global pos_King

        #movimento non valido se finisce su una cella con un pezzo dello stesso colore di quello da spostare
        if(chess_board[posx_2][posy_2].get_piece() != NULL):
            if( chess_board[posx_2][posy_2].get_piece().get_color() == chess_board[posx_1][posy_1].get_piece().get_color() ):
                return False
        
        #controlla che lo spostamento sia di max 1 cella verso qualsiasi direzione
        if ( (abs(posx_1-posx_2)<=1) and (abs(posy_1-posy_2)<=1) ):
            enemy_king = 0
            if( self.color ):
                enemy_king = 1
            #controlla che il re non finisca su una casella adiacente a quella del re nemico
            if( ((abs(posx_2 - pos_King[enemy_king][0]))>1) or ((abs(posy_2 - pos_King[enemy_king][1]))>1) ):
                return True
        
        return False

    #disegna l'immagine del pezzo
    def draw(self, posx, posy):
        global pos_King

        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

    #setta la variabile scacco
    def set_scacco(self, sc):
        self.scacco = sc
        return self

    #ritorna la variabile scacco
    def get_scacco(self):
        return self.scacco

    #setta la variabile moved a True
    def set_moved(self):
        self.moved = True
        return self

    #ritorna la variabile moved
    def get_moved(self):
        return self.moved
    
    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    @staticmethod    #posizione iniziale re asse x
    def get_posx():
        return 4
    
    @staticmethod    #posizione iniziale re asse y
    def get_posy():
        return 0

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: King, color: "+str(self.color)+")}"
        return s

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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
                    return False
            return True

        elif(posy_1 == posy_2):
            #controlla se ci sono pezzi in mezzo
            movement = 1    
            if(posy_1 > posy_2):
                movement = -1
            for i in range((posy_1+movement), posy_2, movement):
                if (chess_board[posx_1][i].get_piece() != NULL):
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True
        
        #print("Moviemnto non valido")
        #print("> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posx_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo
    
    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: Queen, color: "+str(self.color)+")}"
        return s

class Rook(object):
    #costruttore( colore(True=White) )
    def __init__(self, color):
        self.color = color 
        self.moved = False
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

    #Ritorna True se il movimento da (posx_1, posy_1) --> (posx_2, posy_2) e consentito, altrimenti False
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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
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
        
        
        #print("Moviemnto non valido")
        #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagine del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

    #setta la variabile moved a True
    def set_moved(self):
        self.moved = True
        return self

    #ritorna la variabile moved
    def get_moved(self):
        return self.moved

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: Rook, color: "+str(self.color)+")}"
        return s

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
        
        #print("Moviemnto non valido")
        #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: Knight, color: "+str(self.color)+")}"
        return s

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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(check_x)+","+str(check_y)+")")
                    return False
            return True 
        
        #print("Moviemnto non valido")
        #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo

    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: Bishop, color: "+str(self.color)+")}"
        return s

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
                    #print("Moviemnto non valido")
                    #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+") err_in:pos("+str(posx_1)+","+str(posy_1+c)+")")
                    return False
            return True

        
        #print("Moviemnto non valido")
        #print("-> pos("+str(posx_1)+","+str(posy_1)+") -\-> pos("+str(posx_2)+","+str(posy_2)+")")
        return False

    #Ritorna true se colore=Bianco
    def get_color(self):
        return self.color

    #disegna l'immagene del pezzo
    def draw(self, posx, posy):
        win.blit(self.king_piece, self.set_coord(posx, posy))      #visualizza pezzo
    
    #rappresentazione oggetto, utile per il printf
    def __repr__(self):
        s = "{Piece:(type: Pawn, color: "+str(self.color)+")}"
        return s
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
    
#Inserimento pezzi sulla scacchiera
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
def check_scacco(chess_board, posx, posy, color):

    #controlla l'asse verticale dal basso verso l'alto
    for i in range(0, (posy), 1):
        tmp_piece = chess_board[posx][posy-(i+1)].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( posx, posy-(i+1), posx, posy)) ):
                #print( "v) Scacco da ("+str(posx)+"), ("+str(posy-(i+1))+")" )
                return True
            else:
                break
            
    #controlla l'asse verticale dall'alto verso il basso
    for i in range(0, (7-posy), 1):
        tmp_piece = chess_board[posx][posy+(i+1)].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( posx, posy+(i+1), posx, posy)) ):
                #print( "v) Scacco da ("+str(posx)+"), ("+str(posy+(i+1))+")" )
                return True
            else:
                break

    #controlla l'asse orizzontale da destra verso sinistra  ( [<-] )
    for i in range(0, (posx), 1):
        tmp_piece = chess_board[(posx-(i+1))][posy].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx-(i+1)), posy, posx, posy)) ):
                #print( "o) Scacco da ("+str((posx-(i+1)))+"), ("+str(posy)+")" )
                return True
            else:
                break

    #controlla l'asse orizzontale da sinistra verso destra  ( [->] )
    for i in range(0, (7-posx), 1):
        tmp_piece = chess_board[(posx+(i+1))][posy].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx+(i+1)), posy, posx, posy)) ):
                #print( "o) Scacco da ("+str((posx+(i+1)))+"), ("+str(posy)+")" )
                return True
            else:
                break

    #controllo possibile attacco da un cavallo
    segno1 = 1
    segno2 = 1
    for i in range(1, 9):
        x = posx+( segno1 * (1+(i%2)) )
        y = posy+( segno2 * (1+((i+1)%2)) )

        #controlla che x,y appartengono alla matrice
        if( (x>=0) and (x<8) and (y>=0) and (y<8)):
            #print("("+str(x)+":"+str(segno1)+", "+str(y)+":"+str(segno2)+")", end="- " )
            tmp_piece = chess_board[x][y].get_piece()
            #controlla se c'è un pezzo nella cella selezionata
            if( (tmp_piece!=NULL) ):
                #controlla se in quella cella c'è un cavallo del colore opposto che può mangiare il re
                if( (isinstance(tmp_piece, Knight)) and (tmp_piece.get_color() != color) and (tmp_piece.move( x, y, posx, posy)) ):
                    return True

        match (i//2):
            case 1:
                segno1 = -1
                segno2 = -1
            case 2:
                segno1 = 1
                segno2 = -1
            case 3:
                segno1 = -1
                segno2 = 1


    #controlla la diagonale1_up dal basso verso l'alto ( [\] )
    for i in range(0, min(posx, posy), 1):
        tmp_piece = chess_board[(posx-(i+1))][(posy-(i+1))].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx-(i+1)), (posy-(i+1)), posx, posy)) ):
                #print( "d1) Scacco da ("+str((posx-(i+1)))+", "+str((posy-(i+1)))+")" )
                return True
            else:
                break

    #controlla la diagonale1_down dall'alto verso il basso ( [\] )
    for i in range(0, ( min((7-posx),(7-posy)) ), 1):
        tmp_piece = chess_board[(posx+(i+1))][(posy+(i+1))].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx+(i+1)), (posy+(i+1)), posx, posy )) ):
                #print( "d1) Scacco da ("+str((posx+(i+1)))+", "+str((posy+(i+1)))+")" )
                return True
            else:
                break
    
    #controlla la diagonale2_up dalL'alto verso il basso ( [<-/] )
    for i in range(0, ( min((7-posx), posy) ), 1):
        tmp_piece = chess_board[(posx+(i+1))][(posy-(i+1))].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx+(i+1)), (posy-(i+1)), posx, posy )) ):
                #print( "d2) Scacco da ("+str((posx+(i+1)))+"), ("+str((posy-(i+1)))+")" )
                return True
            else:
                break

    #controlla la diagonale2_down dall'basso verso l'alto ( [/->] )
    for i in range(0, (min(posx, (7-posy))), 1):
        tmp_piece = chess_board[(posx-(i+1))][(posy+(i+1))].get_piece()
        #controlla se c'è un pezzo nella cella selezionata
        if( (tmp_piece != NULL)):
            #controlla se il pezzo nella cella selezionata è del colore opposto a quello del re e se può mangiarlo
            if( (tmp_piece.get_color() != color) and (tmp_piece.move( (posx-(i+1)), (posy+(i+1)), posx, posy )) ):
                #print( "d22) Scacco da ("+str((posx-(i+1)))+"), ("+str((posy+(i+1)))+")" )
                return True
            else:
                break
        
    return False            

#aggiorna le variabili che tengono traccia della posizione dei 2 re
def update_pos_King(piece, posx, posy):
    global pos_King
    if( isinstance(piece, king) ):
        if(piece.get_color()):
            pos_King[0] = (posx, posy)
        else:
            pos_King[1] = (posx, posy)
    
#controlla se la mossa di un pezzo crea una situazione di scacco per il proprio re (nel caso annulla la mossa e restituisce: FALSE)
def move_validation(cell1, cell2, tmp_piece_cell2, king_color, turn_color):
    global chess_board, pos_King
    king_switch = 1
    if(king_color):
        king_switch = 0


    #controlla se si è creata una situazione di scacco per il re king_color
    scacco = check_scacco(chess_board, pos_King[king_switch][0], pos_King[king_switch][1], king_color)
    if(scacco):
        #controlla se il movimento di un pezzo causa scacco al proprio re
        if( king_color == turn_color ):
            cell1.set_color(NULL)                 #deseleziona cella1
            cell2.set_color(NULL)                 #deseleziona cella2
            cell1.set_piece(cell2.get_piece())    #copia il pezzo in cella2 --> cella1
            cell2.set_piece(tmp_piece_cell2)      #ripristina il pezzo precedente in cella2
            #controlla se il pezzo spostato era un re, nel caso aggiorna le variabili che ne tengono traccia
            update_pos_King(cell1.get_piece(), cell1.posx, cell1.posy)
            return False

        #situazione dove un pezzo ha messo sotto scacco il re avversario
        else:
            if(chess_board[(pos_King[(1+king_switch)%2][0])][(pos_King[(1+king_switch)%2][1])].get_piece().get_scacco() == False):
                chess_board[(pos_King[king_switch][0])][(pos_King[king_switch][1])].get_piece().set_scacco(True)
            return True

    #non c'è scacco
    else:
        chess_board[(pos_King[king_switch][0])][(pos_King[king_switch][1])].get_piece().set_scacco(False)
        return True


def arrocco(cell1, cell2, highlighted_cells):
    global chess_board

    #controlla se il pezzo da spostare è un re e che esso non si è mai mosso dall'inizio della partita
    if( isinstance(cell1.get_piece(), king) and (cell1.get_piece().get_moved()==False) ):
        king_posy = 0
        if( cell1.get_piece().get_color() ):
            king_posy = 7
        
        #controlla che la cella dove si vuole spostare sia quella dell'arrocco
        if( (cell2.posy==king_posy) and ((cell2.posx==2) or (cell2.posx==6)) ):
            direction = 1
            if(cell1.posx > cell2.posx):
                direction = -1
            #controlla che dal lato dell'arrocco ci sia una torre che non si è mai mossa dall'inizio della partita
            rook_piece = chess_board[int((7+(direction*7))/2)][king_posy].get_piece()
            if( (isinstance(rook_piece, Rook)) and (rook_piece.get_moved()==False) ):
                #controlla che non ci siano pezzi in mezzo
                if( (chess_board[4+(direction)][king_posy].get_piece()== NULL) and (chess_board[4+(2*direction)][king_posy].get_piece()== NULL) and (chess_board[3+(2*direction)][king_posy].get_piece()== NULL)):

                    #controlla che il re possa spostarsi nella celle di transizione fine a raggiungere la destinazione
                    for i in range(1,3):
                        chess_board[4+(i*direction)][king_posy].set_piece(chess_board[4+((i-1)*direction)][king_posy].get_piece())         #copio il re dalla sua cella alla successiva
                        chess_board[4+((i-1)*direction)][king_posy].set_piece(NULL)                                                        #elimino il re dalla sua cella

                        #verifica se si è creata una situazione di scacco
                        if( check_scacco(chess_board, (4+(i*direction)), king_posy, chess_board[4+(i*direction)][king_posy].get_piece().get_color()) ):
                            cell1.set_piece(chess_board[4+(i*direction)][king_posy].get_piece())
                            chess_board[4+(i*direction)][king_posy].set_piece(NULL)
                            return False
                        
                    #se tutte le condizioni per arroccare sono valide, esegue l'arrocco (spostando la torre)
                    chess_board[4+(direction)][king_posy].set_piece(rook_piece)            #copia la torre nella cella destinazione
                    chess_board[int((7+(direction*7))/2)][king_posy].set_piece(NULL)       #rimuove la torre dalla cella iniziale
                    update_pos_King(cell2.get_piece(), cell2.posx, cell2.posy)             #aggiorna la posizione del re

                    #cambio selezione celle
                    highlighted_cells[0].set_color(NULL)        #deseleziona la cella1 precedente
                    highlighted_cells[1].set_color(NULL)        #deseleziona la cella1 precedente
                    highlighted_cells[0] = cell1                #aggiorna highlighted cells
                    highlighted_cells[1] = cell2                #aggiorna highlighted cells

                return True
        
    return False

#verifica se un pedone ha raggiunto la promozione
def pawn_to_queen(cell2):
    #controlla se il pezzo appena spostato è un pedone
    if( isinstance(cell2.get_piece(), Pawn) ):
        #controlla se un pedone (bianco) è arrivato in fondo alla scacchiera
        if( (cell2.posy == 0) ):
            cell2.set_piece(Queen(True))
        elif( (cell2.posy == 7) ):
            cell2.set_piece(Queen(False))

#Colora la cella della scacchiera di default
def color_cell_chessboard(posx, posy):
    global win, GREEN, WHITE

    x = first_cell_x + (size_cell * posx)
    y = first_cell_y + (size_cell * posy)
    if ((posx+posy)%2 == 0):
        pygame.draw.rect(win, GREEN, (x, y, 75, 75))
    else:
        pygame.draw.rect(win, WHITE, (x, y, 75, 75))

    #Stampa su ogni cella la propria coordinata
    #number_cell = (font.render((str(posx)+","+str(posy)), True, (0,0,0)))
    #win.blit(number_cell, (x, y))

    piece = chess_board[posx][posy].get_piece()
    if( (isinstance(piece,king)) and (piece.get_scacco()) ):
        pygame.draw.rect(win, RED, (x, y, 75, 75))

#stampa della scacchiera
def draw_chessboard(chess_board, numbers, letters):
    global win, first_cell_x, first_cell_y

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
    
    draw_chessboard(chess_board, numbers, letters)     #disegna la scacchiera

    #aggiorna il display
    pygame.display.update()
#-------------------------------------- ********* -------------------------------------------------------




#Main-Loop *********************************************************************************************************
input = True                                   #indica se è arrivato un qualche segnale e deve aggiornare lo schermo  
run = True                                     #condizione loop
chess_board = []                               #matrice che rappresenta la scacchiera
set_chessboard(chess_board)                    #inizializza le celle della scacchiera 
insert_piece_init(chess_board)                 #inserisce i pezzi nella schacchiera
pos_wKing = (4, 7)                             #posizione iniziale del re bianco
pos_bKing = (4, 0)                             #posizione iniziale del re nero
pos_King = [pos_wKing, pos_bKing]              #coppia che contiene le posizione dei due re
scacco = False                                 #stato di scacco
(numbers, letters) = set_text_chessboard()     #crea 2 array con numeri e lettere in formato font.render necessati per disegnare la scacchiera
switch_mouse = True                            #variabile di supporto per gestire il click del mouse
select_cells = 2                               #indica il numero di celle selezionate
turn_color = True                              #indica a quale colore tocca muovere (True = turno Bianco)
cell1 = chess_board[0][0]                      #variabile di supporto per lo spostamento dei pezzi  (inizializzata con valore generico solo per evitare un ulteriore controllo)
cell2 = chess_board[0][0]                      #variabile di supporto per lo spostamento dei pezzi  ( '' '' '' )
tmp_color_cell = WHITE                         #variabile temporanea per settare il colore di una cella
highlighted_cells = [cell1, cell2]             #indica le celle selezionate


while(run):
    clock.tick(30)                       #tempo di aggiornamento dell'immagine (FPS) 

    #controlla gli eventi
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:      #interrompe il ciclo se viene premuto quit
            run = False

    #controlla se il mouse passa da up a down (utilizza variabile di supporto switch_mouse)  
    if( (event.type == pygame.MOUSEBUTTONDOWN) and switch_mouse ): 
        mx, my = pygame.mouse.get_pos()              #prende le coordinate del mouse
        posx, posy = get_posxy(mx, my)               #estrae la posizione della cella dove si trova il mouse
        
        #controlla che la cella selezionata sia valida
        if( (posx>=0 and posx<8) and (posy>=0 and posy<8) ):

            #controlla se non era già stata selezionata una cella
            if(select_cells==2):
                #controlla che la cella selezionata abbia un pezzo e che il colore di tale pezzo == turn_color
                if(chess_board[posx][posy].get_piece() != NULL and chess_board[posx][posy].get_piece().get_color() == turn_color):
                    select_cells = 1                          #indica che è stata selezionata una cella
                    cell1 = chess_board[posx][posy]           #cella1 = cella indicata dal cursore
                    tmp_color_cell = color_select_cell(cell1.posx, cell1.posy)   #ritorna il tipo di colore per evidenziare la cella
                    cell1.set_color(tmp_color_cell)            #setta il colore della cella1 se è presente un pezzo
                
            #caso in cui era già stata selezionata una cella
            else:
                select_cells = 2                           #indica che sono state selezionate 2 celle
                cell2 = chess_board[posx][posy]            #cella destinazione

                #controlla che cella di partenza e di destinazione siano diverse
                if( (cell1.posx != cell2.posx) or (cell1.posy != cell2.posy) ):
                    #controlla se viene selezionato un'altro pezzo di colore = colore del turno
                    if(chess_board[posx][posy].get_piece() != NULL and chess_board[posx][posy].get_piece().get_color() == turn_color):
                        select_cells = 1                          #indica che è stata selezionata una cella
                        cell1.set_color(NULL)                     #deseleziona la cella1 precedente
                        cell1 = chess_board[posx][posy]           #cella1 = cella indicata dal cursore
                        tmp_color_cell = color_select_cell(cell1.posx, cell1.posy)    #ritorna il tipo di colore per evidenziare la cella
                        cell1.set_color(tmp_color_cell)           #setta il colore della cella1 se è presente un pezzo

                    #controlla che il pezzo in cella1 può spostarsi in cella2
                    elif(cell1.get_piece().move(cell1.posx, cell1.posy, cell2.posx, cell2.posy)):
                        tmp_color_cell = color_select_cell(cell2.posx, cell2.posy)   #ritorna il tipo di colore per evidenziare la cella
                        cell2.set_color(tmp_color_cell)            #evidenzia la cella2 selezionata dal cursore
                        tmp_piece_cell2 = cell2.get_piece()        #salva il pezzo contenuto in cella2
                        cell2.set_piece(cell1.get_piece())         #copia il pezzo in cella1 --> cella2
                        cell1.set_piece(NULL)                      #elimina il pezzo in cella1

                        #controlla se il pezzo spostato era un re, nel caso aggiorna le variabili che ne tengono traccia
                        update_pos_King(cell2.get_piece(), cell2.posx, cell2.posy)

                        #se la mossa del bianco non è valida ripete il turno
                        if( not(move_validation(cell1, cell2, tmp_piece_cell2, True, turn_color)) ):
                            continue

                        #se la mossa del nero non è valida ripete il turno
                        if( not(move_validation(cell1, cell2, tmp_piece_cell2, False, turn_color)) ):
                            continue

                        #controlla se il pezzo spostato è un pedone ed ha raggiunto la promozione
                        pawn_to_queen(cell2)

                        #cambio selezione celle
                        highlighted_cells[0].set_color(NULL)        #deseleziona la cella1 precedente
                        highlighted_cells[1].set_color(NULL)        #deseleziona la cella1 precedente
                        highlighted_cells[0] = cell1                #aggiorna highlighted cells
                        highlighted_cells[1] = cell2                #aggiorna highlighted cells


                        #se il pezzo spostato era un re o torre, setta moved a true (utile per condizione arrocco)
                        if( isinstance(cell2.get_piece(), king) or isinstance(cell2.get_piece(), Rook) ):
                            cell2.get_piece().set_moved()

                        #cambia turno
                        turn_color = not(turn_color)              
                    
                    #caso movimento pezzo non valido
                    else:
                        #controlla se un re stava eseguendo un arrocco
                        if( arrocco(cell1, cell2, highlighted_cells) ):
                            turn_color = not(turn_color)
                        else:
                            cell1.set_color(NULL)              #deseleziona cella1
            
            input = True                                 #indica di aggiornare il display
            switch_mouse = False                         #setta a False per evitare che con il mouse esegua ripetutamente la selezione

            #print(str((posx, posy)))
        
    #setta switch_mode=True quando il mouse viene rilasciato
    elif event.type == pygame.MOUSEBUTTONUP and not(switch_mouse):
        switch_mouse = True             


    #aggiorna solo se arriva qualche input
    if input:
        redraw(chess_board, numbers, letters)
        input = False


pygame.quit()