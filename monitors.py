import threading
import time
import random
import ast
from threading import Condition as C
from threading import Lock as L
import math
import pygame

K = 30

vehiculos = {}
lista_v = []
tanques = [K, K, K]
estacion = [False] * 6
llenado =  [False] * 2
queue = []

l1 = L()
l2 = L()
l3 = L()
l4 = L()
l5 = L()
l6 = L()

ls1 = L()
ls2 = L()
ls3 = L()

cont = 0
"""def on_draw(a):
    arcade.start_render()

    arcade.draw_rectangle_outline(200, 400, 100, 200, arcade.color.BLUE, 4)
    arcade.draw_text(str(tanques[0]), 200, 350, arcade.color.WHITE, anchor_x="center")
    arcade.draw_rectangle_outline(400, 400, 100, 200, arcade.color.BLUE, 4)
    arcade.draw_text(str(tanques[1]), 400, 350, arcade.color.WHITE, anchor_x="center")
    arcade.draw_rectangle_outline(600, 400, 100, 200, arcade.color.BLUE, 4)
    arcade.draw_text(str(tanques[2]), 600, 350, arcade.color.WHITE, anchor_x="center")
"""

class monitor:
    global K
    global queue
    global estacion
    mon_est = [C(l1), C(l2), C(l3), C(l4), C(l5), C(l6)]
    mon_tan = [C(ls1), C(ls2), C(ls3)]
    mon_g = C(L())
    global cont    # controla las gandolas
    global tanques


    def __init__(self):
        self.pv = 0
        self.ps = 0

    def llenar_surtidor(self, index):
        def predicate():
            return bool(1)
        for i in range(K):
            time.sleep(0.5)
            tanques[int(index)] += 1
            print("llenando tanque #" + str(int(index) + 1) + ": " + str(tanques[int(index)]) + " de " + str(K))
        return predicate

    def revisar(self):
        for i in range(6):
            if not estacion[i]:
                self.pv = i
                return i
        return math.inf

    def vacante(self):
        for i in range(6):
            if not estacion[i]:
                estacion[i] = True
                return i
        return -1

    def revisar_llenado(self):
        global cont

        def predicate():
            return bool(1)
        while True:
            if cont < 2:
                return predicate

    def cola_entrada(self, veh):
        global queue
        time.sleep(2)
        queue.append(veh)
        i = self.vacante()
        while i == -1:
            i = self.vacante()
        self.surtir(queue.pop(0), i)

    def surtir(self, c, pos):
        global cont
        c.estado = 1
        """while True:
            if self.revisar() >= 0 and self.revisar() <= len(lista_v) - 1:
                pos = self.revisar()
                estacion[pos] = True
                break"""
        with self.mon_est[pos]:
            print("Estacion #" + str(pos + 1))
            ite = c.limite - c.ca
            c.pos = pos
            for i in range(ite):
                with self.mon_tan[int(pos/2)]:
                    if tanques[int(pos / 2)] == 0:
                        self.mon_tan[int(pos/2)].wait_for(self.revisar_llenado())
                        cont += 1
                        self.mon_tan[int(pos/2)].wait_for(self.llenar_surtidor(int(pos/2)))
                        cont -= 1
                    time.sleep(0.5)
                    c.ca += 1
                    tanques[int(pos / 2)] -= 1
                    print(c.nombre + " #" + str(c.id) + " llenando tanque, capacidad " + str(c.ca) + " de " + str(c.limite) + "\n")
            estacion[pos] = False
            c.estado = 2

mon = monitor()

class V():
    def __init__(self, t, v):
        self.nombre = ""
        self.id = v
        self.cola = None
        self.tipo = t
        self.limite = 0
        self.imagen = ''
        self.pos = -100
        self.estado = 0
        if t == 1:
            self.limite = 20
            self.nombre = 'Moto'
            self.imagen = 'bike.png'
        elif t == 2:
            self.limite = 40
            self.nombre = 'Carro'
            self.imagen = 'car.png'
        else:
            self.limite = 60
            self.nombre = 'Camión'
            self.imagen = 'truck.png'
        self.ca = random.randrange(0, self.limite, 1)



def get_params():
    global vehiculos
    with open('parameters.txt', 'r') as f:
        s = f.read()
        vehiculos = ast.literal_eval(s)


def crear_vehiculos():
    global lista_v
    for i in vehiculos:
        for v in range(vehiculos[i]):
            lista_v.append(V(i, v+1))


def ventana():
    global cont
    global cont_cola
    global queue
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)

    V = []
    Vrect = []
    T = []
    Trect = []

    # Set the height and width of the screen
    size = [1000, 500]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("GAS STATION")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(60)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        screen.fill(GRAY)

        pygame.draw.polygon(screen, YELLOW, [(805, 190), (805, 230), (785, 210)])
        pygame.draw.rect(screen, YELLOW, [805, 203, 80, 15])

        pygame.draw.rect(screen, YELLOW, [820, 0, 25, 160])
        pygame.draw.rect(screen, BLACK, [820, 0, 25, 160], 2)

        pygame.draw.rect(screen, YELLOW, [820, 260, 25, 300])
        pygame.draw.rect(screen, BLACK, [820, 260, 25, 300], 2)

        font = pygame.font.Font('freesansbold.ttf', 16)
        font2 = pygame.font.Font('freesansbold.ttf', 12)

        dy = 0
        d = 0
        for v in lista_v:
            V.append(pygame.image.load(v.imagen))
            Vrect.append(V[-1].get_rect())
            T.append(font2.render(v.nombre + " #" + str(v.id), True, BLACK, GRAY))
            T.append(font2.render(str(v.ca) + '/' + str(v.limite), True, BLACK, GRAY))
            Trect.append(T[-1].get_rect())
            Trect.append(T[-2].get_rect())
            if v.estado == 1:
                Vrect[-1].center = ((v.pos + 1) * 100 + 60, 150)
                screen.blit(V[-1], Vrect[-1])
                Trect[-1].center = ((v.pos + 1) * 100 + 65, 75)
                screen.blit(T[-1], Trect[-1])
                Trect[-2].center = ((v.pos + 1) * 100 + 50, 55)
                screen.blit(T[-2], Trect[-2])
            elif v.estado == 0 and len(queue) > 0:
                try:
                    V.append(pygame.image.load(queue[d].imagen))
                except:
                    print('error maligno')
                Vrect.append(V[-1].get_rect())
                Vrect[-1].center = (950, 250 + dy)
                dy += 130
                d += 1
                screen.blit(V[-1], Vrect[-1])
                del V[-1]
                del Vrect[-1]

        pygame.draw.rect(screen, RED, [200, 300, 200, 100], 2)
        pygame.draw.rect(screen, BLUE, [202, 302, 197, 97])
        if cont >= 1:
            gand = pygame.image.load("gandola.png")
            gandrect = gand.get_rect()
            gandrect.center = (300, 450)
            screen.blit(gand, gandrect)

        pygame.draw.rect(screen, RED, [500, 300, 200, 100], 2)
        pygame.draw.rect(screen, BLUE, [502, 302, 197, 97])
        if cont == 2:
            gand2 = pygame.image.load("gandola.png")
            gandrect2 = gand2.get_rect()
            gandrect2.center = (600, 450)
            screen.blit(gand2, gandrect2)

        pygame.draw.rect(screen, GREEN, [202, 100 + 2 + int(100 * (K - tanques[0])/K), 22, int(100 * tanques[0]/K)])
        pygame.draw.rect(screen, BLACK, [200, 100, 25, 102], 2)
        text1 = font.render(str(tanques[0]) + '/' + str(K), True, BLACK, GRAY)
        textrect1 = text1.get_rect()
        textrect1.center = (212, 220)
        screen.blit(text1, textrect1)

        pygame.draw.rect(screen, GREEN, [402, 100 + 2 + int(100 * (K - tanques[1])/K), 22, int(100 * tanques[1]/K)])
        pygame.draw.rect(screen, BLACK, [400, 100, 25, 102], 2)
        text2 = font.render(str(tanques[1]) + '/' + str(K), True, BLACK, GRAY)
        textrect2 = text2.get_rect()
        textrect2.center = (412, 220)
        screen.blit(text2, textrect2)

        pygame.draw.rect(screen, GREEN, [602, 100 + 2 + int(100 * (K - tanques[2])/K), 22, int(100 * tanques[2]/K)])
        pygame.draw.rect(screen, BLACK, [600, 100, 25, 102], 2)
        text3 = font.render(str(tanques[2]) + '/' + str(K), True, BLACK, GRAY)
        textrect3 = text3.get_rect()
        textrect3.center = (612, 220)
        screen.blit(text3, textrect3)

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


def main():
    global mon
    pr = []
    get_params()
    crear_vehiculos()
    random.shuffle(lista_v)
    for i in lista_v:
        pr.append(lambda: mon.cola_entrada(i))
        threading.Thread(target=pr[-1]).start()
    #threading.Thread(target=ventana()).start()
    ventana()

if __name__ == "__main__":
    main()


