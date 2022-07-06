'''
   Funzioni in più
'''
#stampa della scacchiera senza matrice
def draw_chessboard2():
    (numbers, letters) = set_text_chessboard()     #prende i numeri e lettere da inserire
    cell_y = first_cell_y                          #posizione della prima cella
    cell_x = first_cell_x                          #posizione della prima cella
    number_x = first_cell_x/3                      #pos_x numeri
    number_y = first_cell_y + (size_cell/3)        #posy_ numeri
    letters_x = first_cell_x + (size_cell/3)       #pos_x lettere
    letters_y = first_cell_y/3                     #pos_y lettere

    #costruzione della scacchiera
    for j in range(0,8):
        #stampa i numeri e lettere
        win.blit(numbers[j], (number_x, number_y))                      #stampa i numeri a sinistra della scacchiera
        win.blit(numbers[j], ((win_width - number_x - 15), number_y))   #stampa i numeri a destra della scacchiera
        number_y += size_cell
        win.blit(letters[j], (letters_x, letters_y))                      #stampa le lettere a sinistra della scacchiera
        win.blit(letters[j], (letters_x, (win_heigth - letters_y - 18)))  #stampa le lettere a destra della scacchiera
        letters_x += size_cell

        #stampa le celle
        for i in range(0,8):
            if ((i+j)%2 == 0):
                pygame.draw.rect(win, GREEN, (cell_x, cell_y, 75, 75))   #stampa cella verde
            else:
                pygame.draw.rect(win, WHITE, (cell_x, cell_y, 75, 75))   #stampa cella bianca
            cell_x += size_cell

        cell_y += size_cell
        cell_x = first_cell_x


#stampa i pezzi nella scacchiera
def draw_piece():
    wk = king(True)
    bk = king(False)
    wk.draw()
    bk.draw()

    print("wk:"+str(wk.posx)+"-"+str(wk.posy))
    print("bk:"+str(bk.posx)+"-"+str(bk.posy))

    wk.move(3,6)
    wk.draw()

    a = cell(win, (0,0,0), 50, 50)
    a.draw()


#Classe pezzo King
class king(object):
    #costruttore( colore(True=White), posx_sulla_matrice, posy_sulla_matrice) )
    def __init__(self, color, posx=-1, posy=-1):
        #setta le posizione sulla matrice
        if (posx!=-1 and posy!=-1):      #controlla se vengono forniti in input
            self.posx = posx                     #posizione sulla matrice (cella orizzontale)
            self.posy = posy                     #posizione sulla matrice (cella verticale)   
        else:                    #altrimenta setta di default
            #setta correttamente (posx, posy) in base al colore del pezzo
            if color: 
                self.posx = 4                      #posizione sulla matrice (cella orizzontale)
                self.posy = 7                      #posizione sulla matrice (cella verticale)           
            else:
                self.posx = 4                      #posizione sulla matrice (cella orizzontale)
                self.posy = 0                      #posizione sulla matrice (cella verticale)
        
        #carica l'immagine corretta a seconda del colore del pezzo
        if color:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/wk.png'), (75, 75))
        else:
            self.king_piece = pygame.transform.scale(pygame.image.load('chess_img/bk.png'), (75, 75))

        #setta le coordinate (x,y) lin base alla posizione sulla matrice
        self.x = 0
        self.y = 0
        self.set_coord(self.posx, self.posy)

    #setta le coordinate (self.posx, self.posy) sulla base della posizione del pezzo sulla matrice
    def set_coord(self, posx, posy):
        self.x = first_cell_x + (size_cell * posx)
        self.y = first_cell_y + (size_cell * posy)

    #setta la posizione del pezzo sulla matrice sulla base delle coordinate (self.posx, self.posy)
    def set_pos(self):
        self.posx = (self.x - first_cell_x) // size_cell
        self.posy = (self.y - first_cell_y) // size_cell

    #moviemnto
    def move(self, posx, posy):
        if ( (self.posx>= 0) and ((self.posx - x)<=1) and (self.posy - y)<=1 ):
            self.posx = x
            self.posy = y
            self.set_coord(self.posx, self.posy)
            return 0


        print("Moviemnto non valido")
        print("pos("+str(self.posx)+","+str(self.posy)+") -\-> pos("+str(x)+","+str(y)+")")

    #disegna l'immagene del pezzo
    def draw(self):
        win.blit(self.king_piece, (self.x,self.y))      #visualizza pezzo





#*******************    ALTRO
print(")>"+str((cell1.posx, cell1.posy))+" - "+str((cell2.posx, cell2.posy)))