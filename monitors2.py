import threading
import time
import random
import ast


vehiculos = {}
lista_v = []
tanques = [100] * 3
estacion = [False] * 6


class monitor:
    global tanques
    global estacion
    mon_espacios = threading.Condition(threading.Lock())
    mon_tanques = threading.Condition(threading.Lock())

    def __init__(self):
        self.pv = 0

    def revisar(self):
        for i in range(6):
            if not estacion[i]:
                self.pv = i
                estacion[i] = True
                return True
        return False

    def llenar_surtidor(self, index):
        time.sleep(0.5)
        tanques[int(index)] += 1
        print(str(tanques[int(index)]) + " de 100")

    def surtir(self, c):
        with self.mon_espacios:
            while not self.revisar():
                self.mon_espacios.wait()
            self.mon_espacios.notify_all()
            print("Estacion #" + str(self.pv + 1))
            for i in range(c.limite - c.ca):
                with self.mon_tanques:
                    while not estadot[int(self.pv / 2)]:
                        print("llenando tanque surtidor #" + str(int(self.pv / 2)) + "...")
                        self.llenar_surtidor(str(int(self.pv / 2)))
                        self.mon_tanques.wait()
                    estadot[int(self.pv / 2)] = True
                    self.mon_tanques.notify_all()
                c.ca += 1
                print(c.nombre + " #" + str(c.id) + " llenando tanque, capacidad " + str(c.ca) + " de " + str(c.limite))
                time.sleep(0.5)
                tanques[int(self.pv / 2)] -= 1
                if tanques[int(self.pv / 2)] == 0: estadot[int(self.pv / 2)] = False
                print("capacidad del tanque surtidor #" + str(int(self.pv / 2)) + ": " + str(tanques[int(self.pv / 2)]))
            self.mon_espacios.notify_all()
            estacion[self.pv] = False

class V(threading.Thread):
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
    for i in lista_v:
        pr.append(lambda: mon.surtir(i))
        Thread(target=pr[-1]).start()