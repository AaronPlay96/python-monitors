import threading
import time
import random
import ast
from threading import Condition as C
from threading import Lock as L
import math

K = 10

vehiculos = {}
lista_v = []
tanques = [K, K, K]
estacion = [False] * 6
llenado =  [False] * 2

l1 = L()
l2 = L()
l3 = L()
l4 = L()
l5 = L()
l6 = L()

ls1 = L()
ls2 = L()
ls3 = L()


class monitor:
    global K
    global estacion
    mon_est = [C(l1), C(l2), C(l3), C(l4), C(l5), C(l6)]
    mon_sur = [C(ls1), C(ls2)]
    mon_g = C(L())
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

    def revisar_llenado(self):
        for i in range(2):
            if not llenado[i]:
                self.ps = i
                return i
        return math.inf

    def surtir(self, c):
        while True:
            if self.revisar() >= 0 and self.revisar() <= len(lista_v) - 1:
                pos = self.revisar()
                estacion[pos] = True
                break
        with self.mon_est[pos]:
            print("Estacion #" + str(pos + 1))
            ite = c.limite - c.ca
            posl = self.revisar_llenado()
            for i in range(ite):
                with self.mon_sur[posl]:
                    if tanques[int(pos / 2)] == 0:
                        while True:
                            if self.revisar_llenado() >= 0 and self.revisar_llenado() <= 1:
                                posl = self.revisar_llenado()
                                llenado[posl] = True
                                break
                        self.mon_sur[posl].wait_for(self.llenar_surtidor(str(int(pos/ 2))))
                        llenado[posl] = False
                time.sleep(0.5)
                c.ca += 1
                tanques[int(pos / 2)] -= 1
                print(c.nombre + " #" + str(c.id) + " llenando tanque, capacidad " + str(c.ca) + " de " + str(c.limite) + "\n")
            estacion[pos] = False



class V():
    def __init__(self, t, v):
        self.nombre = ""
        self.id = v
        self.tipo = t
        self.limite = 0
        if t == 1:
            self.limite = 20
            self.nombre = 'moto'
        elif t == 2:
            self.limite = 40
            self.nombre = 'carro'
        else:
            self.limite = 60
            self.nombre = 'camion'
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


if __name__ == "__main__":
    pr = []
    mon = monitor()
    get_params()
    crear_vehiculos()
    random.shuffle(lista_v)
    for i in lista_v:
        pr.append(lambda: mon.surtir(i))
        threading.Thread(target=pr[-1]).start()
